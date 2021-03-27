import bpy



class GAMERIG_OT_generate(bpy.types.Operator):
    """Generates a rig from the active metarig armature"""

    bl_idname = "pose.gamerig_generate"
    bl_label = "GameRig Generate Rig"
    bl_options = {'UNDO'}
    bl_description = 'Generates a rig from the active metarig armature'

    def execute(self, context):
        print("test")

        return {'FINISHED'}


classes = [
	GAMERIG_OT_generate,
]

def register():
    from bpy.utils import register_class
    for c in classes:
        print("registering", c)
        register_class(c)

def unregister():
	from bpy.utils import unregister_class
	for c in classes:
		unregister_class(c)
