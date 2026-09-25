---
title: Prompting Guide
---

How to write prompts that give you usable motion first time. The short version is in the User Guide's
*Writing prompts* section; this page goes further, with patterns by kind of motion.

## How the model reads a prompt

Kimodo was trained on motion-capture clips with plain descriptions of what the body does. It
understands **bodies and movements**, not stories, moods or objects. So:

- Say **who moves**: start with "a person".
- Say **which part** moves and **which side**: "the right arm", "the left foot".
- Say **how**: speed, size and direction ("slowly", "a small step", "forward and to the left").
- Say **what the feet do**, because they decide whether the character travels, turns or stays put.
- Leave out names, props and places. "Swings a sword" is fine (it knows the arm motion); the sword itself
  is a preview prop you add afterwards.

One action per segment. Two actions in one sentence tend to blur into a mix of both; give each its own
segment on the timeline.

## Durations

Kimodo fills the time you give it. Too long and the action finishes early and drifts; too short and it
gets rushed or cut off.

| Motion | Duration |
|---|---|
| Punch, jab, quick gesture | 1 - 1.5 s |
| Kick, sword swing, throw | 1.5 - 2 s |
| Wave, nod, point | 1.5 - 2.5 s |
| Walk or run cycle | 2 - 3 s |
| Jump and land | 1.5 - 2.5 s |
| Turn on the spot | 1.5 - 2 s |
| Sit down, stand up, lie down | 3 - 5 s |
| Idle, breathing, looking around | 3 - 6 s |

With the kimodo.cpp backend each segment can be at most 10 seconds.

## Patterns that work

### Locomotion

- a person walks forward at a normal pace, arms swinging naturally
- a person jogs forward, then slows to a walk
- a person walks forward slowly and cautiously, crouched low, looking left and right
- a person strafes to the left with small side steps, facing forward
- a person walks backward slowly
- a person runs forward fast and stops suddenly

For a looping cycle, generate 3 s, trim the export range to one clean stride pair, and use **Make
Loop**.

### Turns and starts

- a person turns 90 degrees to the right on the spot
- a person turns around to face the other way and starts walking
- a person standing still starts walking forward

### Combat

- a person throws a straight punch forward with the right fist, then pulls back into a guard
- a person swings a heavy two-handed sword down from over the right shoulder in a fast diagonal arc
- a person raises the right knee and drives a straight kick forward at waist height, then plants the foot
- a person dodges quickly to the left, ducking the head
- a person staggers backward as if hit in the chest, then regains balance

### Idles and emotes

- a person stands still, breathing, shifting weight from one foot to the other
- a person waves hello with the right hand above the head
- a person claps both hands in front of the chest
- a person shrugs both shoulders with the palms turned up
- a person cheers with both arms raised above the head

### Interactions with the world (use a preview mesh)

The model doesn't know the object is there, so it only gets the body right. Add the object as a
**Preview Scene Mesh** and pose the contact with a key if needed.

- a person sits down slowly on a chair behind them (Preview Scene Mesh: a chair)
- a person bends down and picks something up from the floor with both hands
- a person pushes forward with both hands at chest height (a door, a crate)
- a person climbs up onto a ledge at waist height

## Chaining segments

Several segments make one continuous clip, and the model writes the transition between them. Keep
each transition physically possible:

| Segment | Prompt | Duration |
|---|---|---|
| 1 | a person walks forward | 2 s |
| 2 | the person stops and waves with the right hand | 2 s |
| 3 | the person turns around and walks back | 2.5 s |

Going from lying down to sprinting needs a bridge in between ("the person pushes up to standing").
If a transition pops, raise **Transition Cfg Weight**; if it looks forced, lower it.

## Using seeds, samples and guidance

1. Write the prompt and set **Samples** to 3-4 with **Diffusion Steps Override** at 10-20. After the
   first take, repeat takes of the same prompt are much faster (the model remembers the prompt).
2. Pick the best take from **Takes** and use **Pin This Take's Seed**.
3. With the seed pinned, change **one** thing at a time: a word in the prompt, the duration, or the
   guidance.
4. Set Samples back to 1 and steps back up (or 0 for the global default) for the final clip.

| Setting | Raise it when | Lower it when |
|---|---|---|
| Text Cfg Weight (2.0) | The prompt is ignored | The motion looks stiff or robotic |
| Transition Cfg Weight (2.0) | Transitions pop | Transitions look forced |

## When a prompt doesn't work

| You see | Try |
|---|---|
| A different action from the one asked for | Describe it in body terms, one limb at a time |
| Barely moves | Shorter duration; say what the feet do |
| Drifts after the action | Shorter duration, or trim the export range |
| Two actions blended into one | Split them into two segments |
| Wrong hand or foot | Name the side: "with the left hand" |
| Right idea, clumsy execution | More Samples; it varies between seeds |
