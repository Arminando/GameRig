import bpy, os, importlib

from bpy.props import StringProperty

from . import gamerig_generate
from . import ui

rigify_info = {
    'name': "GameRig",
    'author': "Armin Halac",
    'version': (0, 0, 1),
    'blender': (2, 92, 0),
    'description': "Feature set made for game rigs",
    'doc_url': "TODO",
    'link': "TODO",
}

modules = [
    gamerig_generate,
    ui,
]

def register():

    # Properties
    bpy.types.PoseBone.rigify_associated_def = StringProperty(name = "Associated DEF bone", description = "Utility property used to easily find the DEF bone this ORG bone was duplicated from.")

    from bpy.utils import register_class
    for m in modules:
        importlib.reload(m)
        m.register()

def unregister():

    # Properties
    del bpy.types.PoseBone.rigify_associated_def
    
    from bpy.utils import unregister_class
    for m in reversed(modules):
        m.unregister

"""
# Copyed this from cloudrig, need to check what it does exactly
from rigify import feature_set_list
if not hasattr(feature_set_list, 'call_register_function'):
    register()
"""