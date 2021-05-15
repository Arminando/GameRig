import bpy

from rigify.rigs.limbs.rear_paw import Rig as old_rear_paw
from rigify.rigs.limbs.rear_paw import create_sample as orig_create_sample
from .paw import Rig as paw

class Rig(paw, old_rear_paw):
    pass


def create_sample(obj):
    bones = orig_create_sample(obj)
    pbone = obj.pose.bones[bones['thigh.L']]
    pbone.rigify_type = 'game.rear_paw'
    return bones