import bpy, os, importlib

from bpy.props import EnumProperty

from . import gamerig_generate
from . import ui
from . import operators
from . utils import space_switch

rigify_info = {
    'name': "GameRig",
    'author': "Armin Halac",
    'version': (2, 0, 0),
    'blender': (4, 5, 4),
    'description': "Feature set made for game rigs",
    'doc_url': "https://github.com/Arminando/GameRig#readme",
    'link': "https://github.com/Arminando/GameRig",
}



modules = [
    space_switch,
    gamerig_generate,
    operators,
    ui,
]

def register():

    # Properties

    from bpy.utils import register_class
    for m in modules:
        importlib.reload(m)
        m.register()

def unregister():

    # Properties
    
    from bpy.utils import unregister_class
    for m in reversed(modules):
        m.unregister()
