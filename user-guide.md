---
title: User Guide
---

You describe a body moving in plain words; MotionForge runs NVIDIA's Kimodo model on your own
machine and gives you an animation on its bundled SOMA skeleton. You then trim it, touch it up by
hand, export a clip ready for your game, and retarget it onto your own character. Nothing leaves
your computer.

**The one thing to know first:** the model generates a *body*. It has no idea swords, chairs or
floors exist. "Sits in a chair" gives you a seated posture in mid air. That's normal - you add the
chair as a preview mesh and pose the body onto it (see *Props*).

## Opening MotionForge

Click the **MotionForge** button on the main editor toolbar. It reopens the recipe you touched
most recently, or creates a new one under your Recipes folder. You can also right-click in the
Content Browser to create a *MotionForge Recipe*, or double-click any recipe.

If generation isn't set up yet, the Setup Wizard opens first (see [Installation Guide](installation-guide.md)).

## The editor

Five dockable tabs. Drag them anywhere; **Window > Load Layout > Default Editor Layout** resets.

| Tab | What it's for |
|---|---|
| **Viewport** | Watch the animation, pose it by hand, place props. Status lines on top say whether Generate can run and what the last action did. |
| **Timeline** | The prompt timeline, the frame ruler, the export range and your pose keys. |
| **AutoPose** | Posing controls: gizmo mode, World/Local, IK/FK, Capture/Pin, Make Loop, the bone picker. |
| **Details** | Every recipe setting: seed, samples, steps, guidance, export, props, target mesh, loaded clip. |
| **Setup** | Backend health, Check Setup, licences, search, this machine, where files go. |

### Toolbar

| Button | What it does |
|---|---|
| **Generate** / **Cancel** | Runs the recipe. While running it becomes Cancel (finished takes are kept). |
| **New Seed** | Draws a fresh seed and pins it. |
| **Takes** | Switch between the takes of the last Generate; *Pin This Take's Seed*. |
| **Import Clip** | Import a `.bvh`, or a kimodo.cpp output folder (pick its `.f32` file). |
| **Load Clip...** | Preview any AnimSequence already in your project. |
| **Refresh** | Stop and reload the recipe's clip. |
| **Export** | Make the finished clip (see *Exporting*). |
| **Retarget** | Retarget the latest export onto a base character, Manny/Quinn/UEFN, or your own mesh. |
| **Show** | Preview the generated, exported or retargeted clip, or the reference pose. |
| **Tour** / **Guide** | The editor tour, and this guide (see *Help inside the editor*). |
| **Search box** | Find any recipe, clip, guide section or tab (see *Search*). |

## Help inside the editor

Two buttons and a search box at the right of the recipe editor's toolbar:

| Button | What it does |
|---|---|
| **Tour** | A short walk through the five tabs and the toolbar, one caption at a time (Back / Next / Skip). It also runs by itself the first time a project opens a recipe. |
| **Guide** | Opens this guide in an editor window. |
| **Search box** | Type what you're looking for; see *Search*. |

## Search

The search box at the right of the toolbar finds:

| Result | What it matches | Picking it |
|---|---|---|
| **Recipe** | Every recipe in the project, by the words of its prompts | Opens it |
| **Clip** | Clips a recipe made (under that recipe's prompts), and other clips in your Generated, Exports and Retargeted folders (by name) | Selects it in the Content Browser |
| **Guide** | Each section of this guide | Opens the guide at that section |
| **Tab** | The editor's five tabs | Brings the tab forward |

Exact-word matches show up while you type. With an embedding model, results that match by *meaning*
follow a moment later, marked **related**: "greeting a friend" finds a recipe prompted "a person waves
hello", though they share no words. Up/Down and Enter pick a result; Esc closes the list.

**Setup tab > Search** shows which model the box is using (**Check**), embeds everything up front (**Index Now**), and opens the settings (**Search Settings** - *Editor Preferences > Plugins > MotionForge > Search*). **Auto (local)** uses an embedding model in Ollama (install one with `ollama pull nomic-embed-text`) or one loaded in LM Studio, and never a cloud service by itself. Pick OpenAI, Gemini or a Custom server there to use one; your prompts and this guide's text are then sent to it to be embedded. **Off** keeps the box to exact words.

Embeddings are cached in the project's `Saved` folder, so an unchanged recipe is never embedded twice.
Without an embedding model the box still works, by exact words, and says so under the results.

## Writing prompts

Describe the body, not the mood. Name the limb and the side, say how fast, say what the feet do.

| Instead of | Write |
|---|---|
| zombie walk | a person shuffles forward slowly, hunched, arms hanging loose, dragging the right leg |
| cool sword attack | a person swings a heavy two-handed sword down from over the right shoulder in a fast diagonal arc |
| kick the door | a person raises the right knee and drives a straight kick forward at waist height, then plants the foot |

Match the duration to the action: a punch ~1-1.5 s, a sword swing ~1.5 s, a walk cycle 2-3 s,
sitting down 4-5 s. Give a punch 5 seconds and you get a punch followed by drifting.

### The prompt timeline

Each row is one segment: a prompt and a duration. Several segments generate **one continuous
clip** that moves through them in order, with a real transition authored by the model.

| Control | What it does |
|---|---|
| **+** | Add a segment. |
| **<** / **>** | Move it earlier / later. |
| **Lock** | Protect it from accidental edits. |
| **Mute** | Keep it, but leave it out of the next Generate. |
| **Delete** | Remove it. |

Transitions must be physically possible: lying down followed by sprinting needs a bridging segment
("the person pushes up to standing") in between.

## Generating

| Setting (Details) | Meaning | Use |
|---|---|---|
| **Samples** | Takes per Generate (seed, seed+1, ...). Each take is a separate run. | 2-4 while exploring, 1 once you like a take. |
| **Seed** | -1 draws a new one each time. | Pin a seed (Takes > Pin This Take's Seed) and change one thing at a time. |
| **Diffusion Steps Override** | Quality vs time. 0 uses the global setting. | 10-20 while iterating, then back up. |
| **Num Transition Frames** | Frames the model spends blending one segment into the next. | 5 is fine. |
| **Text Cfg Weight** | How literally the prompt is obeyed. | 2.0; raise to 3-4 if ignored (stiffer); lower toward 1.5 if robotic. |
| **Transition Cfg Weight** | How hard each segment's start is held to the end of the previous one. | 2.0; raise if transitions pop, lower if they look forced. |

After Generate, the status line reads the result: take, seed, length, and **how far the pelvis
travelled** (straight-line and along its path). A "walk forward" that travelled almost nothing
did not walk, whatever a still frame looks like.

Every take gets an immutable **result record** (recipe hash, seed, steps, backend, model, prompts,
metrics) in your Results folder, so any clip can be traced back and reproduced. Don't hand-edit
those.

**Editing a recipe changes its identity.** Change a prompt, duration, seed, steps or guidance and
the loaded clip is marked stale (orange status line) - it no longer matches the recipe. Colours,
locks, pose keys, export range and props don't count; changing them never marks a clip stale.

## AutoPose: posing by hand

AutoPose is for "nearly right, but the hand should be *here*". You pose a joint at a frame; that
becomes a **key** that fades in and out around its frame and is baked into the exported clip.

MotionForge's kimodo.cpp backend has no pose-constraint input, so keys are an edit on top of the
generated motion - they don't make the model re-author the motion around them. Key sparsely: two
or three keys at the extremes of an action (the contact, the peak) shape a clip; twenty keys make
it look interpolated.

1. Press **AutoPose: Off** to turn it on. Playback pauses.
2. Click a joint in the viewport (or a button in the bone picker).
3. Drag the gizmo. Every finished drag keys itself at the playhead.

| Key / control | What it does |
|---|---|
| **W** / **Move** | Move gizmo. Moves the pelvis; with **IK** on, drags a hand or foot as a goal. |
| **E** / **Rotate** | Rotate gizmo. |
| **World / Local** | Handle orientation: World to put a foot on the ground, Local to bend a joint about its own axis. |
| **FK / IK** | Hands and feet only. FK rotates the wrist/ankle; IK solves the whole arm or leg to reach the goal. |
| **Capture Whole Pose (F)** | Key every joint that currently differs from the generated pose, at this frame. |
| **Pin Current Pose** | Key the selected joint exactly where it is - to hold it while you pose something else. |
| **Make Loop** | Keys the export range's last frame to its first frame's pose (travel is kept), blending in over the final frames. |
| **Revert All Pose Edits** | Delete every key. Ctrl+Z brings them back. |
| **Pitch / Yaw / Roll** | Type the selected joint's rotation at this frame directly. |

Everything is undoable with **Ctrl+Z**.

### Working with keys on the timeline

Each posed bone gets its own lane. A key is drawn as a square with a bar showing its blend span.

| Action | How |
|---|---|
| Play / pause | Spacebar |
| Scrub | Click or drag the ruler |
| Step a frame | Left / Right arrows, or the transport buttons |
| Select a key | Click it |
| Re-time a key | Drag it along its lane |
| Delete a key | Delete |
| Copy / paste | Ctrl+C, then Ctrl+V pastes at the playhead |

The panel under the lanes edits the selected key: nudge a frame, **Blend in/out** (frames either
side), **To clip ends**, **Weight**, **Enabled**, **Lock**, **Duplicate** (to the playhead),
**Delete**.

## Props: posing against something real

| Kind | Behaviour | For |
|---|---|---|
| **Preview Prop** | Follows a bone. | Anything held - a sword, a rifle, a mug. |
| **Preview Scene Mesh** | Stands still in the scene. | Anything the body moves against - a chair, a crate, a ledge. |

Both are preview only: never sent to the model, never exported, never mark a clip stale.

- **Held prop:** in Details > Preview Prop, set the mesh and pick the **Attach Bone** from the
  dropdown (RightHand is typical). Then click the prop in the viewport and move it with the gizmo,
  or type the offset.
- **Scene mesh:** set it in Details > Preview Scene, click it and move it, then **Drop Scene Mesh
  To Floor** (AutoPose tab) to sit its lowest point on the ground - rotation is accounted for.

Props are picked by their bounding box. A joint click always wins over a prop behind it; click
empty space to put the gizmo back on the body. Props can be moved with AutoPose on or off.

## Exporting

Generations drift; the middle is usually the strongest part. Export the good part.

1. Drag on the **Animation** row of the timeline to set the export range. The line above the
   timeline reports it, e.g. `Export range: F23 - F96, 74 frames, 2.433s`. Playback loops inside
   the range so you can judge a loop by eye.
2. Choose **Export Motion** in Details:

| Export Motion | What you get | Use it for |
|---|---|---|
| **Root Motion** | Travel and turning move onto the root bone and Unreal extracts them, so a capsule follows. | Root-motion locomotion, dodges, traversal, Motion Matching. |
| **In Place** | Travel removed; the body plays on the spot. | Blendspace locomotion where your code moves the capsule. |
| **As Generated** | Travel stays on the body; nothing extracted. | Cinematics, emotes, anything you place yourself. |

3. Press **Export**. The clip is trimmed, keys are baked in, and the motion mode is applied. It's
   saved as `A_<Recipe>_<hash>` in the recipe's Output Directory (or your Exports folder).
   Re-exporting the same recipe revision overwrites its previous export.

**Why the root path is smoothed:** a walking pelvis sways side to side each step; copied straight
onto the root, the capsule snakes. The root path is averaged over roughly one stride (**Root
Motion Smoothing Frames** in settings, default 31; 0 = exact), and the sway stays on the body. The
dotted line on the viewport floor (**Root Path**) is the raw pelvis path, before smoothing.

A Root Motion clip looks like it runs on the spot in the animation editor - there's no capsule
there. Play it on a character.

## Retargeting onto a character

Open the **Retarget** menu on the toolbar and pick a character. MotionForge retargets the latest
export (or the raw clip if nothing is exported) through Unreal's IK Retargeter and shows the result.

| Menu entry | What it is |
|---|---|
| **Base Male (MotionForge)** / **Base Female (MotionForge)** | Ready-made base characters that ship with the plugin: a neutral mannequin body on a UE-mannequin-style skeleton (`pelvis`, `spine_01`, `upperarm_l`, `thigh_l`, full fingers), with a physics asset. Free to use in your game. |
| **UE5 Manny** / **UE5 Quinn** / **UEFN Mannequin** | Epic's mannequins, when they're in your project. |
| **Target Skeletal Mesh** | Your own character, set in Details > Retarget. Asks where to save the result. |

One-click characters need no setup: MotionForge builds its own IK Rig for the target automatically
(chains only, so a solver in a hand-made rig can't pin the pelvis) and keeps it next to the result.
Retargets onto the base characters land in `/Game/MotionForge/Retargeted/<Character>`; retargets
onto your own meshes go next to the mesh.

MotionForge's skeleton stands in a T-pose, while Manny, Quinn and most game characters stand in
an A-pose. The first time a character is retargeted, MotionForge lines its arms and legs up with the
T-pose in a retarget pose called **AlignedToSource**, so the arms hang as they do in the clip instead
of sitting out from the body. If a character needs a different starting pose, adjust that pose in
the IK Retargeter editor; MotionForge keeps your change.

**Manny and Quinn aren't bundled** - Epic's licence only lets them ship inside a project, not a
plugin - but they're free for every Unreal user. Add Epic's free *Mannequins Asset Pack* from
**Window > Fab** (or the Third Person template content) and they appear in the menu automatically.
The menu's **How do I get Manny and Quinn?** entry repeats these steps. The UEFN mannequin comes with
Epic's free Game Animation Sample the same way.

Check the result on the character: facing, feet on the ground, travel kept, natural wrists.

The IK Retargeter creates new animations with root-motion flags at their defaults; MotionForge
carries a Root Motion export's setting across for you. For clips retargeted by hand, right-click
them in the Content Browser: **MotionForge > Set Up For Root Motion** / **Set Up For In Place**.

Fix motion problems at the source (a better prompt, a key), not in the retarget.

## Scripting

The toolbar's Import Clip, Export and Retarget are also callable from Editor Utility Blueprints and
editor Python, under **MotionForge > Scripting** (`unreal.MotionForgeScriptLibrary`). Each returns
the new asset's path, or an empty string with the reason in its error output.

| Function | Does what the toolbar's... |
|---|---|
| **Import Clip** (source path, destination package) | Import Clip does: a `.bvh`, or a kimodo.cpp output folder, onto the bundled skeleton. |
| **Export Recipe Clip** (recipe) | Export does for that recipe's loaded clip. |
| **Retarget Clip** (clip, target mesh, output folder) | Retarget menu does; an empty output folder puts it next to the mesh. |

```
clip, err = unreal.MotionForgeScriptLibrary.import_clip("D:/kimodo/out/walk", "/Game/MotionForge/Generated/Walk")
```

## Demo level

The plugin's optional **Demo** folder has a level, `L_MotionForge_AnimationDemo`, where Epic's UE5 Manny
and Quinn play six MotionForge clips. In the Content Browser, turn on **Settings > Show Plugin Content**, then
open the level from **MotionForge Content > Demo > Maps**. Open any recipe in **Demo > Recipes** to see the
prompt behind a clip. MotionForge doesn't need the Demo folder - delete it whenever you like.

## Where files go

Set in **Edit > Editor Preferences > Plugins > MotionForge > Output**. Everything MotionForge
creates goes into your project, never the plugin.

| Folder (default) | Contents |
|---|---|
| `/Game/MotionForge/Recipes` | Your recipes |
| `/Game/MotionForge/Generated` | Raw generations, one per take |
| `/Game/MotionForge/Results` | One result record per take |
| `/Game/MotionForge/Exports` | Finished clips (a recipe's Output Directory overrides this) |
| `/Game/MotionForge/Retargeted` | Retargets onto the bundled base characters, one folder each |

## When something looks wrong

| You see | Do this |
|---|---|
| Wrong action | Rewrite the prompt in body terms. If it's still ignored, raise Text Cfg Weight. |
| Barely moves or drifts | Shorten the duration; describe the feet. |
| Right action, ugly execution | More Samples - it's random. |
| Stiff or robotic | Lower Text Cfg Weight; remove keys that fight the motion. |
| One limb wrong | A key on that limb at the extreme frame. |
| Good middle, bad ends | Trim the export range. |
| Two actions mushed together | Split them into two segments. |
| A transition is garbage | Add a bridging segment. |
| Sits or leans in mid air | Expected - add a Preview Scene Mesh and pose onto it. |
| Held object doesn't follow the hand | It's in Preview Scene Mesh; held objects go in Preview Prop. |
| Exported clip runs on the spot | Expected for Root Motion; play it on a character, or export As Generated. |
| Root path snakes | Raise Root Motion Smoothing Frames and export again. |
| Generate is greyed out | The top status line says why: backend not set up, licences not accepted, or no active prompt. |
| Generation is slow | Each take reloads the model (tens of seconds on CPU). Lower Samples and steps while iterating. |
