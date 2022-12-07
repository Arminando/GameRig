import bpy

outdated_types = {"game.arm" : "game.limbs.arm",
                    "game.basic_spine" : "game.spines.basic_spine",
                    "game.basic_tail" : "game.spines.basic_tail",
                    "game.copy_chain" : "game.basic.copy_chain",
                    "game.front_paw" : "game.limbs.front_paw",
                    "game.leg" : "game.limbs.leg",
                    "game.paw" : "game.limbs.paw",
                    "game.pivot" : "game.basic.pivot",
                    "game.raw_copy" : "game.basic.raw_copy",
                    "game.rear_paw" : "game.limbs.rear_paw",
                    "game.simple_tentacle" : "game.limbs.simple_tentacle",
                    "game.super_copy" : "game.basic.super_copy",
                    "game.super_face" : "game.faces.super_face",
                    "game.super_finger" : "game.limbs.super_finger",
                    "game.super_head" : "game.spines.super_head",
                    "game.super_limb" : "game.limbs.super_limb",
                    "game.super_spine" : "game.spines.super_spine",
                    "game.super_palm" : "game.limbs.super_palm"}


class POSE_OT_gamerig_upgrade_gamerig_types(bpy.types.Operator):
    """Upgrades metarig bones rigify_types"""

    bl_idname = "pose.gamerig_upgrade_types"
    bl_label = "Upgrade GameRig Types"
    bl_description = 'Upgrades outdated gamerig types on the active metarig armature'
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if type(obj.data) == bpy.types.Armature:
                for bone in obj.pose.bones:
                    rig_type = bone.rigify_type
                    if rig_type in outdated_types.keys():
                        bone.rigify_type = outdated_types[rig_type]
        return {'FINISHED'}


# =============================================
# Registration

classes = (
    POSE_OT_gamerig_upgrade_gamerig_types,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)