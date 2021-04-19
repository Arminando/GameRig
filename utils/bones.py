import bpy

from rigify.utils.bones import BoneUtilityMixin

class BoneUtilityMixin(BoneUtilityMixin):

    def clean_def_hierarchy(self, bone_name):
        old_parent = self.get_bone_parent(bone_name)
        if old_parent:
            target = self.find_relink_target('DEF', old_parent)
            if target:
                self.set_bone_parent(bone_name, target)
            else:
                self.remove_bone_parent(bone_name)
                self.generator.disable_auto_parent(bone_name)

    def remove_bone_parent(self, bone_name):
        print(bone_name)
        eb = self.obj.data.edit_bones
        bone = eb[bone_name]
        bone.parent = None