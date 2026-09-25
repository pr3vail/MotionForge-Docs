---
title: Characters Guide
---

MotionForge generates onto its own bundled skeleton, then retargets the clip onto your character
through Unreal's IK Retargeter. This page covers each kind of character and how to play the result.

## Which characters work in one click

Open the recipe editor's **Retarget** menu, or right-click clips in the Content Browser and choose
**MotionForge > Retarget To**. The list shows:

| Character | When it's listed | Notes |
|---|---|---|
| Base Male / Base Female (MotionForge) | Always; they ship with the plugin | Free to use in your game |
| UE5 Manny / Quinn | Epic's Mannequins Asset Pack or the Third Person template is in your project | Add them from **Window > Fab** (free) |
| UEFN Mannequin | Epic's Game Animation Sample content is in your project | |
| MetaHuman: *name* | A MetaHuman body is in your project | See below |
| Character Creator: *name* | A CC3/CC4 character imported as a skeletal mesh | Found by its `CC_Base_` bones |
| Mixamo: *name* | A Mixamo-rigged character imported as a skeletal mesh | Found by its bone names (`Hips`, `LeftUpLeg`...) |

Up to 12 MetaHuman, CC and Mixamo characters are listed. Anything else humanoid works through
**Details > Retarget > Target Skeletal Mesh**, then **Retarget > Target Skeletal Mesh**.

The first retarget onto a character builds an IK Rig for it (chains only, next to the result) and an
IK Retargeter with a pose called **AlignedToSource** that lines the character's arms and legs up with
MotionForge's T-pose. Later retargets reuse both, and any change you make to that pose in the IK
Retargeter editor is kept.

## MetaHumans

1. Add the MetaHuman to your project (MetaHuman Creator, or Quixel Bridge for older ones). Its body
   mesh, skinned to `metahuman_base_skel`, is what MotionForge lists.
2. **Retarget > MetaHuman: *name***. The clip is saved next to the body mesh.
3. To play it, open the MetaHuman's Blueprint (`BP_<name>`), select the **Body** component and set
   **Animation Mode** to *Use Animation Asset* with the clip, or drop the clip into a Level Sequence on
   the MetaHuman's Body track. The face and clothing follow the body.

Retargeted MetaHuman clips carry root motion the same way as any other export (see the User Guide's
*Exporting* section).

## Character Creator (CC3 / CC4)

Export from Character Creator as FBX with the **Unreal** preset and import it as a skeletal mesh. If
you exported with Reallusion's "UE skeleton" naming, the character uses Epic's bone names and works
like Manny instead.

## Mixamo

Download the character from Mixamo as FBX (**T-pose**, with skin) and import it as a skeletal mesh.
Unreal drops Mixamo's `mixamorig:` prefix on import, so the bones arrive as `Hips`, `Spine`,
`LeftUpLeg` and so on. MotionForge recognises both forms.

## Your own characters

Any humanoid skeletal mesh with a recognisable spine, two arms and two legs works through **Target
Skeletal Mesh**. If MotionForge reports that the skeleton "doesn't match a known humanoid template",
Unreal couldn't identify the limbs from the bone names. Create an IK Rig for it once
(**Window > Animation > IK Rig Editor**: one retarget chain each for spine, head, both arms and both
legs, plus a retarget root on the pelvis). MotionForge then uses it.

## Checking a retarget

Look at the result on the character, not in the animation editor:

- **Facing**: walks the way the character faces.
- **Feet**: on the ground, not floating or sinking.
- **Travel**: a walk still moves forward (with root motion on, the capsule should follow).
- **Wrists and fingers**: natural. If the arms look too high or too low, adjust **AlignedToSource**
  in the IK Retargeter (`RTG_...` next to the result).

Fix motion problems at the source (the prompt or a pose key), not in the retarget.
