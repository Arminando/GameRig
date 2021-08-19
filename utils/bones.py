import bpy

from rigify.utils.bones import BoneUtilityMixin
from rigify.utils.naming import choose_derived_bone


class BoneUtilityMixin(BoneUtilityMixin):

    def clean_def_hierarchy(self, bone_name):
        old_parent = self.get_bone_parent(bone_name)
        if old_parent:
            target = self.find_derived_def_target(old_parent)
            if target:
                self.set_bone_parent(bone_name, target)
            else:
                self.remove_bone_parent(bone_name)
                self.generator.disable_auto_parent(bone_name)
        else:
            self.generator.disable_auto_parent(bone_name)

    def find_derived_def_target(self, old_target):
        result = None
        while old_target:
            result = choose_derived_bone(self.generator, old_target, 'def')
            if result:
                break
            else:
                old_target = self.get_bone_parent(old_target)
        return result


    def remove_bone_parent(self, bone_name):
        eb = self.obj.data.edit_bones
        bone = eb[bone_name]
        bone.parent = None

    
    def remove_quat_rot_mode(self, controls: dict):
        for key in controls:
            item = controls[key]

            if isinstance(item, dict):
                self.remove_quat_rot_mode(item)
            else:
                if isinstance(item, str):
                    item = [item]

                for bone in item:
                    bone_obj = self.get_bone(bone)
                    if bone_obj.rotation_mode == 'QUATERNION':
                        bone_obj.rotation_mode = 'XYZ'