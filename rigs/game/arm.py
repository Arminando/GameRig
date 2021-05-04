import bpy

from rigify.rigs.limbs.arm import Rig as arm
from rigify.rigs.limbs.arm import create_sample as orig_create_sample
from ..limb_rigs import BaseLimbRig

class Rig(BaseLimbRig, arm):
    pass


def create_sample(obj, limb = False):
    bones = orig_create_sample(obj, limb)

    pbone = obj.pose.bones[bones['upper_arm.L']]
    pbone.rigify_type = 'game.super_limb' if limb else 'game.arm'
