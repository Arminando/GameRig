import bpy
import addon_utils

from rigify import rig_lists
from rigify.utils.errors import MetarigError
from .gamerig_generate import generate_rig

class GAMERIG_OT_generate(bpy.types.Operator):
    """Generates a rig from the active metarig armature"""

    bl_idname = "pose.rigify_generate"
    bl_label = "GameRig Generate Rig"
    bl_options = {'UNDO'}
    bl_description = 'Generates a rig from the active metarig armature'

    def execute(self, context):
        try:
            generate_rig(context, context.object)
        except MetarigError as rig_exception:
            import traceback
            traceback.print_exc()

            rigify_report_exception(self, rig_exception)
        except Exception as rig_exception:
            import traceback
            traceback.print_exc()

            self.report({'ERROR'}, 'Generation has thrown an exception: ' + str(rig_exception))
        finally:
            bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


def draw_gamerig_rigify_buttons(self, context):
    self.layout.operator("pose.gamerig_generate", text="Generate GameRig", icon='POSE_HLT')


def draw_gamerig_generate_settings(self, context):
    #self.layout.label(text="test")
    pass
    #for adding custom UI stuff after the Generate Button
    


classes = [
    GAMERIG_OT_generate
]

def register():
    from bpy.utils import register_class

    # Classes.
    for c in classes:
        register_class(c)

    bpy.types.DATA_PT_rigify_buttons.append(draw_gamerig_generate_settings)



def unregister():
    from bpy.utils import unregister_class

    # Classes.
    for c in classes:
        unregister_class(c)

    bpy.types.DATA_PT_rigify_buttons.remove(draw_gamerig_generate_settings)