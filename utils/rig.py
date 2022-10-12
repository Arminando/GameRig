

outdated_types = {"game.copy_chain"
                  }

def upgradeMetarigTypes(metarig):

    for bone in metarig.pose.bones:
        rig_type = bone.rigify_type
        if rig_type in outdated_types.keys():
            bone.rigify_type = outdated_types[rig_type]