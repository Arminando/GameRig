import bpy

from rigify.rigs.basic.raw_copy import Rig as raw_copy
from rigify.rigs.basic.raw_copy import create_sample as orig_create_sample
from ....utils.bones import BoneUtilityMixin

class Rig(BoneUtilityMixin, raw_copy):

    def parent_bones(self):
        super().parent_bones()
        bone_name = self.bones.org
        if "DEF-" in bone_name:
            # self.clean_def_hierarchy(self.bones.org)
            old_parent = self.get_bone_parent(bone_name)
            if old_parent:
                target = self.find_derived_def_target(old_parent)
                if target:
                    self.set_bone_parent(bone_name, target)
                else:
                    self.generator.disable_auto_parent(bone_name)
            else:
                self.generator.disable_auto_parent(bone_name)

def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    bones = orig_create_sample(obj)

    pbone = obj.pose.bones[bones['DEF-bone']]
    pbone.rigify_type = 'game.basic.raw_copy'

    return bones