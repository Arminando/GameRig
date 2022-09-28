import bpy

from rigify.rigs.skin.stretchy_chain import Rig as stretchy_chain
from .basic_chain import Rig as BasicChainRig

class Rig(BasicChainRig, stretchy_chain):
    pass


def create_sample(obj):
    from ..basic.copy_chain import create_sample as inner
    obj.pose.bones[inner(obj)["bone.01"]].rigify_type = 'game.skin.stretchy_chain'
