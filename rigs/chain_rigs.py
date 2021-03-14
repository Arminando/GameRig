import bpy
from itertools import count

from rigify.utils.rig import connected_children_names
from rigify.utils.naming import make_derived_name
from rigify.utils.widgets_basic import create_bone_widget
from rigify.utils.misc import map_list

from rigify.base_rig import BaseRig, stage
from rigify.rigs.chain_rigs import SimpleChainRig


class SimpleChainRig(SimpleChainRig):
    """A rig that consists of 3 connected chains of control, org and deform bones."""

    min_chain_length = 2

    def initialize(self):
        super().initialize()

    bbone_segments = None

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
        # Preparation for making a single deformation hierarchy
        # Enables easy finding of deformation bone to parent to in parent_deform_chain
        # TODO make this cleaner and easily applicable to all rigs
        name = self.copy_bone(org, make_derived_name(org, 'def'), parent=True, bbone=True)
        self.obj.pose.bones[org].rigify_associated_def = name
        if self.bbone_segments:
            self.get_bone(name).bbone_segments = self.bbone_segments
        return name

    @stage.parent_bones
    def parent_deform_chain(self):
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into a single hierarchy
        # TODO make this cleaner and easily applicable to all rigs
        def_bone = self.bones.deform[0]
        parent_bone = self.get_bone_parent(def_bone)
        if parent_bone:
            parents_def_bone = self.obj.pose.bones[parent_bone].rigify_associated_def
            if parents_def_bone:
                self.set_bone_parent(def_bone, parents_def_bone)


    def rig_deform_bone(self, i, deform, org):
        self.make_constraint(deform, 'COPY_LOCATION', org)
        self.make_constraint(deform, 'COPY_ROTATION', org)

        