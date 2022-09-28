import bpy

from rigify.rigs.skin.anchor import Rig as anchor
from .skin_rigs import BaseSkinChainRigWithRotationOption
from rigify.base_rig import stage


class Rig(BaseSkinChainRigWithRotationOption, anchor):

    @stage.parent_bones
    def parent_deform_chain(self):
        if self.make_deform:
            self.set_bone_parent(self.bones.deform, self.rig_parent_bone)
            self.clean_def_hierarchy(self.bones.deform)
    
    @stage.rig_bones
    def rig_deform_bone(self):
        self.make_constraint(self.bones.deform, 'COPY_LOCATION', self.bones.org)
        self.make_constraint(self.bones.deform, 'COPY_ROTATION', self.bones.org)


def create_sample(obj):
    from ..basic.super_copy import create_sample as inner
    obj.pose.bones[inner(obj)["Bone"]].rigify_type = 'game.skin.anchor'
