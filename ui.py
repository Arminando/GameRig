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
            is_game_metarig = is_gamerig_metarig(obj)

            for b in obj.pose.bones:
                if b.rigify_type and "game" not in b.rigify_type:
                    has_non_game_rigs = True
                    break

            if has_non_game_rigs and is_game_metarig:
                layout.label(text="Non Game types detected", icon='ERROR')

            row = layout.row()
            # Rig type field

            col = layout.column(align=True)
            col.active = (not 'rig_id' in C.object.data)
            generator_override = armature_id_store.gameRig_force_generator
            if generator_override == 'Rigify':
                col.operator("pose.rigify_generate", text="Generate Rig", icon='POSE_HLT')
            elif generator_override == 'GameRig':
                col.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')
            elif is_game_metarig:
                col.operator("pose.gamerig_generate", text="Generate GameRig", icon='GHOST_ENABLED')
            else:
                col.operator("pose.rigify_generate", text="Generate Rig", icon='POSE_HLT')

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


class VIEW3D_PT_gamerig_layer_names(bpy.types.Panel):
    bl_label = "Layer Names"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GameRig'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE' and context.active_object.data.get("rig_id") is None

    def draw(self, context):
        layout = self.layout
        obj = context.object
        arm = obj.data

        # layout.use_property_split = True
        layout.use_property_decorate = False

        # Ensure that the layers exist
        if 0:
            for i in range(1 + len(arm.rigify_layers), 29):
                arm.rigify_layers.add()
        else:
            # Can't add while drawing, just use button
            if len(arm.rigify_layers) < 29:
                layout.operator("pose.rigify_layer_init")
                return

        # UI
        main_row = layout.row(align=True).split(factor=0.05)
        col1 = main_row.column(align=True)
        col2 = main_row.column(align=True)

        col1.label()
        for i in range(32):
            if i == 16 or i == 29:
                col1.label()
            col1.label(text=str(i))

        for i, rigify_layer in enumerate(arm.rigify_layers):
            # note: rigify_layer == arm.rigify_layers[i]
            if (i % 16) == 0:
                col = col2.column()
                if i == 0:
                    col.label(text="Top Row:")
                else:
                    col.label(text="Bottom Row:")
            if (i % 8) == 0:
                col = col2.column()
            if i != 28:
                col2_row = col2.row(align=True).split(factor=0.5)
                col2_1 = col2_row.column(align=True)
                col2_2 = col2_row.column(align=True)
                col2_3 = col2_row.column(align=True)

                row = col2_1.row(align=True)
                row.prop(rigify_layer, "name", text="")
                
                row = col2_2.row(align=True)
                row.prop(rigify_layer, "group", text=arm.rigify_colors[rigify_layer.group-1].name if rigify_layer.group != 0 else "None")

                row = col2_3.row(align=True)
                row.prop(rigify_layer, "row", text="")              
                icon = 'RESTRICT_VIEW_OFF' if arm.layers[i] else 'RESTRICT_VIEW_ON'
                row.prop(arm, "layers", index=i, text="", toggle=True, icon=icon)
                icon = 'RADIOBUT_ON' if rigify_layer.selset else 'RADIOBUT_OFF'
                row.prop(rigify_layer, "selset", text="", toggle=True, icon=icon)
            else:
                col2_row = col2.row(align=True).split(factor=0.5)
                col2_1 = col2_row.column(align=True)
                col2_2 = col2_row.column(align=True)
                col2_3 = col2_row.column(align=True)

                row = col2_1.row(align=True)
                row.prop(rigify_layer, "name", text="")

                row = col2_2.row(align=True)             
                row.prop(rigify_layer, "group", text=arm.rigify_colors[rigify_layer.group-1].name if rigify_layer.group != 0 else "None")

                row = col2_3.row(align=True)
                row.label()
                row.label()
                icon = 'RADIOBUT_ON' if rigify_layer.selset else 'RADIOBUT_OFF'
                row.prop(rigify_layer, "selset", text="", toggle=True, icon=icon)
                
        

        col = col2.column(align=True)
        col.label(text="Reserved:")
        # reserved_names = {28: 'Root', 29: 'DEF', 30: 'MCH', 31: 'ORG'}
        reserved_names = {29: 'DEF', 30: 'MCH', 31: 'ORG'} 
        
        # for i in range(28, 32):
        for i in range(29, 32):
            col2_row = col2.row(align=True).split(factor=0.5)
            col2_1 = col2_row.column(align=True)
            col2_2 = col2_row.column(align=True)
            col2_3 = col2_row.column(align=True)

            row = col2_1.row(align=True)
            row.label(text=reserved_names[i])

            row = col2_2.row(align=True)
            row.label(text="")

            row = col2_3.row(align=True).split(factor=0.4)
            row.label()
            icon = 'RESTRICT_VIEW_OFF' if arm.layers[i] else 'RESTRICT_VIEW_ON'
            row.prop(arm, "layers", index=i, text="", toggle=True, icon=icon)
            

            

class VIEW3D_PT_gamerig_bone_groups(bpy.types.Panel):
    bl_label = "Bone Groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GameRig'
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE' and context.active_object.data.get("rig_id") is None

    def draw(self, context):
        obj = context.object
        armature = obj.data
        color_sets = obj.data.rigify_colors
        idx = obj.data.rigify_colors_index

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.template_list("VIEW3D_UL_gamerig_bone_groups", "", obj.data, "rigify_colors", obj.data, "rigify_colors_index")
        col = row.column(align=True)
        col.operator("armature.rigify_bone_group_add", icon='ADD', text="")
        col.operator("armature.rigify_bone_group_remove", icon='REMOVE', text="").idx = obj.data.rigify_colors_index
        col.separator()
        col.menu("VIEW3D_MT_gamerig_bone_groups_context_menu", icon='DOWNARROW_HLT', text="")

        if obj.data.rigify_colors_index < len(obj.data.rigify_colors.items()):
            split = layout.split(factor=0.3)
            col = split.column()
            col.label(text="")
            col = split.column()

            col.prop(obj.data.rigify_colors[obj.data.rigify_colors_index], "normal", text="Colors")
            col = split.column()
            sub = col.row(align=True)
            sub.enabled = not obj.data.rigify_colors_lock  # only custom colors are editable
            sub.prop(obj.data.rigify_colors[obj.data.rigify_colors_index], "select", text="")
            sub.prop(obj.data.rigify_colors[obj.data.rigify_colors_index], "active", text="")

        layout.separator()
        box = layout.box()
        row = box.row()
        icon = 'LOCKED' if armature.rigify_colors_lock else 'UNLOCKED'
        row.prop(armature, 'rigify_colors_lock', text = 'Unified select/active colors', icon=icon)
        if armature.rigify_colors_lock:

            split = box.split(factor=0.5)
            col = split.column()
            col.label(text="")
            col = split.column()

            sub = col.row(align=True)
            sub.enabled = obj.data.rigify_colors_lock  # only custom colors are editable
            sub.prop(armature.rigify_selection_colors, 'select', text='')
            sub.prop(armature.rigify_selection_colors, 'active', text='')
            sub.operator("armature.rigify_use_standard_colors", icon='FILE_REFRESH', text='') 
            sub.operator("armature.rigify_apply_selection_colors", icon='EYEDROPPER', text='')

        box.separator()
        row = box.row()
        op = row.operator("armature.rigify_bone_group_add_theme", text="Add From Theme")
        op.theme = armature.rigify_theme_to_add
        row.prop(armature, 'rigify_theme_to_add', text = '')
        


class VIEW3D_UL_gamerig_bone_groups(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False, icon='GROUP_BONE')
        

class VIEW3D_MT_gamerig_bone_groups_context_menu(bpy.types.Menu):
    bl_label = 'Bone Groups Specials'

    def draw(self, context):
        layout = self.layout

        layout.operator("armature.rigify_add_bone_groups", text="Add Standard")
        layout.operator('armature.rigify_bone_group_remove_all')



class VIEW3D_PT_gamerig_types(bpy.types.Panel):
    bl_label = "Rig Element"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GameRig'

    @classmethod
    def poll(cls, context):
        if not context.object:
            return False
        return context.object.type == 'ARMATURE' and context.active_pose_bone\
               and context.active_object.data.get("rig_id") is None

    def draw(self, context):
        C = context
        id_store = C.window_manager
        bone = context.active_pose_bone
        rig_name = str(context.active_pose_bone.rigify_type).replace(" ", "")

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Build types list
        build_type_list(context, id_store.rigify_types)

        # Rig type field
        if len(feature_set_list.get_installed_list()) > 0:
            row = layout.row()
            row.prop(context.object.data, "active_feature_set")
        row = layout.row()
        row.prop_search(bone, "rigify_type", id_store, "rigify_types", text="Rig type")

        # Rig type parameters / Rig type non-exist alert
        if rig_name != "":
            try:
                rig = rig_lists.rigs[rig_name]['module']
            except (ImportError, AttributeError, KeyError):
                row = layout.row()
                box = row.box()
                box.label(text="ERROR: type \"%s\" does not exist!" % rig_name, icon='ERROR')
            else:
                if hasattr(rig.Rig, 'parameters_ui'):
                    try:
                        rig.Rig.parameters_ui
                    except AttributeError:
                        col = layout.column()
                        col.label(text="No options")
                    else:
                        col = layout.column()
                        col.label(text="Options:")
                        box = layout.box()
                        rig.Rig.parameters_ui(box, bone.rigify_parameters)

                if hasattr(rig.Rig, 'get_space_switch_children'):
                    children = rig.Rig.get_space_switch_children()
                    col = layout.column()
                    for child in children:
                        col.label(text=child)



class VIEW3D_PT_gamerig_preferences(bpy.types.Panel):
    bl_label = "Preferences"
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
        armature_id_store = C.object.data
        id_store = C.window_manager


        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(armature_id_store, "gameRig_force_generator", text="Force Generator")
        layout.separator()

        split = layout.row().split(factor=0.4)
        split.label(text='')
        split.operator("script.reload", text="Reload Scripts", icon='FILE_REFRESH')
        

classes = [
    VIEW3D_PT_gamerig_buttons,
    VIEW3D_PT_gamerig_types,
    VIEW3D_PT_gamerig_layer_names,
    VIEW3D_UL_gamerig_bone_groups,
    VIEW3D_PT_gamerig_bone_groups,
    VIEW3D_MT_gamerig_bone_groups_context_menu,
    VIEW3D_PT_gamerig_preferences,
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
