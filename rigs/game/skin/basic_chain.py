import bpy
import math

from .skin_rigs import BaseSkinChainRigWithRotationOption
from rigify.rigs.skin.basic_chain import Rig as basic_chain
from rigify.base_rig import stage

class Rig(BaseSkinChainRigWithRotationOption, basic_chain):
    

    @stage.parent_bones
    def parent_deform_chain(self):
        
        self.set_bone_parent(self.bones.deform[0], self.rig_parent_bone)
        self.parent_bone_chain(self.bones.deform, use_connect=False)

        # This puts the deformation bones into the def hierarchy of its parent rig
        self.clean_def_hierarchy(self.bones.deform[0])

    def rig_deform_bone(self, i, deform, org):
        self.make_constraint(deform, 'COPY_LOCATION', org)
        self.make_constraint(deform, 'COPY_ROTATION', org)


    @classmethod
    def add_parameters(self, params):
        params.bbones = bpy.props.IntProperty(
            name='B-Bone Segments',
            default=1,
            min=1,
            description='Number of B-Bone segments'
        )

        params.skin_chain_use_reparent = bpy.props.BoolProperty(
            name='Merge Parent Rotation And Scale',
            default=False,
            description='When controls are merged into ones owned by other chains, include ' +
                        'parent-induced rotation/scale difference into handle motion. Otherwise ' +
                        'only local motion of the control bone is used',
        )

        params.skin_chain_use_scale = bpy.props.BoolVectorProperty(
            size=4,
            name='Use Handle Scale',
            default=(False, False, False, False),
            description='Use control scaling to scale the B-Bone'
        )

        params.skin_chain_connect_mirror = bpy.props.BoolVectorProperty(
            size=2,
            name='Connect With Mirror',
            default=(True, True),
            description='Create a smooth B-Bone transition if an end of the chain meets its mirror'
        )

        params.skin_chain_connect_sharp_angle = bpy.props.FloatVectorProperty(
            size=2,
            name='Sharpen Corner',
            default=(0, 0),
            min=0,
            max=math.pi,
            description='Create a mechanism to sharpen a connected corner when the angle is below this value',
            unit='ROTATION',
        )

        params.skin_chain_connect_ends = bpy.props.BoolVectorProperty(
            size=2,
            name='Connect Matching Ends',
            default=(False, False),
            description='Create a smooth B-Bone transition if an end of the chain meets another chain going in the same direction'
        )

        super().add_parameters(params)

def create_sample(obj):
    from ..basic.copy_chain import create_sample as inner
    obj.pose.bones[inner(obj)["bone.01"]].rigify_type = 'game.skin.basic_chain'
