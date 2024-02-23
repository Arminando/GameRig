import bpy

from ....utils.bones import BoneUtilityMixin

from rigify.base_rig import stage
from rigify.rigs.limbs.limb_rigs import BaseLimbRig as old_BaseLimbRig
from rigify.rigs.limbs.limb_rigs import SegmentEntry
from rigify.utils.naming import choose_derived_bone


class BaseLimbRig(BoneUtilityMixin, old_BaseLimbRig):

    def initialize(self):
        super().initialize()
        self.bbone_segments = 1
        self.enable_scale = self.params.enable_scale
        self.leaf_hierarchy = self.params.leaf_hierarchy

    @stage.parent_bones
    def parent_deform_chain(self):
        self.set_bone_parent(self.bones.deform[0], self.rig_parent_bone)
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.clean_def_hierarchy(self.bones.deform[0])

        # Create leaf hierarchy
        if self.leaf_hierarchy:
            limb_segments = []
            for bone in self.bones.org['main']:
                limb_segments.append(choose_derived_bone(self.generator, bone, 'def'))
            self.set_bone_parent(limb_segments[1], limb_segments[0])
            self.set_bone_parent(limb_segments[2], limb_segments[1])

            for bone in self.bones.deform:
                if bone not in limb_segments:
                    for segment in limb_segments:
                        if segment in bone:
                            self.set_bone_parent(bone, segment)

    def rig_deform_bone(self, i, deform, entry, next_entry, tweak, next_tweak):
        if self.enable_scale:
            if tweak:
                self.make_constraint(deform, 'COPY_TRANSFORMS', tweak)

                if next_tweak:
                    self.make_constraint(deform, 'STRETCH_TO', next_tweak, keep_axis='SWING_Y')

                    # self.rig_deform_easing(i, deform, tweak, next_tweak) #bbone stuff, not relevant here.

                elif next_entry:
                    self.make_constraint(deform, 'STRETCH_TO', next_entry.org, keep_axis='SWING_Y')

            else:
                self.make_constraint(deform, 'COPY_TRANSFORMS', entry.org)
        else:
            if tweak:
                self.make_constraint(deform, 'COPY_LOCATION', tweak)
                self.make_constraint(deform, 'COPY_ROTATION', tweak)

                if next_tweak:
                    self.make_constraint(deform, 'DAMPED_TRACK', next_tweak)

                    # self.rig_deform_easing(i, deform, tweak, next_tweak) #bbone stuff, not relevant here.

                elif next_entry:
                    self.make_constraint(deform, 'DAMPED_TRACK', next_entry.org)

            else:
                self.make_constraint(deform, 'COPY_LOCATION', entry.org)
                self.make_constraint(deform, 'COPY_ROTATION', entry.org)

    @stage.configure_bones
    def set_control_orientations(self):
        self.remove_quat_rot_mode(self.bones.ctrl)

    
    # def rig_tweak_mch_bone(self, i: int, tweak: str, entry: SegmentEntry):
    #     if entry.seg_idx:
    #         prev_tweak, next_tweak, fac = self.get_tweak_blend(i, entry)

    #         self.make_constraint(tweak, 'COPY_TRANSFORMS', prev_tweak)
    #         self.make_constraint(tweak, 'COPY_TRANSFORMS', next_tweak, influence=fac)
    #         self.make_constraint(tweak, 'COPY_ROTATION', next_tweak, influence= entry.seg_idx / (self.segments - 1))
    #         self.make_constraint(tweak, 'DAMPED_TRACK', next_tweak)

    #     elif entry.seg_idx is not None:
    #         self.make_constraint(tweak, 'COPY_SCALE', self.bones.mch.follow, use_make_uniform=True)

    #     if i == 0:
    #         self.make_constraint(tweak, 'COPY_LOCATION', entry.org)
    #         self.make_constraint(tweak, 'DAMPED_TRACK', entry.org, head_tail=1)

    ##############################
    # Parameter UI

    @classmethod
    def add_parameters(self, params):
        """ Add the parameters of this rig type to the
            RigifyParameters PropertyGroup
        """
        super().add_parameters(params)
        params.enable_scale = bpy.props.BoolProperty(
            name="Scale",
            default=False,
            description="Deformation bones will inherit the scale of their ORG bones. Enable this only if you know what you are doing because scale can break your rig in the game engine"
        )
        params.leaf_hierarchy = bpy.props.BoolProperty(
            name="Leaf Hierarchy",
            default=False,
            description="False means limb segments and tweak bones will create a single chain. True means limb segments will be parented to each other directly and the tweak bones will be parented to their respective segment."
        )

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        super().parameters_ui(layout, params)

        c = layout.column()
        c.prop(params, "enable_scale")
        c.prop(params, "leaf_hierarchy")
