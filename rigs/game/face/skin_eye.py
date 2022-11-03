import bpy
import math

from ..skin.skin_rigs import BaseSkinRig
from rigify.rigs.face.skin_eye import Rig as skin_eye
from rigify.rigs.face.skin_eye import create_sample as old_create_sample
from rigify.base_rig import stage


class Rig(BaseSkinRig, skin_eye):

    @stage.parent_bones
    def parent_deform_chain(self):
        deform = self.bones.deform
        self.set_bone_parent(deform.master, self.bones.org)

        self.clean_def_hierarchy(deform.master)

        if self.params.make_deform:
            self.set_bone_parent(deform.eye, self.bones.mch.master)
            self.set_bone_parent(deform.iris, deform.eye)

            self.clean_def_hierarchy(deform.eye)

    @stage.rig_bones
    def rig_deform_chain(self):
        super().rig_deform_chain()
        if hasattr(self.bones.deform, 'eye'):
            self.make_constraint(self.bones.deform.eye, 'COPY_LOCATION', self.bones.mch.master)
            self.make_constraint(self.bones.deform.eye, 'COPY_ROTATION', self.bones.mch.master)


def create_sample(obj):
    bones = old_create_sample(obj)

    pbone = obj.pose.bones[bones['lid1.B.L']]
    pbone.rigify_type = 'game.skin.stretchy_chain'

    pbone = obj.pose.bones[bones['lid1.T.L']]
    pbone.rigify_type = 'game.skin.stretchy_chain'

    pbone = obj.pose.bones[bones['eye.L']]
    pbone.rigify_type = 'game.face.skin_eye'