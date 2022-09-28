import bpy

from ....utils.bones import BoneUtilityMixin

from rigify.rigs.skin.skin_rigs import BaseSkinRig as old_BaseSkinRig
from rigify.rigs.skin.skin_rigs import BaseSkinChainRig as old_BaseSkinChainRig
from rigify.rigs.skin.skin_rigs import BaseSkinChainRig as old_BaseSkinChainRigWithRotationOption




class BaseSkinRig(BoneUtilityMixin, old_BaseSkinRig):
    """
    Base type for all rigs involved in the skin system.
    This includes chain rigs and the parent provider rigs.
    """

    pass



class BaseSkinChainRig(BaseSkinRig, old_BaseSkinChainRig):
    """
    Base type for all skin rigs that can own control nodes, rather than
    only modifying nodes of their children or other rigs.
    """

    pass


class BaseSkinChainRigWithRotationOption(BaseSkinChainRig, old_BaseSkinChainRigWithRotationOption):
    """
    Skin chain rig with an option to override the orientation to use
    for controls via specifying an arbitrary template bone.
    """

    pass
