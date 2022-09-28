import bpy

from rigify.rigs.limbs.leg import Rig as leg
from rigify.rigs.limbs.leg import create_sample as orig_create_sample
from .limb_rigs import BaseLimbRig

class Rig(BaseLimbRig, leg):
    pass


def create_sample(obj):
    bones = orig_create_sample(obj)

    pbone = obj.pose.bones[bones['thigh.L']]
    pbone.rigify_type = 'game.leg'
