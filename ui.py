import bpy

from rigify.ui import DATA_PT_rigify
from rigify.utils.misc import verify_armature_obj
from rigify.utils.rig import get_rigify_type

from .utils.ui import is_gamerig_metarig
from .operators.upgrade_metarig_types import outdated_types as outdated_game_types

def draw_gamerig_rigify_button(self, context):
    C = context

    layout = self.layout
    obj = verify_armature_obj(C.object)


    if not is_gamerig_metarig(context.object):
        return
        
    layout.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')


    show_upgrade_game_face = False
    show_upgrade_game_types = False

    old_rig = ''
    old_bone = ''

    for b in obj.pose.bones:
        old_rig = get_rigify_type(b)
        if b.rigify_type == 'game.faces.super_face':
            show_upgrade_game_face = True
        elif b.rigify_type in outdated_game_types.keys():
            show_upgrade_game_types = True

    if show_upgrade_game_face:
        layout.label(text="This metarig uses the old game face rig.", icon='INFO')
        layout.operator("pose.gamerig_upgrade_game_face")
    if show_upgrade_game_types:
        layout.label(text="This metarig uses the old game types.", icon='ERROR')
        layout.operator("pose.gamerig_upgrade_types")

    armature_id_store = C.object.data

    has_non_game_rigs = False
    is_game_metarig = is_gamerig_metarig(obj)

    for b in obj.pose.bones:
        if b.rigify_type and "game" not in b.rigify_type:
            has_non_game_rigs = True
            break

    if has_non_game_rigs and is_game_metarig:
        layout.label(text="Non Game types detected", icon='ERROR')


class VIEW3D_PT_gamerig_preferences(bpy.types.Panel):
    bl_label = "Game Rig Preferences"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_parent_id = 'DATA_PT_rigify'
    bl_options = {'DEFAULT_CLOSED'}
    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE' and context.active_object.data.get("rig_id") is None

    def draw(self, context):
        C = context
        armature_id_store = C.object.data
        id_store = C.window_manager


        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.operator("pose.gamerig_make_game_ready", text="Make GameRig Ready", icon='CHECKMARK')
        layout.separator()

        layout.prop(armature_id_store, "gameRig_force_generator", text="Force Generator", expand=True)
        layout.separator()

        split = layout.row().split(factor=0.4)
        split.label(text='')
        split.operator("script.reload", text="Reload Scripts", icon='FILE_REFRESH')
        

classes = [
    VIEW3D_PT_gamerig_preferences,
]


def register():
    from bpy.utils import register_class

    bpy.types.DATA_PT_rigify.prepend(draw_gamerig_rigify_button)

    # Classes.
    for c in classes:
        register_class(c)

    

def unregister():
    from bpy.utils import unregister_class

    bpy.types.DATA_PT_rigify.remove(draw_gamerig_rigify_button)

    # Classes.
    for c in classes:
        unregister_class(c)
