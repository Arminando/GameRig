import bpy
from .chain_rigs import ConnectingChainRig
from rigify.utils.layers import ControlLayersOption
from rigify.base_rig import stage


class BboneChainRig(ConnectingChainRig):

    min_chain_length = 2
    bbone_segments = 0 # For deformation bones

    def initialize(self):
        super().initialize()
        
        # self.use_connect_chain = self.params.connect_chain # Already happening in parent class
        # self.connected_tweak = None # Already happening in parent class
        self.bbone_start = self.params.bbone_start
        self.bbone_end = self.params.bbone_end
        self.control_divisions = self.params.control_divisions
        self.guide_bbone = self.params.guide_bbone
        self.parent_end_to_start = self.params.parent_end_to_start

    ##############################
    # BONES
    #
    # org[]:
    #   ORG bones
    # ctrl:
    #   Handles[]:
    #     B-Bone control handles.
    #   tweak[]:
    #     Tweak control chain.
    # deform[]:
    #   DEF bones
    #
    ##############################

    ##############################
    # Clean up things we don't need from the parent class
    @stage.generate_bones
    def make_control_chain(self):
        pass

    @stage.parent_bones
    def parent_control_chain(self):
        pass

    @stage.configure_bones
    def configure_control_chain(self):
        pass

    @stage.generate_widgets
    def make_control_widgets(self):
        pass
    
    # Will actually need to fix this one later and parent the tweaks properly
    @stage.parent_bones
    def parent_tweak_chain(self):
        for tweak in self.bones.ctrl.tweak:
            self.set_bone_parent(tweak, None)
    
    ####################################################
    # SETTINGS

    @classmethod
    def add_parameters(self, params):
        params.bbone_start = bpy.props.IntProperty(
            name='B-Bone Start',
            default=1,
            min=0,
            description='Index of bone at which the B-Bone will start'
        )
        params.bbone_end = bpy.props.IntProperty(
            name='B-Bone End',
            default=3,
            min=2,
            description='Index of bone at which the B-Bone will end. Last index is Tail of last bone in chain.'
        )
        params.control_divisions = bpy.props.IntProperty(
            name='Control Divisions',
            default=1,
            min=0,
            description='Number of controls along the B-Bone'
        )
        params.guide_bbone = bpy.props.StringProperty(
            name="Guide Bone",
            description="B-Bone that will be used as reference for setting B-Bone values on the final rig."
        )
        params.parent_end_to_start = bpy.props.BoolProperty(
            name="Parent End to Start",
            description="Should the end handle be parented to the start handle."
        )

        super().add_parameters(params)

    @classmethod
    def parameters_ui(self, layout, params):
        r = layout.row()
        super().parameters_ui(layout, params)

        layout.prop(params, 'parent_end_to_start')
        layout.prop(params, 'bbone_start', text = "B-Bone Index: Start")
        layout.prop(params, 'bbone_end', text = "End")
        layout.prop(params, 'control_divisions')
        layout.prop(params, 'guide_bbone')