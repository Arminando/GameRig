import bpy

from rigify.utils.bones import new_bone
from rigify.generate import Generator, get_xy_spread
from rigify.utils.rig import get_rigify_type
from rigify.utils.naming import make_original_name, ROOT_NAME
from rigify.ui import rigify_report_exception
from rigify.utils.errors import MetarigError
from rigify.rig_lists import get_rigs
from rigify.rig_lists import rigs


class Generator_gamerig(Generator):
    
    # Removing this for now as it creates an error if the metarig is called 'Armature'
    # def __init__(self, context, metarig):
    #     super().__init__(context, metarig)
    #     if not metarig.data.rigify_rig_basename:
    #         metarig.data.rigify_rig_basename = "Armature"

    # Added this just to make game.raw_copy work, which is identical to raw_copy
    def _Generator__rename_org_bones(self, obj):
        # Make a list of the original bones, so we can keep track of them.
        original_bones = [bone.name for bone in obj.data.bones]

        # Add the ORG_PREFIX to the original bones.
        for i in range(0, len(original_bones)):
            bone = obj.pose.bones[original_bones[i]]

            # Preserve the root bone as is if present
            if bone.name == ROOT_NAME:
                if bone.parent:
                    raise MetarigError('Root bone must have no parent')
                if get_rigify_type(bone) not in ('', 'basic.raw_copy'):
                    raise MetarigError('Root bone must have no rig, or use basic.raw_copy')
                continue

            # This rig type is special in that it preserves the name of the bone.
            if get_rigify_type(bone) not in ('basic.raw_copy', 'game.basic.raw_copy'):

                bone.name = make_original_name(original_bones[i])
                original_bones[i] = bone.name

        self.original_bones = original_bones

    
    def _Generator__create_root_bone(self):
        obj = self.obj
        metarig = self.metarig

        #----------------------------------
        # Create the root bone.
        root_bone = new_bone(obj, ROOT_NAME)
        spread = get_xy_spread(metarig.data.bones) or metarig.data.bones[0].length
        spread = float('%.3g' % spread)
        scale = spread/0.589
        obj.data.edit_bones[root_bone].head = (0, 0, 0)
        obj.data.edit_bones[root_bone].tail = (0, scale, 0)
        obj.data.edit_bones[root_bone].roll = 0
        self.root_bone = root_bone
        self.bone_owners[root_bone] = None

        # Only this line changed. The rest is a straight copy from Generator
        bpy.ops.object.mode_set(mode='POSE')
        obj.pose.bones[root_bone].rotation_mode = 'XYZ'
        bpy.ops.object.mode_set(mode='EDIT')

    def _Generator__lock_transforms(self):
        super()._Generator__lock_transforms()

        # Unlock on DEF- bones
        for pb in self.obj.pose.bones:
            if "DEF-" in pb.name:
                pb.lock_location = (False, False, False)
                pb.lock_rotation = (False, False, False)
                pb.lock_rotation_w = False
                pb.lock_scale = (False, False, False)

        
# Part of the execute function for the class below
def generate_rig(context, metarig):
    """ Generates a rig from a metarig.

    """
    # Initial configuration
    rest_backup = metarig.data.pose_position
    metarig.data.pose_position = 'REST'

    try:
        Generator_gamerig(context, metarig).generate()

        metarig.data.pose_position = rest_backup

    except Exception as e:
        # Cleanup if something goes wrong
        print("Rigify: failed to generate rig.")

        bpy.ops.object.mode_set(mode='OBJECT')
        metarig.data.pose_position = rest_backup

        # Continue the exception
        raise e


class GAMERIG_OT_generate(bpy.types.Operator):
    """Generates a rig from the active metarig armature"""

    bl_idname = "pose.gamerig_generate"
    bl_label = "GameRig Generate Rig"
    bl_options = {'UNDO'}
    bl_description = 'Generates a rig from the active metarig armature'

    def execute(self, context):

        self.make_game_ready(context)

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
    
    def make_game_ready(self, context):
        rigs_list = list(rigs.keys())
        for bone in context.object.pose.bones:
            if bone.rigify_type == "":
                continue

            if "game" not in bone.rigify_type:
                if "game." + bone.rigify_type in rigs_list:
                    bone.rigify_type = "game." + bone.rigify_type
                else:
                    print("GameRig: Bone", bone.name, bone.rigify_type, "could not convert to GameRig type.")


classes = [
    GAMERIG_OT_generate,
]

def register():
    from bpy.utils import register_class
    for c in classes:
        print("registering", c)
        register_class(c)

def unregister():
    from bpy.utils import unregister_class
    for c in classes:
        unregister_class(c)
