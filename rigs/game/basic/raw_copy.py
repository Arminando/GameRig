import bpy

from rigify.rigs.basic.raw_copy import Rig as raw_copy
from rigify.rigs.basic.raw_copy import create_sample as orig_create_sample

class Rig(raw_copy):
    pass

def create_sample(obj):
    """ Create a sample metarig for this rig type.
    """
    bones = orig_create_sample(obj)

    pbone = obj.pose.bones[bones['DEF-bone']]
    pbone.rigify_type = 'game.basic.raw_copy'

    return bones