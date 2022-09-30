import bpy
import math

from ..skin.skin_rigs import BaseSkinRig
from rigify.rigs.face.skin_jaw import Rig as skin_jaw
from rigify.rigs.face.skin_jaw import create_sample as old_create_sample
from rigify.base_rig import stage


class Rig(BaseSkinRig, skin_jaw):
    
    @stage.parent_bones
    def parent_deform_chain(self):
        deform = self.bones.deform
        # self.set_bone_parent(deform.master, self.bones.org)
        
        self.clean_def_hierarchy(deform.master)

def create_sample(obj):
    bones = old_create_sample(obj)

    pbone = obj.pose.bones[bones['lip.T.L']]
    pbone.rigify_type = 'game.skin.stretchy_chain'
    pbone = obj.pose.bones[bones['lip.B.L']]
    pbone.rigify_type = 'game.skin.stretchy_chain'
    pbone = obj.pose.bones[bones['lip.T.R']]
    pbone.rigify_type = 'game.skin.stretchy_chain'
    pbone = obj.pose.bones[bones['lip.B.R']]
    pbone.rigify_type = 'game.skin.stretchy_chain'

    pbone = obj.pose.bones[bones['jaw']]
    pbone.rigify_type = 'game.face.skin_jaw'