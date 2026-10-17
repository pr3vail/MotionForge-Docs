---
title: Remote server
---

# MIA MotionForge remote server

Run MIA MotionForge's generator on another machine - a PC with a better GPU on your network - and
generate from any editor that points at it. Clips come back to your editor and import exactly as local
takes do, constraints (pinned poses) included.

This server is a separate, optional download. It is not part of the MIA MotionForge plugin.

## On the server machine

1. Install Python 3.9 or newer (python.org). Nothing else: the server uses only the standard library.
2. Download to that machine:
   - [`motionforge_server.py`](motionforge_server.py) from this folder.
   - The kimodo.cpp command-line build from the
     [backend-1 release](https://github.com/pr3vail/MotionForge-Docs/releases/tag/backend-1):
     the `vulkan-*` files for a GPU, or the `cpu-*` files for the CPU only. Put them in one folder and
     drop the `vulkan-` / `cpu-` prefix, so it holds `kmd-generate.exe` and its `ggml*.dll` files.
   - The model files the plugin's Setup Wizard downloaded: `kimodo-soma-rp-v1.1-f32.gguf` and the
     `llm2vec-text-bundle` folder (by default in `<your project>/Saved/MotionForgeModels`).
3. Pick a token (any password) and start the server from a command prompt, with your own paths, on one line:

       python motionforge_server.py --exe "C:\MotionForgeBackend\kmd-generate.exe" --model "C:\MotionForgeModels\models\kimodo-soma-rp-v1.1-f32.gguf" --text-bundle "C:\MotionForgeModels\generated\llm2vec-text-bundle" --port 7870 --token <your token>

   Allow the port (7870) through that machine's firewall when Windows asks.

## In the editor

Editor Preferences > Plugins > MIA MotionForge:

- **Backend**: Remote server (URL)
- **Remote Server Url**: `http://<that machine's address>:7870`
- **Remote Server Token**: the token you picked

Then the recipe editor's Setup tab > **Check Server**.

The server runs one generation at a time and keeps the model loaded between them. It's meant for a
trusted network: use a token, and don't expose the port to the internet.
