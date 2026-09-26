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
| **In Level** | Play the take on the character selected in the level (retargeted onto it first if needed), or on a new one in front of the camera (see *In the level*). |
| **Level Target** | Edit the constraint pins on that character in the level, with the level gizmo (see *Placing pins in the level*). |
| **Blender** | Edit in Blender, Sync Back, Auto Sync (see *Editing in Blender*). |
| **Jobs** | The Jobs tab: every generation, queued, running and finished (see *Working on many clips at once*). |
| **Tour** / **Guide** | The editor tour, and this guide (see *Help inside the editor*). |
| **Search box** | Find any recipe, clip, guide section or tab (see *Search*). |

### Viewport options

The row under the viewport: **Joints**, **Root Path** (the pelvis's ground path), **Contacts** (a green
ring under each planted foot - low and still, the same test the clean-up uses) and **Pins**
(constraints). **View** holds the floor toggle, playback speed (0.25x-2x) and the camera's field of
view.

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

### How long a take takes

On a CPU, most of a first take is spent reading your prompt with the text model (about 12 seconds),
and the rest is the diffusion steps (about half a second each). With the kimodo.cpp backend,
MotionForge keeps the model running between takes and remembers every prompt it has read, so **a second take of the same prompt skips
that part**: measured on a desktop CPU, a 2-second take at 5 steps went from 18 s to 3 s, and at 20
steps from 23 s to 10 s. That makes Samples of 2-4, a new seed, or a tweak to steps or guidance cheap
once the first take is done. A new prompt, or an edited one, pays the reading cost once.

The kept-loaded model uses memory while it's alive and exits after 10 idle minutes. Both are in
**Editor Preferences > Plugins > MotionForge > kimodo.cpp**: **Keep kimodo.cpp Loaded** and **Idle
Shutdown (minutes)**. Changing guidance restarts it once, because those values are read when
it starts.

**GPU or CPU.** MotionForge ships two builds of the generator: one that uses the GPU through Vulkan
and one for the CPU only. **Compute Device** (same settings page) picks between them:

| Compute Device | Runs on |
|---|---|
| **Auto** (default) | The GPU when this PC has Vulkan drivers (every current AMD, NVIDIA and Intel driver installs them), else the CPU. A GPU run that fails, for example out of video memory, is retried on the CPU, which is then used for the rest of the session. |
| **CPU only** | The CPU. |
| **Vulkan** | The GPU, reporting errors instead of falling back. |

The Setup tab's **This Machine** section says which one will be used. On a 16 GB AMD card, a repeat
take finished in about 0.1 s against 3 s on the CPU; a first take is only a little faster, because
reading the prompt is mostly reading the text model from disk. GPU and CPU results differ by float
rounding (about 1-2 cm on the root), so each take's result record notes which device made it.

**Segment length.** kimodo.cpp makes at most **10 seconds per segment** (300 frames); the timeline
won't go past that, and a longer segment from an older recipe stops Generate with a message naming
it. For longer motion, add segments: they still come out as one continuous clip.

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

Keys are an edit on top of the generated motion - they don't make the model re-author the motion
around them (a **constraint** does that; see the next section). Key sparsely: two or three keys at
the extremes of an action (the contact, the peak) shape a clip; twenty keys make it look
interpolated.

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

## Constraints: steering the model

A constraint is a pose the model must hit. Unlike an AutoPose key, which is baked on top afterwards,
a constraint is sent to the model with the prompt, so the **next Generate authors the whole motion
around it**: the steps before a planted foot lead into it, the body turns to reach a pinned hand.

Every backend takes constraints: the bundled kimodo.cpp (MotionForge's build adds constraint input
to it), kimodo_gen, and a remote server. If you point **Kimodo Cpp Generate Exe Path** at your own
kimodo.cpp build, it needs MotionForge's patch (`Resources/kimodo-cpp-win64/motionforge.patch`).

1. Get the body into the pose at a frame - pose it with AutoPose, or use a take that's close.
2. In the AutoPose tab under **Constraints**, pin what matters:

| Button | Holds | Kimodo type |
|---|---|---|
| **Pin Full Body** | Every joint, and where the body is. | `fullbody` |
| **Pin Root Path** | Where the pelvis is on the ground (X/Y). A few along a line make the character walk that path. | `root2d` |
| **Pin L / R Hand** | Where the hand is, and how it's turned. | `left-hand` / `right-hand` |
| **Pin L / R Foot** | Where the foot is - plant a step on a mark. | `left-foot` / `right-foot` |

3. Generate. Each take now bends to the pins (in testing, on every backend, pinned joints landed 2-7 cm from their pins,
   against 23-272 cm for the same seed without them).

Pinning snapshots the pose on screen, so loading another take never moves a constraint. The list
under the buttons can switch one off, jump to its frame (**Go**), replace it with the pose now on
screen (**Re-pin**) or delete it. Constraints also get their own lanes at the bottom of the
Timeline tab. A few well-spaced pins steer best; pinning every frame fights the model.

In the viewport, a pin on the current frame shows as a pink ghost of the pinned pose (the pinned hand
or foot circled), and Root Path pins show as pink rings joined on the floor. Turn them off with
**Pins** under the viewport.

### Placing pins in the level

**Level Target** (toolbar) edits the pins on a character standing in your level, against the real
scene: a hand on a real table, a step on a real stair.

1. Select the character in the level (or select nothing to get a new one in front of the camera).
2. Click **Level Target**. The take plays on the character, and every pin gets a marker: a small
   sphere for a hand or foot, a flat disc for a Root Path pin.
3. Move a marker with the level gizmo. A hand or foot pin re-solves that arm or leg, a Full Body pin
   moves the whole pose, and a Root Path pin moves on the ground. A marker the limb can't reach snaps
   back to where it can.
4. The character follows this editor's playhead, so scrub to a pin's frame to check it.
5. Click **Level Target** again to finish, then **Generate**.

Moving the character moves its markers with it. The markers are temporary and never saved with the
level. On a retargeted character, pins are scaled to its height.

### Drawing a path

To make the character walk a route, draw it:

1. **Draw Path**, then click points on the floor in the viewport. **Clear Drawing** starts over.
2. **Make Smooth** curves through the points; off, it's straight lines between them.
3. **Apply Path** turns the drawing into Root Path pins every *N* frames (**Pin every**), spread by
   distance over the recipe's whole length - a steady walking pace. It replaces the recipe's Root
   Path pins.
4. Generate with a walking prompt. **Shift Root Pins** moves every Root Path pin by an X / Y
   offset; **Remove Root Pins** clears them.

**Import... / Export...** read and write Kimodo's own `constraints.json`, so constraint sets move
between recipes, teammates and NVIDIA's Kimodo demo. Poses must be 77-joint SOMA poses.

Constraints can only be pinned on a clip on MotionForge's SOMA skeleton (a generated clip), not a
retargeted one. Adding, moving or switching off a constraint marks the loaded clip stale, since it
changes what's generated.

**Reduce Foot Sliding** (Details panel, Generation) lets kimodo_gen run Kimodo's own foot-skate
cleanup. It needs Kimodo's `motion_correction` extension built in your venv; leave it off if
generation fails with it on.

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

Tick **Clean Up On Export** (Details > Export) to run the clean-up below on every export.

## Cleaning up clips

Generated motion can float a little, sink a little, or let a planted foot slide. The clean-up fixes
that after the fact, on any clip - generated, exported or retargeted onto another character (it
finds the legs and arms on MotionForge's skeleton, Manny/Quinn, MetaHumans, UEFN, Mixamo and
Character Creator characters). Right-click clips > **MotionForge > Clean Up...**, or a folder >
**MotionForge: Clean Up Clips in Folder...**. It saves cleaned copies (`<clip>_Clean`) unless you
tick **Overwrite**.

| Pass | What it does |
|---|---|
| **Ground** | Moves the whole body up or down so planted feet stand at **Ground Height**. |
| **Ground Feet** | While a foot is planted, puts its sole on the floor (no floating, no sinking). |
| **Anchor Feet** | While a foot is planted, holds it still - removes foot sliding. |
| **Self Collision** | Pushes the arms out of the torso and thighs where they pass through the body. **Hands Only** is a gentler version for the hands alone. |

A foot counts as planted when it's below **Contact Height** (10 cm) and slower than **Contact
Speed** (15 cm/s) - Kimodo's own rule. Fixes fade in and out over **Blend Frames** and are capped by
**Max Correction**, so a wrong detection can't wreck a pose. Legs and arms are moved with two-bone
IK. Where a planted foot is out of reach even with the leg straight, **Lower Hips To Reach** drops
the hips just enough for it (capped by **Max Correction**, eased over the neighbouring frames).
Collision uses the character's own physics asset when it has one (the clip's preview mesh or its
skeleton's): every capsule, sphere and box on the body. Without one, it uses capsules sized from the
skeleton (shoulder and hip width). The report says which.

In testing on a generated walk, planted-foot sliding went from 2.1 cm to 0.0 cm and soles from 9.4
cm to 0.0 cm off the floor. With IK alone, without lowering the hips, the results were 0.6 cm and
1.3 cm. A clip lifted 6 cm was grounded back exactly. A hand driven into the chest was pushed 11 cm
clear, and to a physics-asset body's surface (24 cm) when it had one.

## Retargeting onto a character

Open the **Retarget** menu on the toolbar and pick a character. MotionForge retargets the latest
export (or the raw clip if nothing is exported) through Unreal's IK Retargeter and shows the result.

| Menu entry | What it is |
|---|---|
| **Base Male (MotionForge)** / **Base Female (MotionForge)** | Ready-made base characters that ship with the plugin: a neutral mannequin body on a UE-mannequin-style skeleton (`pelvis`, `spine_01`, `upperarm_l`, `thigh_l`, full fingers), with a physics asset. Free to use in your game. |
| **UE5 Manny** / **UE5 Quinn** / **UEFN Mannequin** | Epic's mannequins, when they're in your project. |
| **MetaHuman: *name*** | Each MetaHuman body in your project (found by its `metahuman_base_skel` skeleton). |
| **Character Creator: *name*** / **Mixamo: *name*** | Reallusion CC3/CC4 characters (`CC_Base_` bones) and Mixamo-rigged characters (`Hips`, `LeftUpLeg`... or `mixamorig:` bones) in your project. |
| **Target Skeletal Mesh** | Your own character, set in Details > Retarget. Asks where to save the result. |

MetaHumans, Character Creator and Mixamo characters only appear once they're in the project: add a
MetaHuman from the MetaHuman Creator or Quixel Bridge, or import a CC or Mixamo FBX as a skeletal mesh.
The menu lists up to 12 of them. For a MetaHuman, the clip goes onto the **body** (the face follows
through the MetaHuman Blueprint). To play it, set the clip on the Body component, or use it in the
MetaHuman's animation Blueprint.

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

A character with longer or shorter legs than MotionForge's skeleton can end up floating or sinking.
Tick **Ground Retargeted Clips** (Editor Preferences > Plugins > MotionForge > Export) to stand every
retarget back on the floor, or run **Clean Up** on it.

**Auto Scale Retargets** (same place, on by default) finds the stride scale for each character. That
is the IK Retargeter's **Pelvis Motion > Scale Horizontal**: how far the hips travel per centimetre
the source travels. MotionForge tries a few values with quick retarget passes and keeps the one with
the least foot sliding, and the status line reports it. In testing on a generated walk, sliding went
from 2.29 cm to 0.83 cm on the Base Male, 1.76 to 0.75 cm on the Base Female and 1.12 to 0.64 cm on
a MetaHuman. Turn it off to keep a scale you set yourself in the IK Retargeter.

MetaHuman clothing is separate meshes on the body's skeleton. To work with one mesh, select the body
and its garments and choose **MotionForge: Merge Body + Garments** (see [MetaHuman Guide](metahuman-guide.md)).

Fix motion problems at the source (a better prompt, a key), not in the retarget.

## Working on many clips at once

Select several assets in the Content Browser and right-click. Everything here does what the recipe
editor's buttons do, for the whole selection.

| On | Right-click > MotionForge > | What it does |
|---|---|---|
| **Animation sequences** | **Retarget To** > a character | Retargets every selected clip onto that character (the same list as the Retarget menu). Each lands next to the character, with its root-motion setting carried across. |
| | **Set Up For Root Motion** / **Set Up For In Place** | Sets the root-motion flags on every selected clip. |
| | **Clean Up...** | Grounds, plants and (optionally) un-collides every selected clip (see *Cleaning up clips*). |
| | **Chain into Level Sequence...** | Plays the clips back to back on one character in a new Level Sequence (see *In Sequencer*). |
| | **Lay Out in Level...** | A labelled grid of characters, one per clip (see *In the level*). |
| | **Edit in Blender** / **Sync Back from Blender** | See *Editing in Blender*. |
| | **Build Motion Index...** / **Export Animation Pack...** | See *Motion index and animation packs*. |
| **Folders** | **MotionForge: Clean Up Clips in Folder...** / **Build Motion Index for Folder...** / **Export Folder as Animation Pack...** | The same, for every clip in the folder and its subfolders. |
| **Blueprints** | **MotionForge: Make Playable Character...** | See *In the level*. |
| **Recipes** | **Generate Selected** | Queues each recipe in the Jobs tab; they generate one after another in the background, each with its own Samples, seed and settings. Recipes open in the recipe editor are skipped (generate those from their editor). |
| | **Export Selected** | Exports each recipe's loaded clip: trimmed, keys baked, Export Motion applied. |
| | **Retarget Latest Export To** > a character | Retargets each recipe's latest export (or its loaded clip, if it has no export). |

When an Export or Retarget batch finishes, the new clips are selected in the Content Browser and a
notification lists anything that failed and why.

### The Jobs tab

**Window > MotionForge Jobs** (or **Jobs** on the recipe editor's toolbar): every generation - queued,
running and finished - one row each, newest on top: recipe, status, takes done, time, where it came
from, backend, and what it made (click to find it in the Content Browser; hover for the list and any
error). **Cancel** takes a queued job out or stops the running one (finished takes are kept);
**Cancel All**, **Clear History**. The history survives restarts (`Saved/MotionForge/JobHistory.json`).
The recipe editor's own Generate shows up here too.

### Batches from a prompt file

**New Batch from Prompt File...** (in the Jobs tab) turns a list of prompts into recipes and generates
them all. Load a file or paste the list:

```
# Walk set
1. a person walks forward and waves | 6s | seed 12 | name Wave
2. a person jogs in a circle
- a person sits down -> stands up | 3s, 2.5s
```

One clip per line. Only the prompt is required; `| 6s` sets the length, `| seed 12` pins the seed,
`| name Wave` names the recipe, and `a -> b` makes two segments (with a length each, `3s, 2.5s`).
List markers, `#` headings and `>` quotes are ignored. A CSV (`prompt,duration,seed,name`, durations
of segments separated by `;`) works too.

Each line becomes a recipe in the batch folder and a job in the queue. Optionally each finished line
is exported (with an Export Motion of your choice), retargeted onto any characters you tick, and
renamed by a **Name pattern**: `{Index}` (the line number, 001), `{Recipe}`, `{Prompt}` (its first
words), `{Target}` (the character), `{Seed}`, `{Kind}` (Export / Retarget) - e.g.
`A_{Index}_{Prompt}_{Target}`.

A batch keeps a record in `Saved/MotionForge/Batches`, so a batch that was cancelled, failed partway or
cut short by closing the editor carries on from **Resume Batch** - only the unfinished lines run
again (**Run Every Line Again** redoes all of them).

### Importing prompts into one recipe

**Import Prompts...** under the prompt timeline pastes a list the same way, but every line becomes a
segment of this recipe - one continuous clip - instead of a recipe of its own.

## In Sequencer

The full walkthrough is in [Sequencer Guide](sequencer-guide.md).

**The MotionForge track.** On a character's row, click **+ Track > MotionForge** to add a shot at the
playhead: a prompt over a stretch of time. Right-click the shot and choose **Generate**. MotionForge
reads the pose just before the shot and the pose at its end, from whatever plays there (animation
clips, or a Control Rig track you keyed by hand), and pins them. It then generates between them and
puts the take on the character's animation track. Generating again replaces the shot's last take.
To land a move exactly, key the pose on a Control Rig track at the shot's end and generate into it.

Open a Level Sequence with a character in it. Sequencer's toolbar also gets a **MotionForge** menu.

**Generate on Selected Character...** - select the character's track, put the playhead where the new
motion should start, and write the prompt (one segment per line; `| 2s` for a segment's length).
MotionForge generates in the background (see the Jobs tab), retargets the result onto that character
if it needs it, and adds it to the character's animation track at the playhead. **Start from the
pose playing here** pins the new motion's first frame to the MotionForge clip already playing at the
playhead, so it carries on from it instead of snapping to a new start. **Mute the older sections it
overlaps** keeps the old take on the track, switched off. Both the raw clip and the retargeted one are
kept.

**Add Prompt Subtitles** - shows each MotionForge clip's prompt as a line of text over the selected
character while it plays (a text actor per clip, attached to the head).

**Bake Selected to Control Rig** - turns the selected character's animation into an FK Control Rig
track, so any joint can be keyed by hand.

**Chain into Level Sequence...** (right-click clips in the Content Browser) builds a new Level
Sequence that plays the selected clips back to back on one character, in the order you selected them.
Each clip starts where the previous one ended, facing the way it faced (**Match height** off keeps
every clip's own height), and neighbouring clips blend over **Blend frames**. **Show each clip's
prompt as a subtitle** adds the subtitles as above.

## In the level

**In Level** (recipe editor toolbar) plays the take in the level itself: on the character you have
selected there - retargeted onto it first if its skeleton is different - or, with nothing selected, on
a new character in front of the camera.

**Level Target** (recipe editor toolbar) plays the take on that character too, and puts each
constraint pin in the level as a marker you move with the gizmo (see *Placing pins in the level*).

**Lay Out in Level...** (right-click clips) places every selected clip in the level as a grid of
characters, each playing its clip on a loop, labelled with the clip's name and prompt, standing on the
floor below - a quick way to compare a batch. They go in the World Outliner folder
**MotionForge Layout**. Pick a **Character** to play them all on one character (retargeting as needed).

**Make Playable Character...** (right-click a MetaHuman's Blueprint, or any character Blueprint >
MotionForge) makes a playable character Blueprint: a child of the base class you pick with the MetaHuman
attached to its capsule. Pick a base that already moves - the Third Person template's character is
chosen for you when the project has it. **Make it the default pawn** also creates a game mode that
spawns it and sets it in **Project Settings > Maps & Modes**. (Tested with a stand-in Blueprint; with a
real MetaHuman you may still need to point its body at the base character's animation, the way
Epic's MetaHuman docs describe.)

## Motion index and animation packs

**Build Motion Index...** (right-click clips, or a folder) makes a DataTable with one row per clip:
the prompt it came from, its length, seed, character, kind (take, export or retarget), the recipe,
how far it travels, and **Tags** for searching. Tags are the prompt's key words plus what the motion
does: `in-place` or `travels`, a pace (`slow`, `walking-pace`, `running-pace`), `turns`, `loops`,
`short` or `long`, and the kind. The row type (`FMotionForgeMotionIndexRow`) is in the plugin's runtime module, so
your game can read the table to pick clips. CSV and JSON copies go to `Saved/MotionForge/Index`.

**Export Animation Pack...** copies the clips into a clean `/Game/<Pack>` folder - grouped by
character under `Animations/`, with the pack's own index in `Data/` - and writes `prompts.md`, the
index as CSV/JSON and a README to `Saved/MotionForge/Packs/<Pack>`. Right-click the pack folder >
**Migrate** to move it into an empty project for sharing or a Fab listing. Clips made with MotionForge
come from NVIDIA's Kimodo; check the model licence (NVIDIA Open Model License) before selling them.

## Editing in Blender

**Edit in Blender** (the recipe editor's **Blender** menu, or right-click a clip) opens the clip in
Blender. Edit it there, then press **Send to Unreal** (the **MotionForge** tab in the 3D viewport
sidebar, N) - or just save the .blend with **Send on Save** ticked. Back in Unreal, **Sync Back from
Blender** puts the edit on the **same** clip asset, so everything that uses it - a Blend Space, a
Sequencer section, a montage - sees the change. **Auto Sync** does the Sync Back by itself as soon as
Blender sends.

MotionForge finds Blender under Program Files; set **Blender Executable Path** (Editor Preferences >
Plugins > MotionForge > Blender) if it's elsewhere. The round trip goes through FBX in
`Saved/MotionForge/Blender`. In testing, a clip sent out and back unedited came back with the same
number of frames and every joint within 0.05 mm.

## Generating on another machine

Generation can run on another PC - a machine with a better GPU on your network - while you work.
Copy the plugin's `Resources/motionforge-server` folder, a `kimodo-cpp-win64` folder and the model files
to that machine and start `motionforge_server.py` there (its README has the steps; it needs only
Python). Then set **Backend** to **Remote server (URL)**, **Remote Server Url** to
`http://<that machine>:7870` and **Remote Server Token** to its token, and press **Check Server** in
the Setup tab. Everything else works the same - takes, constraints, the Jobs tab - with the clips
imported here. Use a token, and keep the port inside your network.

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
| `/Game/MotionForge/Batches/<Batch>` | Recipes made by a prompt-file batch |
| `/Game/MotionForge/Sequencer/<Sequence>` | Recipes made by Generate in Sequencer |
| `Saved/MotionForge/` | Job history, batch records (`Batches/`), index copies (`Index/`), pack files (`Packs/`), Blender round-trip FBX (`Blender/`) |

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
| Generation is slow | The first take of a new prompt spends ~12 s reading it; repeat takes of the same prompt skip that. Check **Keep kimodo.cpp Loaded** is on, and that the Setup tab's **This Machine** says the GPU. Lower steps while iterating. |
| A MetaHuman, CC or Mixamo character isn't in the Retarget menu | It must be a skeletal mesh in your project's Content folder. MetaHumans are found by their body mesh; CC and Mixamo by their bone names. Otherwise set it as the Target Skeletal Mesh in Details. |

## More guides and help

The guides are in the plugin's Docs folder and on the docs site (https://pr3vail.github.io/MotionForge-Docs/).

- [Prompting Guide](prompting-guide.md): prompt patterns that work, by kind of motion, with durations and settings.
- [Characters Guide](characters-guide.md): getting clips onto MetaHumans, Character Creator, Mixamo and your own
  characters, and playing them.
- [MetaHuman Guide](metahuman-guide.md): a MetaHuman from retarget to playable, with Level Target and Merge Body + Garments.
- [Sequencer Guide](sequencer-guide.md): the MotionForge track, generating between poses and Control Rig keys, and
  chaining clips.
- Questions and bug reports: **support@pr3vailco.com**, or the Pr3vail Discord at
  **https://discord.gg/4ChPb2gZey**. For a generation problem, include what the Setup tab's **Check
  Setup** reports.
