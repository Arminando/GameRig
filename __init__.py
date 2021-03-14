import bpy, os, importlib

rigify_info = {
	'name': "GameRig",
	'author': "Armin Halac",
	'version': (0, 0, 1),
	'blender': (2, 92, 0),
	'description': "Feature set made for game friendly rigs",
	'doc_url': "TODO",
	'link': "TODO",
}

modules = [
    # Add custom module imports here
]

def register():
    from bpy.utils import register_class
    for m in modules:
        importlib.reload(m)
        n.register()

def unregister():
    from bpy.utils import unregister_class
    for m in reversed(modules):
        m.unregister

# Copyied this from cloudrig, need to check what it does exactly
from rigify import feature_set_list
if not hasattr(feature_set_list, 'call_register_function'):
	register()