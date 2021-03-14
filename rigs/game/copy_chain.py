import bpy

from ..chain_rigs import SimpleChainRig
from rigify.base_rig import stage
from rigify.rigs.basic.copy_chain import Rig as copy_chain
from rigify.rigs.basic.copy_chain import create_sample as orig_create_sample

class Rig(SimpleChainRig, copy_chain):
    """ A "copy_chain" rig.  All it does is duplicate the original bone chain
        and constrain it.
        This is a control and deformation rig.
    """

    def initialize(self):
        super().initialize()

        """ Gather and validate data about the rig.
        """
        self.enable_scale = self.params.enable_scale

    ##############################
    # Control chain

    ##############################
    # ORG chain

    ##############################
    # Deform chain

    ##############################
    # Parameter UI

    @classmethod
    def add_parameters(self, params):
        """ Add the parameters of this rig type to the
            RigifyParameters PropertyGroup
        """
        super().add_parameters(params)
        params.enable_scale = bpy.props.BoolProperty(name="Scale", default=False, description="Deformation bones will inherit the scale of their ORG bones. Enable this only if you know what you are doing because scale can break your rig in the game engine")

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        super().parameters_ui(layout, params)
        #layout.separator(factor = 0.2)
        r = layout.row()
        r.prop(params, "enable_scale")



def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    bones = orig_create_sample(obj)

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['bone.01']]
    pbone.rigify_type = 'game.copy_chain'


    bpy.ops.object.mode_set(mode='EDIT')

    return bones