import bpy

from rigify.rigs.skin.transform.basic import Rig as basic


class Rig(basic):
    pass


def create_sample(obj):
    from rigify.rigs.basic.super_copy import create_sample as inner
    obj.pose.bones[inner(obj)["Bone"]].rigify_type = 'game.skin.transform.basic'