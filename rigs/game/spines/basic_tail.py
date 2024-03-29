import bpy

from rigify.rigs.spines.basic_tail import Rig as basic_tail
from .spine_rigs import BaseHeadTailRig

class Rig(BaseHeadTailRig, basic_tail):

    pass


def create_sample(obj, *, parent=None):
    # generated by rigify.utils.write_metarig
    bpy.ops.object.mode_set(mode='EDIT')
    arm = obj.data

    bones = {}

    bone = arm.edit_bones.new('tail')
    bone.head[:] = 0.0000, 0.0552, 1.0099
    bone.tail[:] = -0.0000, 0.0582, 0.8669
    bone.roll = 0.0000
    bone.use_connect = False
    if parent:
        bone.parent = arm.edit_bones[parent]
    bones['tail'] = bone.name
    bone = arm.edit_bones.new('tail.001')
    bone.head[:] = -0.0000, 0.0582, 0.8669
    bone.tail[:] = -0.0000, 0.0365, 0.7674
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tail']]
    bones['tail.001'] = bone.name
    bone = arm.edit_bones.new('tail.002')
    bone.head[:] = -0.0000, 0.0365, 0.7674
    bone.tail[:] = -0.0000, 0.0010, 0.6984
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tail.001']]
    bones['tail.002'] = bone.name

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['tail']]
    pbone.rigify_type = 'game.spines.basic_tail'
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    try:
        pbone.rigify_parameters.connect_chain = bool(parent)
    except AttributeError:
        pass
    try:
        pbone.rigify_parameters.tweak_layers = [False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    except AttributeError:
        pass
    pbone = obj.pose.bones[bones['tail.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tail.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    for b in bones:
        bone = arm.edit_bones[bones[b]]
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        arm.edit_bones.active = bone