import bpy

from ..base_rig import BaseRig
from ..utils.bones import BoneUtilityMixin

from rigify.base_rig import stage
from rigify.utils.naming import make_derived_name
from rigify.rigs.chain_rigs import SimpleChainRig


class SimpleChainRig(BoneUtilityMixin, SimpleChainRig):
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

    def make_deform_bone(self, i , org):
        name = super().make_deform_bone(i, org)

        # Preparation for making a single deformation hierarchy
        # Enables easy finding of deformation bone to parent to in parent_deform_chain
        self.write_def_name(self.obj, org, name)

        return name

    @stage.parent_bones
    def parent_deform_chain(self):
        # Connect is disabled so that the deformation bones can freely follow the location of their ORG bones
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.parent_to_def(self.bones.deform[0])


    def rig_deform_bone(self, i, deform, org):
        if self.enable_scale:
            self.make_constraint(deform, 'COPY_TRANSFORMS', org)
        else:
            self.make_constraint(deform, 'COPY_LOCATION', org)
            self.make_constraint(deform, 'COPY_ROTATION', org)

        