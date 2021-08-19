import bpy

from ..utils.bones import BoneUtilityMixin

from rigify.base_rig import stage
from rigify.rigs.limbs.limb_rigs import BaseLimbRig as old_BaseLimbRig


class BaseLimbRig(BoneUtilityMixin, old_BaseLimbRig):

    def initialize(self):
        super().initialize()
        self.bbone_segments = 1
        self.enable_scale = self.params.enable_scale

    @stage.parent_bones
    def parent_deform_chain(self):
        self.set_bone_parent(self.bones.deform[0], self.rig_parent_bone)
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.clean_def_hierarchy(self.bones.deform[0])


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

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        super().parameters_ui(layout, params)

        r = layout.row()
        r.prop(params, "enable_scale")