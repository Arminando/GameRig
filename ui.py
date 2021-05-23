import bpy
import addon_utils

from rigify import rig_lists
from rigify.utils.errors import MetarigError
from rigify.ui import build_type_list
from rigify import feature_set_list

from .gamerig_generate import generate_rig
from .utils.ui import is_gamerig_metarig


def draw_gamerig_rigify_button(self, context):
    layout = self.layout
    obj = context.object

    if not is_gamerig_metarig(context.object) or obj.mode=='EDIT':
        return

    if obj.mode not in {'POSE', 'OBJECT'}:
        return
        
    layout.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')

    draw_gamerig_generate_settings(self, context)

def draw_gamerig_generate_settings(self, context):
    #self.layout.label(text="test")
    pass
    #for adding custom UI stuff after the Generate Button


class VIEW3D_PT_gamerig_buttons(bpy.types.Panel):
    bl_label = "GameRig"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GameRig'

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE' and context.active_object.data.get("rig_id") is None

    def draw(self, context):
        C = context
        layout = self.layout
        obj = context.object
        id_store = C.window_manager

        layout.use_property_split = True
        layout.use_property_decorate = False

        if obj.mode in {'POSE', 'OBJECT'}:
            armature_id_store = C.object.data

            has_non_game_rigs = False

            for b in obj.pose.bones:
                if b.rigify_type and "game" not in b.rigify_type:
                    has_non_game_rigs = True

            if has_non_game_rigs:
                layout.label(text="Non Game types detected", icon='ERROR')

            row = layout.row()
            # Rig type field

            col = layout.column(align=True)
            col.active = (not 'rig_id' in C.object.data)

            layout.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')

            col = layout.column(align=True)
            col.separator()
            row = col.row(align=True)
            row.prop(armature_id_store, "rigify_generate_mode", expand=True, text="Mode")

            col = layout.column()
            col.prop(armature_id_store, "rigify_rig_basename", text="Rig Name", icon="SORTALPHA")
            if armature_id_store.rigify_generate_mode == "overwrite":
                col.prop(armature_id_store, "rigify_target_rig", text="Target Rig")
                col.prop(armature_id_store, "rigify_rig_ui", text="Target UI", icon='TEXT')
                col.prop(armature_id_store, "rigify_force_widget_update")

        elif obj.mode == 'EDIT':
            # Build types list
            build_type_list(context, id_store.rigify_types)

            if id_store.rigify_active_type > len(id_store.rigify_types):
                id_store.rigify_active_type = 0

            # Rig type list
            if len(feature_set_list.get_installed_list()) > 0:
                col = layout.column()
                col.prop(context.object.data, "active_feature_set")

            col.template_list("UI_UL_list", "rigify_types", id_store, "rigify_types", id_store, 'rigify_active_type')

            props = layout.operator("armature.metarig_sample_add", text="Add sample")
            props.metarig_type = id_store.rigify_types[id_store.rigify_active_type].name


classes = [
    VIEW3D_PT_gamerig_buttons,
]


def register():
    from bpy.utils import register_class

    bpy.types.DATA_PT_rigify_buttons.prepend(draw_gamerig_rigify_button)

    # Classes.
    for c in classes:
        register_class(c)

    

def unregister():
    from bpy.utils import unregister_class

    bpy.types.DATA_PT_rigify_buttons.remove(draw_gamerig_rigify_button)

    # Classes.
    for c in classes:
        unregister_class(c)
