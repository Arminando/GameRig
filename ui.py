import bpy
import addon_utils

from rigify import rig_lists

class GAMERIG_OT_generate(bpy.types.Operator):
    """Generates a rig from the active metarig armature"""

    bl_idname = "pose.gamerig_generate"
    bl_label = "GameRig Generate Rig"
    bl_options = {'UNDO'}
    bl_description = 'Generates a rig from the active metarig armature'

    def execute(self, context):
        print("test")

        return {'FINISHED'}


def draw_gamerig_rigify_buttons(self, context):
    layout = self.layout
    obj = context.object

    """
    if not is_cloud_metarig(context.object) or obj.mode=='EDIT':
        self.draw_old(context)
        return

    if obj.mode not in {'POSE', 'OBJECT'}:
        return
    """
    layout.operator("pose.gamerig_generate", text="Generate GameRig")

    draw_gamerig_generate_settings(self, context)


def draw_gamerig_generate_settings(self, context):
    pass
    #for adding custom UI stuff after the Generate Button


classes = [
    GAMERIG_OT_generate,
]

def register():
    from bpy.utils import register_class

    # Classes.
    for c in classes:
        register_class(c)

    bpy.types.DATA_PT_rigify_buttons.draw_old = bpy.types.DATA_PT_rigify_buttons.draw
    #bpy.types.DATA_PT_rigify_buttons.draw = draw_gamerig_rigify_buttons



def unregister():
    from bpy.utils import unregister_class

    # Classes.
    for c in classes:
        unregister_class(c)

    bpy.types.DATA_PT_rigify_buttons.draw = bpy.types.DATA_PT_rigify_buttons.draw_old