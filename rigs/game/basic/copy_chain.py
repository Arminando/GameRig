import bpy

from itertools import count

from ...chain_rigs import SimpleChainRig
from rigify.base_rig import stage
from rigify.rigs.basic.copy_chain import Rig as copy_chain
from rigify.rigs.basic.copy_chain import create_sample as orig_create_sample
from rigify.utils.widgets import layout_widget_dropdown, create_registered_widget
from rigify.utils.widgets_basic import create_bone_widget

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

    @stage.generate_widgets
    def make_control_widgets(self):
        if self.make_controls:
            # Create control widget
            for args in zip(count(0), self.bones.ctrl.fk):
                self.make_control_widget(*args)

    def make_control_widget(self, i, ctrl):
        create_registered_widget(self.obj, ctrl, self.params.copy_chain_widget_type or 'bone')

    ##############################
    # ORG chain

    ##############################
    # Deform chain
    
    def rig_deform_bone(self, i, deform, org):
        if self.enable_scale:
            self.make_constraint(deform, 'COPY_TRANSFORMS', org)
        else:
            self.make_constraint(deform, 'COPY_LOCATION', org)
            self.make_constraint(deform, 'COPY_ROTATION', org)

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

        params.copy_chain_widget_type = bpy.props.StringProperty(
            name        = "Widget Type",
            default     = 'bone',
            description = "Choose the type of the widget to create"
        )

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        super().parameters_ui(layout, params)

        r = layout.row()
        r.prop(params, "enable_scale")

        r = layout.split(factor=0.3)
        r.label(text='Widget')
        r.enabled = params.make_controls

        r2 = r.row(align=True)
        r2.enabled = params.make_controls
        layout_widget_dropdown(r2, params, "copy_chain_widget_type", text="")


def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    bones = orig_create_sample(obj)

    pbone = obj.pose.bones[bones['bone.01']]
    pbone.rigify_type = 'game.copy_chain'

    obj.data.edit_bones[bones['bone.02']].roll = 0.0
    obj.data.edit_bones[bones['bone.03']].roll = 0.0

    return bones