---
title: Installation Guide
---

MotionForge installs like any other plugin: put the `MotionForge` folder in your project's
`Plugins/` directory (or use `Edit > Plugins > Install` on a packaged copy), enable it, and restart
the editor. That gets you the **MotionForge** toolbar button, the Recipe editor, the bundled
skeleton and the retarget workflow. Generation needs one more thing: the model weights.

MotionForge never bundles NVIDIA's Kimodo checkpoint or Meta's Llama-3 text encoder. You download
them under their own licences, which you accept yourself.

## Recommended: kimodo.cpp (portable, no Python or CUDA)

The default backend, with no Python environment to install. The generator itself -
`kmd-generate.exe`, a build of `github.com/localai-org/kimodo.cpp` (Apache-2.0) - ships inside the
plugin in two versions, one using the GPU through Vulkan and one for the CPU only, so there's nothing
to compile. The GPU version needs nothing beyond your normal graphics driver; without one, MotionForge
uses the CPU version.

1. Click the **MotionForge** toolbar button. The **Setup Wizard** opens.
2. Read and accept both licences it shows (NVIDIA Open Model License for the motion model, Meta
   Llama 3 Community License for the text encoder).
3. Press **Download**. The wizard fetches the motion model (~1.1 GB) and the text-encoder bundle
   (~15 GB) from their public Hugging Face mirrors into `Saved/MotionForgeModels`, and fills in the
   settings for you.
4. Open the Recipe editor's **Setup** tab and press **Check Setup**. It launches the generator once
   and confirms it runs on this machine.

Plan for disk space (~16 GB) and time: the first take of a new prompt takes about 15-25 seconds,
most of it reading the prompt with the text model. Repeat takes of the same prompt are much faster
(well under a second on a GPU). It's local and free to run as often as you like.

### Setting it up by hand

If you already have the weights (from kimodo.cpp's own `scripts/download_gguf_weights.py --model
soma-rp-v1.1`), set these in **Edit > Editor Preferences > Plugins > MotionForge**:

- `Kimodo Cpp Motion Gguf` -> the motion GGUF (e.g. `models/kimodo-soma-rp-v1.1-f32.gguf`)
- `Kimodo Cpp Text Bundle Dir` -> the text-encoder bundle folder (`generated/llm2vec-text-bundle/`)
- `Kimodo Cpp Generate Exe Path` -> leave empty to use the bundled generator. If you point it at
  your own kimodo.cpp build, note that the **Text/Transition Cfg Weight** recipe settings need the
  guidance flags MotionForge's bundled build adds (see `Resources/kimodo-cpp-win64/README.txt`);
  with an unpatched build, leave both at 2.0. Check Setup tells you which kind you have.

Then accept the licences in the Setup tab (**Review & Accept Licences**) - Generate stays off until
you do.

## Advanced: kimodo_gen (Python, PyTorch, GPU)

If you already run Kimodo's own PyTorch environment (faster on a strong GPU, but a full Python +
CUDA/ROCm + PyTorch stack):

1. Clone `github.com/nv-tlabs/kimodo` (Apache-2.0) and `pip install -e .` in your own venv.
2. Obtain `nvidia/Kimodo-SOMA-RP-v1.1` and `meta-llama/Meta-Llama-3-8B-Instruct` from Hugging Face
   under your own account (Meta's model needs a separate approval).
3. In Editor Preferences > Plugins > MotionForge, set `Motion Forge Executable Path` to the
   `kimodo_gen(.exe)` console script in your venv's `Scripts/` folder, and switch `Backend` to
   "kimodo_gen (Python venv)".

The Text/Transition Cfg Weight settings only apply to the kimodo.cpp backend.

## Retargeting

Both backends generate onto the bundled SOMA77 skeleton, not your character. Retarget needs an
**IK Rig** on your target mesh; if it has none, MotionForge creates one automatically for
mannequin-shaped humanoids. For unusual rigs, build one yourself (Window > Animation > IK Rig
Editor). The bundled skeleton already ships with its IK Rig.

See [User Guide](user-guide.md) for the day-to-day workflow, and the plugin's `Docs/NOTICES.md` for exactly what is and isn't
redistributed with this plugin.
