import bpy

from rigify.base_rig import BaseRig
from .utils.bones import BoneUtilityMixin

class base_rig(BoneUtilityMixin, BaseRig):

    def __init__(self, generator, pose_bone):
        super().__init__(generator, pose_bone)

        pass

