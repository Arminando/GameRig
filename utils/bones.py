import bpy

from rigify.utils.bones import BoneUtilityMixin

class BoneUtilityMixin(BoneUtilityMixin):

    def parent_to_def(self, bone_name):
        """Check if parent has associated DEF bone and if so parent this DEF to that one to make a single DEF hierarchy"""
        parent_bone = self.get_bone_parent(bone_name)
        if parent_bone:
            parents_def_bone = self.obj.pose.bones[parent_bone].rigify_associated_def
            if parents_def_bone:
                self.set_bone_parent(bone_name, parents_def_bone)

    def write_def_name(self, obj, org_name, bone_name):
        """Write the associated DEF bone into the custom rigify_associated_def property so it can be found easily later for single DEF hierarchy parenting"""
        obj.pose.bones[org_name].rigify_associated_def = bone_name