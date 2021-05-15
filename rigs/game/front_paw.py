import bpy

from rigify.rigs.limbs.front_paw import Rig as old_front_paw
from rigify.rigs.limbs.front_paw import create_sample as orig_create_sample
from .paw import Rig as paw

class Rig(paw, old_front_paw):
    pass


def create_sample(obj):
    bones = orig_create_sample(obj)
    pbone = obj.pose.bones[bones['front_thigh.L']]
    pbone.rigify_type = 'game.front_paw'
    return bones