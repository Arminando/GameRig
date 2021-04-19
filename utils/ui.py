

def is_gamerig_metarig(rig):
	if rig.type=='ARMATURE' and 'rig_id' not in rig.data:
		for b in rig.pose.bones:
			if 'game' in b.rigify_type:
				return True
	return False