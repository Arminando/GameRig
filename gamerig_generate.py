import bpy

from rigify.generate import Generator
from rigify.utils.rig import get_rigify_type
from rigify.utils.naming import make_original_name

class Generator_gamerig(Generator):

    def _Generator__rename_org_bones(self, obj):
        #----------------------------------
        # Make a list of the original bones so we can keep track of them.
        original_bones = [bone.name for bone in obj.data.bones]

        # Add the ORG_PREFIX to the original bones.
        for i in range(0, len(original_bones)):
            bone = obj.pose.bones[original_bones[i]]

            # This rig type is special in that it preserves the name of the bone.
            if get_rigify_type(bone) not in ('basic.raw_copy', 'game.raw_copy'):
                bone.name = make_original_name(original_bones[i])
                original_bones[i] = bone.name

        self.original_bones = original_bones
        

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



classes = [
    
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
