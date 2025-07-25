import bpy


class POSE_OT_gamerig_make_game_ready(bpy.types.Operator):
    """Replaces metarig types with game rig types"""

    bl_idname = "pose.gamerig_make_game_ready"
    bl_label = "Make GameRig Ready"
    bl_description = 'Changes non GameRig metarig types to GameRig types on the active metarig armature'
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE' and context.active_object.data.get("rig_id") is None
    
    def execute(self, context):
        obj = context.object
        for bone in obj.pose.bones:
            rig_type = bone.rigify_type
            if rig_type and "game" not in rig_type:
                if "game." + rig_type in context.window_manager.rigify_types:
                    bone.rigify_type = "game." + rig_type
        return {'FINISHED'}


# =============================================
# Registration

classes = (
    POSE_OT_gamerig_make_game_ready,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)