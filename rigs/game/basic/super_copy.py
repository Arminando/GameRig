import bpy

from rigify.rigs.basic.super_copy import Rig as super_copy
from rigify.rigs.basic.super_copy import create_sample as orig_create_sample
from rigify.utils.naming import strip_org, make_deformer_name
from ....utils.bones import BoneUtilityMixin
from ....utils.space_switch import gameRig_switch_parents

class Rig(BoneUtilityMixin, super_copy):
    """ A "copy" rig.  All it does is duplicate the original bone and
        constrain it.
        This is a control and deformation rig.

    """

    def initialize(self):
        super().initialize()

        """ Gather and validate data about the rig.
        """
        self.enable_scale = self.params.enable_scale

    def generate_bones(self):
        bones = self.bones

        # Make a control bone (copy of original).
        if self.make_control:
            bones.ctrl = self.copy_bone(bones.org, self.org_name, parent=True)

        # Make a deformation bone (copy of original, child of original).
        if self.make_deform:
            bones.deform = self.copy_bone(bones.org, make_deformer_name(self.org_name), parent = True, bbone=False)
    

    def parent_bones(self):
        bones = self.bones

        new_parent = self.relink_bone_parent(bones.org)

        if self.make_control and new_parent:
            self.set_bone_parent(bones.ctrl, new_parent)
        # This puts the deformation bones into the def hierarchy of its parent rig
        if self.make_deform:
            self.clean_def_hierarchy(self.bones.deform)


    def rig_bones(self):
        bones = self.bones

        self.relink_bone_constraints(bones.org)

        if self.make_control:
            self.relink_move_constraints(bones.org, bones.ctrl, prefix='CTRL:')

            # Constrain the original bone.
            self.make_constraint(bones.org, 'COPY_TRANSFORMS', bones.ctrl, insert_index=0)

        if self.make_deform:
            if self.enable_scale:
                self.make_constraint(bones.deform, 'COPY_TRANSFORMS', bones.org)
            else:
                self.make_constraint(bones.deform, 'COPY_LOCATION', bones.org)
                self.make_constraint(bones.deform, 'COPY_ROTATION', bones.org)

    def configure_bones(self):
        if self.bones.ctrl:
            controls = {'ctrl': [self.bones.ctrl]}
            self.remove_quat_rot_mode(controls)
        


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

        params.switch_parents = bpy.props.CollectionProperty(type=gameRig_switch_parents)

    @classmethod
    def parameters_ui(self, layout, params):
        """ Create the ui for the rig parameters.
        """
        super().parameters_ui(layout, params)

        r = layout.row()
        r.prop(params, "enable_scale")
        # WIP of a new space switch system test, ignore it
        # col = layout.column()
        # for parent in params.switch_parents:
        #     col.label(text=parent.name)


    @classmethod
    def get_space_switch_children(self):
        """ Return list of names of bones for space switching
        """
        return ["bone"]


def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    bones = orig_create_sample(obj)

    pbone = obj.pose.bones[bones['Bone']]
    pbone.rigify_type = 'game.basic.super_copy'

    return bones