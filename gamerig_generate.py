import bpy






classes = [
	
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
