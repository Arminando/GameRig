import bpy

from rigify.rigs.spines.super_head import Rig as super_head
from rigify.rigs.spines.super_head import create_sample as orig_create_sample
from ..spine_rigs import BaseHeadTailRig


class Rig(BaseHeadTailRig, super_head):
    """
    Head rig with long neck support and connect option.
    """
    
    def rig_deform_bone(self, i, deform, org):
        if self.enable_scale:
            self.make_constraint(deform, 'COPY_TRANSFORMS', org)
        else:
            self.make_constraint(deform, 'COPY_LOCATION', org)
            self.make_constraint(deform, 'COPY_ROTATION', org)


def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    bones = orig_create_sample(obj)

    pbone = obj.pose.bones[bones['neck']]
    pbone.rigify_type = 'game.super_head'

    return bones