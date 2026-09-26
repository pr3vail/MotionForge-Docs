---
title: Sequencer Guide
---

How to generate motion right in a Level Sequence, between the poses already there, and finish it
by hand.

## The MotionForge track

A MotionForge track holds **shots**. A shot is a prompt over a stretch of time on one character.
When you generate a shot, MotionForge:

1. reads the pose the character is in just before the shot, and the pose at the shot's end, from
   whatever plays there: animation clips, or a Control Rig track keyed by hand;
2. pins those poses as constraints, generates the prompt over the shot's length, and retargets the
   take onto the character if needed;
3. puts the take on the character's animation track at the shot's start.

The track itself plays nothing. The take is an ordinary animation section, and the MotionForge track
is removed when the sequence is cooked for a game.

### Add a shot

1. Open a Level Sequence with a character in it (a skeletal mesh actor, a MetaHuman, or a Blueprint
   with a skeletal mesh).
2. Put the playhead where the new motion should start.
3. On the character's row, click **+ Track** and choose **MotionForge**. This adds a 4-second shot and
   opens its prompt.
4. Type what happens, one line per segment. `| 2s` sets a line's length, and lines without one share
   the rest of the shot. Then click **Save and Generate**.

Drag the shot's edges to change its length before generating: the end pose is read where the shot
ends. Several shots can share a track, each on its own row when they overlap.

### Generate, and generate again

Right-click a shot:

| Entry | What it does |
|---|---|
| **Generate** | Generates the shot. Generating again replaces this shot's last take on the animation track (the old clip stays in the Content Browser). |
| **Edit Prompt...** | Changes the prompt, then generates. |
| **Open Recipe** | Opens the recipe the last Generate made (`/Game/MotionForge/Sequencer/<Sequence>/R_Shot...`) in MotionForge's full editor, to refine the take with keys, constraints or props. |
| **Properties** | Sequencer's own panel for the shot's settings (below). |

Generation runs in the background, so you can keep working. The Jobs tab shows progress, and the
shot's tooltip shows what the last Generate did.

### Shot settings (right-click > Properties)

| Setting | Default | What it does |
|---|---|---|
| **Prompt** | | What the character does. |
| **Seed** | -1 | -1 gives a new take each time; set a number to repeat one. |
| **Takes** | 1 | Takes to generate. The last goes on the track, and the others stay in the Content Browser. |
| **Start From Pose** | on | Starts from the pose just before the shot. |
| **Hit End Pose** | on | Ends in the pose at the shot's end. |
| **Mute Overlapped** | on | Mutes older animation sections the take overlaps, rather than deleting them. |

A pose is only pinned when something plays there. A shot after the last clip, with no Control Rig
keys, pins only its start, and the shot's tooltip says so.

### How poses become pins

- **On MotionForge's own skeleton,** the exact pose becomes one **Full Body** pin.
- **On any other humanoid** (Manny, Quinn, MetaHumans, Character Creator, Mixamo, your own), the
  pose becomes a **Root Path** pin plus **both hands and both feet**. They are placed on MotionForge's
  skeleton, scaled to the character's height and turned to face its way. The model then fills in
  the body around those five points.

In testing, pins read from a clip and from a baked Control Rig both matched the pose playing there
to within 0.01 cm. On the Base Male, hands and feet landed within 0.4 cm of the character's own.

## Key a pose, then generate into it

This is the main Control Rig workflow:

1. Put the character on a Control Rig track: **MotionForge > Bake Selected to Control Rig** on the
   Sequencer toolbar, or Sequencer's own **Add Control Rig**.
2. At the frame where the move must land, key the pose by hand: a hand on a door handle, a foot on
   a step.
3. Add a MotionForge shot that ends on that frame, type the prompt ("a person walks to the door and
   opens it") and generate.

The take starts from what plays before the shot and lands in your keyed pose. Keep refining the take
on the Control Rig track, or open the shot's recipe.

## The Sequencer toolbar menu

Sequencer's toolbar has a **MotionForge** menu:

- **Generate on Selected Character...** is the quick version of a shot. Select the character, put
  the playhead where the motion should start, and type the prompt. **Start from the pose playing
  here** continues from the MotionForge clip under the playhead.
- **Add Prompt Subtitles** shows each MotionForge clip's prompt over the character while it plays.
- **Bake Selected to Control Rig** turns the selected character's animation into an FK Control Rig
  track, so any joint can be keyed by hand. The animation track it came from is muted, not deleted.
- **Open Jobs** opens the Jobs tab.

## Chain clips into a sequence

Right-click clips in the Content Browser and choose **MotionForge > Chain into Level Sequence...**.
MotionForge builds a new sequence that plays the clips back to back on one character, in the order
you selected them. Each clip starts where the last one ended, facing the same way, and neighbouring
clips blend over **Blend frames**. Add MotionForge shots between them to generate the in-betweens.

## Tips

- Short shots (1-4 s) with one clear action per line steer best.
- Use a shot's **Hit End Pose** to land on the next clip's first frame: the in-between then flows
  into it without a pop.
- To match an exact hand or foot placement, generate, then open the recipe and add a pin, or place
  the pin on the character in the level with **Level Target** (User Guide, *Constraints*).
- Retargeted takes use the character's IK Retargeter. See [Characters Guide](characters-guide.md) for tuning it.
