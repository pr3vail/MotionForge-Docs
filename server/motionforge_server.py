"""MIA MotionForge remote server: run MIA MotionForge's generator on another machine (a GPU box on your LAN)
and point the plugin at it (Editor Preferences > Plugins > MIA MotionForge > Backend: Remote server).

Needs only Python 3.9+ (standard library), the kimodo.cpp command-line build from this repo's
backend-1 release (kmd-generate.exe + its DLLs), and the motion .gguf and text bundle folder the
plugin's Setup Wizard downloaded. See README.md beside this file.

    python motionforge_server.py --exe path/to/kmd-generate.exe --model path/to/kimodo-soma-rp-v1.1-f32.gguf
        --text-bundle path/to/llm2vec-text-bundle [--host 0.0.0.0] [--port 7870] [--token SECRET] [--cpu]

Endpoints (JSON):
    GET  /v1/health     -> {"ok": true, "name": "MIA MotionForge server", "version": 1, "model": ..., "device": ...}
    POST /v1/generate   {"segments": [{"prompt": str, "frames": int}], "transition": int, "steps": int, "seed": int,
                         "textCfg": float, "constraintCfg": float, "constraints": [...] | null}
                        -> {"frames": int, "joints": int, "rotations": base64 f32 [T,J,4], "root": base64 f32 [T,3]}
With --token, every request needs "Authorization: Bearer SECRET". Requests run one at a time; the model
stays loaded between them, and a prompt it has seen recently skips re-encoding.
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = 1


class Worker:
    """One resident `kmd-generate --server` process; restarted when the guidance weights change."""

    def __init__(self, exe, model, bundle, force_cpu):
        self.exe, self.model, self.bundle, self.force_cpu = exe, model, bundle, force_cpu
        self.process = None
        self.cfg = None
        self.lock = threading.Lock()

    def _start(self, cfg):
        self.stop()
        args = [self.exe, "--server", self.model, self.bundle]
        text_cfg, constraint_cfg = cfg
        if abs(text_cfg - 2.0) > 1e-6:
            args += ["--text-cfg", f"{text_cfg:.3f}"]
        if abs(constraint_cfg - 2.0) > 1e-6:
            args += ["--constraint-cfg", f"{constraint_cfg:.3f}"]
        env = dict(os.environ)
        if self.force_cpu:
            env["KIMODO_BACKEND"] = "cpu"
        exe_dir = os.path.dirname(os.path.abspath(self.exe))
        env["PATH"] = exe_dir + os.pathsep + env.get("PATH", "")
        self.process = subprocess.Popen(args, cwd=exe_dir, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1)
        self.cfg = cfg

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.kill()
        self.process = None

    def generate(self, request):
        segments = request.get("segments") or []
        if not segments:
            raise ValueError("no segments")
        cfg = (float(request.get("textCfg", 2.0)), float(request.get("constraintCfg", 2.0)))
        work = tempfile.mkdtemp(prefix="motionforge-")
        try:
            fields = []
            constraints = request.get("constraints")
            if constraints:
                path = os.path.join(work, "constraints.json")
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(constraints, file)
                fields.append("constraints=" + path)
            out_dir = os.path.join(work, "out") + os.sep
            fields += [str(int(request.get("transition", 5))), str(int(request.get("steps", 50))),
                       str(int(request.get("seed", 0))), out_dir]
            for index, segment in enumerate(segments):
                prompt_path = os.path.join(work, f"prompt_{index}.txt")
                with open(prompt_path, "w", encoding="utf-8") as file:
                    file.write(str(segment["prompt"]).strip())
                fields += [str(int(segment["frames"])), prompt_path]
            with self.lock:
                if self.process is None or self.process.poll() is not None or self.cfg != cfg:
                    self._start(cfg)
                self.process.stdin.write("\t".join(fields) + "\n")
                self.process.stdin.flush()
                reply = self.process.stdout.readline().strip()
            if not reply:
                self.stop()
                raise RuntimeError("the generator stopped (see its console for why)")
            parts = reply.split("\t")
            if parts[0] != "OK":
                raise RuntimeError(parts[1] if len(parts) > 1 else reply)
            with open(os.path.join(out_dir, "local_rotations_xyzw.f32"), "rb") as file:
                rotations = file.read()
            with open(os.path.join(out_dir, "root_positions.f32"), "rb") as file:
                root = file.read()
            return {"frames": int(parts[1]), "joints": int(parts[2]),
                    "rotations": base64.b64encode(rotations).decode("ascii"),
                    "root": base64.b64encode(root).decode("ascii")}
        finally:
            shutil.rmtree(work, ignore_errors=True)


def make_handler(worker, token, device):
    class Handler(BaseHTTPRequestHandler):
        server_version = "MotionForgeServer/1"

        def _send(self, code, body):
            data = json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _authorized(self):
            if not token:
                return True
            if self.headers.get("Authorization", "") == "Bearer " + token:
                return True
            self._send(401, {"error": "wrong or missing token"})
            return False

        def do_GET(self):
            if not self._authorized():
                return
            if self.path.rstrip("/") == "/v1/health":
                self._send(200, {"ok": True, "name": "MIA MotionForge server", "version": VERSION,
                                 "model": os.path.basename(worker.model), "device": device})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            if not self._authorized():
                return
            if self.path.rstrip("/") != "/v1/generate":
                self._send(404, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                request = json.loads(self.rfile.read(length).decode("utf-8"))
                self._send(200, worker.generate(request))
            except Exception as error:  # reported to the plugin, which shows it
                self._send(500, {"error": str(error)})

        def log_message(self, fmt, *args):
            sys.stderr.write("[motionforge] " + (fmt % args) + "\n")

    return Handler


def main():
    parser = argparse.ArgumentParser(description="MIA MotionForge remote generation server")
    parser.add_argument("--exe", required=True, help="kmd-generate.exe (MIA MotionForge's build)")
    parser.add_argument("--model", required=True, help="motion .gguf")
    parser.add_argument("--text-bundle", required=True, help="text encoder bundle folder")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7870)
    parser.add_argument("--token", default="", help="require 'Authorization: Bearer TOKEN'")
    parser.add_argument("--cpu", action="store_true", help="never use the GPU")
    args = parser.parse_args()
    for path in (args.exe, args.model, args.text_bundle):
        if not os.path.exists(path):
            sys.exit(f"not found: {path}")
    worker = Worker(args.exe, args.model, args.text_bundle, args.cpu)
    device = "cpu" if args.cpu or "vulkan" not in os.path.dirname(os.path.abspath(args.exe)).lower() else "vulkan"
    server = ThreadingHTTPServer((args.host, args.port), make_handler(worker, args.token, device))
    print(f"MIA MotionForge server on http://{args.host}:{args.port} ({device}{', token required' if args.token else ''})", flush=True)
    try:
        server.serve_forever()
    finally:
        worker.stop()


if __name__ == "__main__":
    main()
