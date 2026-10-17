---
title: Installation Guide
---

MIA MotionForge installs like any other plugin: put the `MIA MotionForge` folder in your project's
`Plugins/` directory (or use `Edit > Plugins > Install` on a packaged copy), enable it, and restart
the editor. That gets you the **MIA MotionForge** toolbar button, the Recipe editor, the bundled
skeleton and the retarget workflow. Generation needs one more thing: the model weights.

MIA MotionForge never bundles NVIDIA's Kimodo checkpoint or Meta's Llama-3 text encoder. You download
them, and you accept the model licences yourself.

## kimodo.cpp (built in, no Python or CUDA)

The generator is built into the plugin: a library build of `github.com/localai-org/kimodo.cpp`
(Apache-2.0) runs inside the editor, so there is nothing to install or compile and no other program
is ever started. It comes in two versions, one using the GPU through Vulkan and one for the CPU only.
The GPU version needs nothing beyond your normal graphics driver; without one, MIA MotionForge uses
the CPU version.

1. Click the **MIA MotionForge** toolbar button. The **Setup Wizard** opens.
2. Read and accept both licences it shows (NVIDIA Open Model License for the motion model, Meta
   Llama 3 Community License for the text encoder).
3. Press **Download**. The wizard fetches the motion model (~1.1 GB) and the text-encoder bundle
   (~15 GB) from their public Hugging Face mirrors into `Saved/MotionForgeModels`, and fills in the
   settings for you. An interrupted download continues where it stopped when you press Download again.
4. Open the Recipe editor's **Setup** tab and press **Check Setup**. It loads the generator and
   confirms it runs on this machine.

Plan for disk space (~16 GB) and time: the first take of a new prompt takes about 15-25 seconds,
most of it reading the prompt with the text model. Repeat takes of the same prompt are much faster
(well under a second on a GPU). It's local and free to run as often as you like.

### Setting it up by hand

If you already have the weights (from kimodo.cpp's own `scripts/download_gguf_weights.py --model
soma-rp-v1.1`), set these in **Edit > Editor Preferences > Plugins > MIA MotionForge**:

- `Kimodo Cpp Motion Gguf` -> the motion GGUF (e.g. `models/kimodo-soma-rp-v1.1-f32.gguf`)
- `Kimodo Cpp Text Bundle Dir` -> the text-encoder bundle folder (`generated/llm2vec-text-bundle/`)

Then accept the licences in the Setup tab (**Review & Accept Licences**) - Generate stays off until
you do.

## Remote server (generate on another machine)

To generate on a stronger PC on your network, run the MIA MotionForge server there and set
**Backend** to "Remote server (URL)" with its address (for example `http://192.168.1.20:7870`) in
Editor Preferences > Plugins > MIA MotionForge > Remote Server. The Setup tab's **Check Server**
tests the connection. The server is a separate download, not part of the plugin:
https://github.com/pr3vail/MotionForge-Docs/tree/main/server (its README has the steps).

## Retargeting

Every backend generates onto the bundled SOMA77 skeleton, not your character. Retarget needs an
**IK Rig** on your target mesh; if it has none, MIA MotionForge creates one automatically for
mannequin-shaped humanoids. For unusual rigs, build one yourself (Window > Animation > IK Rig
Editor). The bundled skeleton already ships with its IK Rig.

See [User Guide](user-guide.md) for the day-to-day workflow, and the plugin's `Docs/NOTICES.md` for exactly what is and isn't
redistributed with this plugin.
