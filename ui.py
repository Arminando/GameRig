import bpy
import addon_utils

from rigify import rig_lists




classes = (
    
)

def register():
    from bpy.utils import register_class

    # Classes.
    for c in classes:
        register_class(c)



def unregister():
    from bpy.utils import unregister_class

    # Classes.
    for c in classes:
        unregister_class(c)
