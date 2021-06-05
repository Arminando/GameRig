import bpy, os, importlib

from bpy.props import EnumProperty

from . import gamerig_generate
from . import ui

rigify_info = {
    'name': "GameRig",
    'author': "Armin Halac",
    'version': (0, 0, 3),
    'blender': (2, 92, 0),
    'description': "Feature set made for game rigs",
    'doc_url': "https://github.com/Arminando/GameRig#readme",
    'link': "https://github.com/Arminando/GameRig",
}

modules = [
    gamerig_generate,
    ui,
]

def register():

    # Properties
    bpy.types.Armature.gameRig_force_generator = EnumProperty(items=(('Auto', 'Auto', 'Do not override'), ('Rigify', 'Rigify', 'Always use default generator'), ('GameRig', 'GameRig', 'Always use GameRig generator')), name='Force Generator')

    from bpy.utils import register_class
    for m in modules:
        importlib.reload(m)
        m.register()

def unregister():

    # Properties
    del bpy.types.Armature.gameRig_force_generator
    
    from bpy.utils import unregister_class
    for m in reversed(modules):
        m.unregister
