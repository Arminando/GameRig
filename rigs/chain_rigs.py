import bpy

from ..base_rig import BaseRig
from ..utils.bones import BoneUtilityMixin

from rigify.base_rig import stage
from rigify.utils.naming import make_derived_name
from rigify.rigs.chain_rigs import SimpleChainRig
from rigify.rigs.basic.raw_copy import RelinkConstraintsMixin


class SimpleChainRig(BoneUtilityMixin, RelinkConstraintsMixin, SimpleChainRig):
    """A rig that consists of 3 connected chains of control, org and deform bones."""

    def initialize(self):
        super().initialize()

    ##############################
    # BONES
    #
    # org[]:
    #   ORG bones
    # ctrl:
    #   fk[]:
    #     FK control chain.
    # deform[]:
    #   DEF bones
    #
    ##############################

    ##############################
    # Control chain


    ##############################
    # ORG chain


    ##############################
    # Deform chain

    @stage.parent_bones
    def parent_deform_chain(self):
        # Connect is disabled so that the deformation bones can freely follow the location of their ORG bones
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.clean_def_hierarchy(self.bones.deform[0])


    def rig_deform_bone(self, i, deform, org):
        if self.enable_scale:
            self.make_constraint(deform, 'COPY_TRANSFORMS', org)
        else:
            self.make_constraint(deform, 'COPY_LOCATION', org)
            self.make_constraint(deform, 'COPY_ROTATION', org)

        