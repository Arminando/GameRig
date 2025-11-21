import bpy

from rigify.rigs.limbs.spline_tentacle import Rig as old_spline_tentacle
from rigify.rigs.limbs.spline_tentacle import create_sample as orig_create_sample
from ...chain_rigs import SimpleChainRig

class Rig(SimpleChainRig, old_spline_tentacle):
    
    def initialize(self):
        super().initialize()

        """ Gather and validate data about the rig.
        """
        self.enable_scale = self.params.enable_scale


    def rig_deform_bone(self, i, deform, org):
        if self.enable_scale:
            self.make_constraint(deform, 'COPY_TRANSFORMS', org)
        else:
            self.make_constraint(deform, 'COPY_LOCATION', org)
            self.make_constraint(deform, 'COPY_ROTATION', org)


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

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        super().parameters_ui(layout, params)

        r = layout.row()
        r.prop(params, "enable_scale")

def create_sample(obj):
    bones = orig_create_sample(obj)
    pbone = obj.pose.bones[bones['Bone']]
    pbone.rigify_type = 'game.spline_tentacle'
    return bones