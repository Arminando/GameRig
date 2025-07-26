import bpy

from ..utils.bones import BoneUtilityMixin

from rigify.base_rig import stage
from rigify.utils.naming import make_derived_name
from rigify.rigs.chain_rigs import SimpleChainRig as old_SimpleChainRig
from rigify.rigs.chain_rigs import TweakChainRig as old_TweakChainRig
from rigify.rigs.chain_rigs import ConnectingChainRig as old_connectingChainRig


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

    
    def make_deform_bone(self, i, org):
        name = self.copy_bone(org, make_derived_name(org, 'def'), parent=True, bbone=True)
        if self.bbone_segments:
            self.get_bone(name).bbone_segments = 1
        return name


    @stage.configure_bones
    def set_control_orientations(self):
        self.remove_quat_rot_mode(self.bones.ctrl)
    

class TweakChainRig(SimpleChainRig, old_TweakChainRig):
    pass


class ConnectingChainRig(TweakChainRig, old_connectingChainRig):
    bbone_segments = None


    @stage.parent_bones
    def parent_org_chain(self):
        if self.use_connect_chain and self.use_connect_reverse:

            for org, tweak in zip(self.bones.org, self.bones.ctrl.tweak[:-1]):
                self.set_bone_parent(org, tweak)

        else:
            self.set_bone_parent(self.bones.org[0], self.rig_parent_bone)


    def rig_org_bone(self, i, org, tweak, next_tweak):
        if self.use_connect_chain and self.use_connect_reverse:
            self.make_constraint(org, 'STRETCH_TO', next_tweak, keep_axis='SWING_Y')
        else:
            super(TweakChainRig, self).rig_org_bone(i, org, tweak, next_tweak)


    def make_deform_bone(self, i, org):
        name = super(TweakChainRig, self).make_deform_bone(i, org)
        
        return name