---
title: MetaHuman Guide
---

How to get MotionForge motion onto a MetaHuman, play it, direct it in the level and in Sequencer, and
make the MetaHuman playable. For other characters, see [Characters Guide](characters-guide.md).

## What you need

- A MetaHuman in your project. Create one in MetaHuman Creator, or add an older one from Quixel
  Bridge. MotionForge finds the **body** mesh by its `metahuman_base_skel` skeleton.
- A MotionForge take: any generated clip or export.

The face isn't animated by MotionForge. It follows the body through the MetaHuman's Blueprint, and
facial animation comes from your usual face tools.

## 1. Retarget the take onto the body

In the recipe editor, open **Retarget** and pick **MetaHuman: *name***. You can also right-click
clips in the Content Browser and choose **MotionForge > Retarget To > MetaHuman: *name***.

The first retarget sets up everything. MotionForge builds an IK Rig for the body and an IK Retargeter
with an **AlignedToSource** pose that lines up the MetaHuman's A-pose with MotionForge's T-pose.
Later retargets reuse both.

With **Auto Scale Retargets** on (Editor Preferences > Plugins > MotionForge > Export; on by
default), each retarget tries a few stride scales and keeps the one with the least foot sliding. On
a MetaHuman walk in testing, sliding dropped from 1.12 cm to 0.64 cm. The recipe editor's status
line shows the scale it chose.

The retargeted clip is saved next to the body mesh when the MetaHuman lives in `/Game`.

## 2. Clean it up (optional)

Right-click the retargeted clip and choose **MotionForge > Clean Up...**:

- **Ground Feet** and **Anchor Feet** plant the feet and stop them sliding. Where a leg is too short
  to reach, the hips drop slightly (**Lower Hips To Reach**).
- **Self Collision** keeps the arms out of the body. A MetaHuman body has a physics asset, so its own
  capsules are used, not an estimate. The report names the physics asset.

## 3. Play it

- **On the MetaHuman Blueprint:** open `BP_<name>`, select the **Body** component, set **Animation
  Mode** to *Use Animation Asset* and pick the clip. The face and clothing follow the body.
- **In the level:** select the MetaHuman in the level and click **In Level** in the recipe editor.
  The take plays on it and is retargeted first if needed.
- **In Sequencer:** add the clip to the MetaHuman's **Body** track. You can also generate straight
  onto the MetaHuman with the MotionForge track (see [Sequencer Guide](sequencer-guide.md)).

## 4. Direct it where it stands (Level Target)

To aim a reach or a step at something in your level:

1. Select the MetaHuman in the level.
2. In the recipe editor, click **Level Target**. The take plays on the MetaHuman, and every
   constraint pin gets a marker in the level: a small sphere for a hand or foot, a flat disc for a
   Root Path pin.
3. Move a marker with the normal level gizmo. The pin follows: a hand or foot pin re-solves its arm
   or leg, a Root Path pin moves the path on the ground. A marker that can't be reached snaps back
   to where the limb can get to.
4. The MetaHuman follows the recipe editor's playhead, so you can scrub to a pin's frame and check it
   against the scene.
5. Click **Level Target** again to finish, then **Generate**.

Markers are temporary. They are never saved with the level.

Pins are stored on MotionForge's skeleton and scaled to the MetaHuman's height, so what you place is
what the retargeted take aims for.

## 5. One mesh instead of body + clothing (Merge Body + Garments)

A MetaHuman is a body plus separate clothing meshes on the same skeleton. For work that wants one
mesh, you can merge them: exporting a single character, a quick level preview, or a game character
with one skeletal mesh component.

1. In the Content Browser, select the body mesh and its garment meshes (all skeletal meshes).
2. Right-click and choose **MotionForge: Merge Body + Garments**.

The result, `<Body>_Merged`, is saved next to the body. For plugin content it goes in
`/Game/MotionForge/Characters`.

It's a copy of the body with every garment's triangles, skin weights and materials added. Each
garment material gets its own slot, and the body's LODs keep their garment's matching LOD. Clothing
bones the body doesn't have are weighted to their nearest parent, and the notification says how
many. Garment morph targets and cloth simulation are not carried over.

The merged mesh uses the body's skeleton, so every retargeted clip plays on it unchanged.

## 6. Make it playable

Right-click the MetaHuman's Blueprint and choose **MotionForge > Make Playable Character...**. This
makes a character Blueprint with the MetaHuman attached to its capsule. **Make it the default pawn**
also sets up a game mode for it. See the User Guide's *In the level* section.

## When something looks wrong

| Problem | Try |
|---|---|
| Arms stick out from the body | Open the IK Retargeter (`RTG_..._to_IK_MF_<body>`) and adjust the **AlignedToSource** pose. MotionForge keeps your change. |
| Feet float or sink | Turn on **Ground Retargeted Clips** (Editor Preferences > Plugins > MotionForge > Export), or run **Clean Up** with **Ground**. |
| Feet slide | Leave **Auto Scale Retargets** on, and run **Clean Up** with **Anchor Feet**. |
| The MetaHuman isn't in the Retarget menu | Its body mesh must use `metahuman_base_skel`. The menu lists up to 12 characters. |
| Clothing pokes through after a merge | Merge only garments made for this body. MotionForge doesn't re-fit clothing. |
