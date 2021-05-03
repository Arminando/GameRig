import bpy

from ..base_rig import BaseRig
from ..utils.bones import BoneUtilityMixin

from rigify.base_rig import stage
from rigify.utils.naming import make_derived_name
from rigify.rigs.chain_rigs import SimpleChainRig as old_SimpleChainRig
from rigify.rigs.chain_rigs import TweakChainRig as old_TweakChainRig


class SimpleChainRig(BoneUtilityMixin, old_SimpleChainRig):
    """A rig that consists of 3 connected chains of control, org and deform bones."""

    ##############################
    # Deform chain

    @stage.parent_bones
    def parent_deform_chain(self):
        # Connect is disabled so that the deformation bones can freely follow the location of their ORG bones
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.clean_def_hierarchy(self.bones.deform[0])

    def rig_deform_bone(self, i, deform, org):
        self.make_constraint(deform, 'COPY_LOCATION', org)
        self.make_constraint(deform, 'COPY_ROTATION', org)


class TweakChainRig(SimpleChainRig):
    pass


class ConnectingChainRig(TweakChainRig):
    bbone_segments = None