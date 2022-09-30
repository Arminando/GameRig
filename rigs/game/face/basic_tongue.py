import bpy

from ...chain_rigs import TweakChainRig
from rigify.base_rig import stage
from rigify.rigs.face.basic_tongue import Rig as basic_tongue
from rigify.utils.naming import make_derived_name
from rigify.utils.bones import copy_bone_position, flip_bone
from rigify.utils.layers import ControlLayersOption
from rigify.utils.misc import map_list

from rigify.rigs.widgets import create_jaw_widget

from itertools import count

class Rig(TweakChainRig, basic_tongue):


    ####################################################
    # BONES
    #
    # ctrl:
    #   master:
    #     Master control.
    # mch:
    #   follow[]:
    #     Partial follow master bones.
    #
    ####################################################

    ####################################################
    # Control chain

    @stage.generate_bones
    def make_control_chain(self):
        org = self.bones.org[-1]
        name = self.copy_bone(org, make_derived_name(org, 'ctrl'), parent=True)
        self.bones.ctrl.master = name


    @stage.parent_bones
    def parent_control_chain(self):
        self.set_bone_parent(self.bones.ctrl.master, self.get_bone_parent(self.bones.org[0]))


    @stage.configure_bones
    def configure_control_chain(self):
        master = self.bones.ctrl.master

        self.copy_bone_properties(self.bones.org[-1], master)

        ControlLayersOption.SKIN_PRIMARY.assign(self.params, self.obj, [master])


    ####################################################
    # Mechanism chain

    @stage.generate_bones
    def make_follow_chain(self):
        self.bones.mch.follow = map_list(self.make_mch_follow_bone, count(1), self.bones.org[:-1])

    def make_mch_follow_bone(self, i, org):
        name = self.copy_bone(org, make_derived_name(org, 'mch'))
        copy_bone_position(self.obj, self.bones.org[-1], name)
        return name

    @stage.parent_bones
    def parent_follow_chain(self):
        for mch in self.bones.mch.follow:
            self.set_bone_parent(mch, self.rig_parent_bone)

    @stage.rig_bones
    def rig_follow_chain(self):
        master = self.bones.ctrl.master
        num_orgs = len(self.bones.org)

        for i, mch in enumerate(self.bones.mch.follow):
            self.make_constraint(mch, 'COPY_TRANSFORMS', master, influence=(1+i)/num_orgs)

    ####################################################
    # Tweak chain

    @stage.parent_bones
    def parent_tweak_chain(self):
        ctrl = self.bones.ctrl
        parents = [self.rig_parent_bone, *self.bones.mch.follow, ctrl.master]
        for tweak, main in zip(ctrl.tweak, parents):
            self.set_bone_parent(tweak, main)


def create_sample(obj):
    from rigify.rigs.face.basic_tongue import create_sample as inner
    obj.pose.bones[inner(obj)["tongue"]].rigify_type = 'game.face.basic_tongue'