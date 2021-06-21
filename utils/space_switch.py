import bpy

class gameRig_switch_parents(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="test",description="The name of the parent")
    position: bpy.props.IntProperty(name="Position", description="The index of the position in switch list")
    default: bpy.props.BoolProperty(default=False, name='Is Default', description="Will this be the default parent")





classes = [
    gameRig_switch_parents,
]


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
