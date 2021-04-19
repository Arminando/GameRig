import bpy
import addon_utils

from rigify import rig_lists
from rigify.utils.errors import MetarigError
from .gamerig_generate import generate_rig
from .utils.ui import is_gamerig_metarig


"""
#not used, delete later
def draw_gamerig_rigify_buttons(self, context):
    layout = self.layout
    obj = context.object

    if not is_gamerig_metarig(context.object) or obj.mode=='EDIT':
        self.draw_old(context)
        return

    if obj.mode not in {'POSE', 'OBJECT'}:
        return

    layout.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')

    draw_gamerig_generate_settings(self, context)
"""


def draw_gamerig_rigify_button(self, context):
    layout = self.layout
    obj = context.object

    if not is_gamerig_metarig(context.object) or obj.mode=='EDIT':
        self.draw_old(context)
        return

    if obj.mode not in {'POSE', 'OBJECT'}:
        return
        
    layout.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')

    draw_gamerig_generate_settings(self, context)

def draw_gamerig_generate_settings(self, context):
    #self.layout.label(text="test")
    pass
    #for adding custom UI stuff after the Generate Button

classes = [

]


def register():
    from bpy.utils import register_class

    # Classes.
    for c in classes:
        register_class(c)

    # Hijack Rigify panels' draw functions.
    #bpy.types.DATA_PT_rigify_buttons.draw_old = bpy.types.DATA_PT_rigify_buttons.draw
    #bpy.types.DATA_PT_rigify_buttons.draw = draw_gamerig_rigify_buttons

    bpy.types.DATA_PT_rigify_buttons.prepend(draw_gamerig_rigify_button)

def unregister():
    from bpy.utils import unregister_class

    # Classes.
    for c in classes:
        unregister_class(c)

    # Restore Rigify panels' draw functions.
    #bpy.types.DATA_PT_rigify_buttons.draw = bpy.types.DATA_PT_rigify_buttons.draw_old
    bpy.types.DATA_PT_rigify_buttons.remove(draw_gamerig_rigify_button)