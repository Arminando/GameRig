import bpy
import math

from .skin_rigs import BaseSkinChainRigWithRotationOption
from rigify.rigs.skin.basic_chain import Rig as basic_chain
from rigify.base_rig import stage

class Rig(BaseSkinChainRigWithRotationOption, basic_chain):
    

    @stage.parent_bones
    def parent_deform_chain(self):
        
        self.set_bone_parent(self.bones.deform[0], self.rig_parent_bone)
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.clean_def_hierarchy(self.bones.deform[0])

    def rig_deform_bone(self, i, deform, org):
        self.make_constraint(deform, 'COPY_LOCATION', org)
        self.make_constraint(deform, 'COPY_ROTATION', org)


def create_sample(obj):
    from ..basic.copy_chain import create_sample as inner
    obj.pose.bones[inner(obj)["bone.01"]].rigify_type = 'game.skin.basic_chain'
