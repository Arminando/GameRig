import bpy

from rigify.rigs.faces.super_face import Rig as old_super_face
from rigify.utils.layers import ControlLayersOption
from rigify.utils.naming import org, strip_org, make_deformer_name, make_mechanism_name
from rigify.utils.bones import copy_bone

from ...utils.bones import BoneUtilityMixin

class Rig(BoneUtilityMixin, old_super_face):


    def create_deformation(self):
        org_bones = self.org_bones

        bpy.ops.object.mode_set(mode='EDIT')
        eb = self.obj.data.edit_bones

        def_bones = []
        for org in org_bones:
            if 'face' in org or 'teeth' in org or 'eye' in org:
                continue

            def_name = make_deformer_name( strip_org( org ) )
            def_name = copy_bone( self.obj, org, def_name, parent=True)
            def_bones.append( def_name )

            eb[def_name].use_connect = False
            eb[def_name].parent      = None

        brow_top_names = [ bone for bone in def_bones if 'brow.T'   in bone ]
        forehead_names = [ bone for bone in def_bones if 'forehead' in bone ]

        brow_left, brow_right         = self.symmetrical_split( brow_top_names )
        forehead_left, forehead_right = self.symmetrical_split( forehead_names )

        brow_left  = brow_left[1:]
        brow_right = brow_right[1:]
        brow_left.reverse()
        brow_right.reverse()

        for browL, browR, foreheadL, foreheadR in zip(
            brow_left, brow_right, forehead_left, forehead_right ):

            eb[foreheadL].tail = eb[browL].head
            eb[foreheadR].tail = eb[browR].head

        return { 'all' : def_bones }


    def parent_bones(self, all_bones, tweak_unique):
        org_bones = self.org_bones
        bpy.ops.object.mode_set(mode ='EDIT')
        eb = self.obj.data.edit_bones

        face_name = [ bone for bone in org_bones if 'face' in bone ].pop()
"""
        # Initially parenting all bones to the face org bone.
        for category in list( all_bones.keys() ):
            for area in list( all_bones[category] ):
                for bone in all_bones[category][area]:
                    eb[ bone ].parent = eb[ face_name ]
        
        ## Parenting all deformation bones and org bones

        # Parent all the deformation bones that have respective tweaks
        def_tweaks = [ bone for bone in all_bones['deform']['all'] if bone[4:] in all_bones['tweaks']['all'] ]

        # Parent all org bones to the ORG-face
        for bone in [ bone for bone in org_bones if 'face' not in bone ]:
            eb[ bone ].parent = eb[ org('face') ]

        for bone in def_tweaks:
            # the def and the matching org bone are parented to their corresponding tweak,
            # whose name is the same as that of the def bone, without the "DEF-" (first 4 chars)
            eb[ bone ].parent            = eb[ bone[4:] ]
            eb[ org( bone[4:] ) ].parent = eb[ bone[4:] ]

        # Parent ORG eyes to corresponding mch bones
        for bone in [ bone for bone in org_bones if 'eye' in bone ]:
            eb[ bone ].parent = eb[ make_mechanism_name( strip_org( bone ) ) ]

        for lip_tweak in list( tweak_unique.values() ):
            # find the def bones that match unique lip_tweaks by slicing [4:-2]
            # example: 'lip.B' matches 'DEF-lip.B.R' and 'DEF-lip.B.L' if
            # you cut off the "DEF-" [4:] and the ".L" or ".R" [:-2]
            lip_defs = [ bone for bone in all_bones['deform']['all'] if bone[4:-2] == lip_tweak ]

            for bone in lip_defs:
                eb[bone].parent = eb[ lip_tweak ]

        # parent cheek bones top respetive tweaks
        lips  = [ 'lips.L',   'lips.R'   ]
        brows = [ 'brow.T.L', 'brow.T.R' ]
        cheekB_defs = [ 'DEF-cheek.B.L', 'DEF-cheek.B.R' ]
        cheekT_defs = [ 'DEF-cheek.T.L', 'DEF-cheek.T.R' ]

        for lip, brow, cheekB, cheekT in zip( lips, brows, cheekB_defs, cheekT_defs ):
            eb[ cheekB ].parent = eb[ lip ]
            eb[ cheekT ].parent = eb[ brow ]

        # parent ear deform bones to their controls
        ear_defs  = [ 'DEF-ear.L', 'DEF-ear.L.001', 'DEF-ear.R', 'DEF-ear.R.001' ]
        ear_ctrls = [ 'ear.L', 'ear.R' ]

        eb[ 'DEF-jaw' ].parent = eb[ 'jaw' ] # Parent jaw def bone to jaw tweak

        for ear_ctrl in ear_ctrls:
            for ear_def in ear_defs:
                if ear_ctrl in ear_def:
                    eb[ ear_def ].parent = eb[ ear_ctrl ]

        # Parent eyelid deform bones (each lid def bone is parented to its respective MCH bone)
        def_lids = [ bone for bone in all_bones['deform']['all'] if 'lid' in bone ]

        for bone in def_lids:
            mch = make_mechanism_name( bone[4:] )
            eb[ bone ].parent = eb[ mch ]

        ## Parenting all mch bones

        eb[ 'MCH-eyes_parent' ].parent = None  # eyes_parent will be parented to root

        # parent all mch tongue bones to the jaw master control bone
        for bone in all_bones['mch']['tongue']:
            eb[ bone ].parent = eb[ all_bones['ctrls']['jaw'][0] ]

        ## Parenting the control bones

        # parent teeth.B and tongue master controls to the jaw master control bone
        for bone in [ 'teeth.B', 'tongue_master' ]:
            eb[ bone ].parent = eb[ all_bones['ctrls']['jaw'][0] ]

        # eyes
        eb[ 'eyes' ].parent = eb[ 'MCH-eyes_parent' ]

        eyes = [
            bone for bone in all_bones['ctrls']['eyes'] if 'eyes' not in bone
        ][0:2]

        for eye in eyes:
            eb[ eye ].parent = eb[ 'eyes' ]

        ## turbo: parent eye master bones to face
        for eye_master in eyes[2:]:
            eb[ eye_master ].parent = eb[ 'ORG-face' ]

        # Parent brow.b, eyes mch and lid tweaks and mch bones to masters
        tweaks = [
            b for b in all_bones['tweaks']['all'] if 'lid' in b or 'brow.B' in b
        ]
        mch = all_bones['mch']['lids']  + \
              all_bones['mch']['eye.R'] + \
              all_bones['mch']['eye.L']

        everyone = tweaks + mch

        left, right = self.symmetrical_split( everyone )

        for l in left:
            eb[ l ].parent = eb[ 'master_eye.L' ]

        for r in right:
            eb[ r ].parent = eb[ 'master_eye.R' ]

        ## turbo: nose to mch jaw.004
        eb[ all_bones['ctrls']['nose'].pop() ].parent = eb['MCH-jaw_master.004']

        ## Parenting the tweak bones

        # Jaw children (values) groups and their parents (keys)
        groups = {
            'jaw_master'         : [
                'jaw',
                'jaw.R.001',
                'jaw.L.001',
                'chin.L',
                'chin.R',
                'chin',
                'tongue.003'
                ],
            'MCH-jaw_master'     : [
                 'lip.B'
                ],
            'MCH-jaw_master.001' : [
                'lip.B.L.001',
                'lip.B.R.001'
                ],
            'MCH-jaw_master.002' : [
                'lips.L',
                'lips.R',
                'cheek.B.L.001',
                'cheek.B.R.001'
                ],
            'MCH-jaw_master.003' : [
                'lip.T',
                'lip.T.L.001',
                'lip.T.R.001'
                ],
            'MCH-jaw_master.004' : [
                'cheek.T.L.001',
                'cheek.T.R.001'
                ],
            'nose_master'        : [
                'nose.002',
                'nose.004',
                'nose.L.001',
                'nose.R.001'
                ]
             }

        for parent in list( groups.keys() ):
            for bone in groups[parent]:
                eb[ bone ].parent = eb[ parent ]

        # Remaining arbitrary relatioships for tweak bone parenting
        eb[ 'chin.001'   ].parent = eb[ 'chin'           ]
        eb[ 'chin.002'   ].parent = eb[ 'lip.B'          ]
        eb[ 'nose.001'   ].parent = eb[ 'nose.002'       ]
        eb[ 'nose.003'   ].parent = eb[ 'nose.002'       ]
        eb[ 'nose.005'   ].parent = eb[ 'lip.T'          ]
        eb[ 'tongue'     ].parent = eb[ 'tongue_master'  ]
        eb[ 'tongue.001' ].parent = eb[ 'MCH-tongue.001' ]
        eb[ 'tongue.002' ].parent = eb[ 'MCH-tongue.002' ]

        for bone in [ 'ear.L.002', 'ear.L.003', 'ear.L.004' ]:
            eb[ bone                       ].parent = eb[ 'ear.L' ]
            eb[ bone.replace( '.L', '.R' ) ].parent = eb[ 'ear.R' ]
"""


def add_parameters(params):
    """ Add the parameters of this rig type to the
        RigifyParameters PropertyGroup
    """

    # Setting up extra layers for the tweak bones
    ControlLayersOption.FACE_PRIMARY.add_parameters(params)
    ControlLayersOption.FACE_SECONDARY.add_parameters(params)


def parameters_ui(layout, params):
    """ Create the ui for the rig parameters."""

    ControlLayersOption.FACE_PRIMARY.parameters_ui(layout, params)
    ControlLayersOption.FACE_SECONDARY.parameters_ui(layout, params)



def create_sample(obj):
    # generated by rigify.utils.write_metarig
    bpy.ops.object.mode_set(mode='EDIT')
    arm = obj.data

    bones = {}

    bone = arm.edit_bones.new('face')
    bone.head[:] = -0.0000, -0.0013, 0.0437
    bone.tail[:] = -0.0000, -0.0013, 0.1048
    bone.roll = 0.0000
    bone.use_connect = False
    bones['face'] = bone.name
    bone = arm.edit_bones.new('nose')
    bone.head[:] = 0.0000, -0.0905, 0.1125
    bone.tail[:] = 0.0000, -0.1105, 0.0864
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['nose'] = bone.name
    bone = arm.edit_bones.new('lip.T.L')
    bone.head[:] = 0.0000, -0.1022, 0.0563
    bone.tail[:] = 0.0131, -0.0986, 0.0567
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['lip.T.L'] = bone.name
    bone = arm.edit_bones.new('lip.B.L')
    bone.head[:] = 0.0000, -0.0993, 0.0455
    bone.tail[:] = 0.0124, -0.0938, 0.0488
    bone.roll = -0.0789
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['lip.B.L'] = bone.name
    bone = arm.edit_bones.new('jaw')
    bone.head[:] = 0.0000, -0.0389, 0.0222
    bone.tail[:] = 0.0000, -0.0923, 0.0044
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['jaw'] = bone.name
    bone = arm.edit_bones.new('ear.L')
    bone.head[:] = 0.0616, -0.0083, 0.0886
    bone.tail[:] = 0.0663, -0.0101, 0.1151
    bone.roll = -0.0324
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['ear.L'] = bone.name
    bone = arm.edit_bones.new('ear.R')
    bone.head[:] = -0.0616, -0.0083, 0.0886
    bone.tail[:] = -0.0663, -0.0101, 0.1151
    bone.roll = 0.0324
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['ear.R'] = bone.name
    bone = arm.edit_bones.new('lip.T.R')
    bone.head[:] = -0.0000, -0.1022, 0.0563
    bone.tail[:] = -0.0131, -0.0986, 0.0567
    bone.roll = -0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['lip.T.R'] = bone.name
    bone = arm.edit_bones.new('lip.B.R')
    bone.head[:] = -0.0000, -0.0993, 0.0455
    bone.tail[:] = -0.0124, -0.0938, 0.0488
    bone.roll = 0.0789
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['lip.B.R'] = bone.name
    bone = arm.edit_bones.new('brow.B.L')
    bone.head[:] = 0.0530, -0.0705, 0.1153
    bone.tail[:] = 0.0472, -0.0780, 0.1192
    bone.roll = 0.0412
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['brow.B.L'] = bone.name
    bone = arm.edit_bones.new('lid.T.L')
    bone.head[:] = 0.0515, -0.0692, 0.1104
    bone.tail[:] = 0.0474, -0.0785, 0.1136
    bone.roll = 0.1166
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['lid.T.L'] = bone.name
    bone = arm.edit_bones.new('brow.B.R')
    bone.head[:] = -0.0530, -0.0705, 0.1153
    bone.tail[:] = -0.0472, -0.0780, 0.1192
    bone.roll = -0.0412
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['brow.B.R'] = bone.name
    bone = arm.edit_bones.new('lid.T.R')
    bone.head[:] = -0.0515, -0.0692, 0.1104
    bone.tail[:] = -0.0474, -0.0785, 0.1136
    bone.roll = -0.1166
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['lid.T.R'] = bone.name
    bone = arm.edit_bones.new('forehead.L')
    bone.head[:] = 0.0113, -0.0764, 0.1611
    bone.tail[:] = 0.0144, -0.0912, 0.1236
    bone.roll = 1.4313
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['forehead.L'] = bone.name
    bone = arm.edit_bones.new('forehead.R')
    bone.head[:] = -0.0113, -0.0764, 0.1611
    bone.tail[:] = -0.0144, -0.0912, 0.1236
    bone.roll = -1.4313
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['forehead.R'] = bone.name
    bone = arm.edit_bones.new('eye.L')
    bone.head[:] = 0.0360, -0.0686, 0.1107
    bone.tail[:] = 0.0360, -0.0848, 0.1107
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['eye.L'] = bone.name
    bone = arm.edit_bones.new('eye.R')
    bone.head[:] = -0.0360, -0.0686, 0.1107
    bone.tail[:] = -0.0360, -0.0848, 0.1107
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['eye.R'] = bone.name
    bone = arm.edit_bones.new('cheek.T.L')
    bone.head[:] = 0.0568, -0.0506, 0.1052
    bone.tail[:] = 0.0379, -0.0834, 0.0816
    bone.roll = -0.0096
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['cheek.T.L'] = bone.name
    bone = arm.edit_bones.new('cheek.T.R')
    bone.head[:] = -0.0568, -0.0506, 0.1052
    bone.tail[:] = -0.0379, -0.0834, 0.0816
    bone.roll = 0.0096
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['cheek.T.R'] = bone.name
    bone = arm.edit_bones.new('teeth.T')
    bone.head[:] = 0.0000, -0.0927, 0.0613
    bone.tail[:] = 0.0000, -0.0621, 0.0613
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['teeth.T'] = bone.name
    bone = arm.edit_bones.new('teeth.B')
    bone.head[:] = 0.0000, -0.0881, 0.0397
    bone.tail[:] = 0.0000, -0.0575, 0.0397
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['teeth.B'] = bone.name
    bone = arm.edit_bones.new('tongue')
    bone.head[:] = 0.0000, -0.0781, 0.0493
    bone.tail[:] = 0.0000, -0.0620, 0.0567
    bone.roll = 0.0000
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['face']]
    bones['tongue'] = bone.name
    bone = arm.edit_bones.new('nose.001')
    bone.head[:] = 0.0000, -0.1105, 0.0864
    bone.tail[:] = 0.0000, -0.1193, 0.0771
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['nose']]
    bones['nose.001'] = bone.name
    bone = arm.edit_bones.new('lip.T.L.001')
    bone.head[:] = 0.0131, -0.0986, 0.0567
    bone.tail[:] = 0.0236, -0.0877, 0.0519
    bone.roll = 0.0236
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lip.T.L']]
    bones['lip.T.L.001'] = bone.name
    bone = arm.edit_bones.new('lip.B.L.001')
    bone.head[:] = 0.0124, -0.0938, 0.0488
    bone.tail[:] = 0.0236, -0.0877, 0.0519
    bone.roll = 0.0731
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lip.B.L']]
    bones['lip.B.L.001'] = bone.name
    bone = arm.edit_bones.new('chin')
    bone.head[:] = 0.0000, -0.0923, 0.0044
    bone.tail[:] = 0.0000, -0.0921, 0.0158
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['jaw']]
    bones['chin'] = bone.name
    bone = arm.edit_bones.new('ear.L.001')
    bone.head[:] = 0.0663, -0.0101, 0.1151
    bone.tail[:] = 0.0804, 0.0065, 0.1189
    bone.roll = 0.0656
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.L']]
    bones['ear.L.001'] = bone.name
    bone = arm.edit_bones.new('ear.R.001')
    bone.head[:] = -0.0663, -0.0101, 0.1151
    bone.tail[:] = -0.0804, 0.0065, 0.1189
    bone.roll = -0.0656
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.R']]
    bones['ear.R.001'] = bone.name
    bone = arm.edit_bones.new('lip.T.R.001')
    bone.head[:] = -0.0131, -0.0986, 0.0567
    bone.tail[:] = -0.0236, -0.0877, 0.0519
    bone.roll = -0.0236
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lip.T.R']]
    bones['lip.T.R.001'] = bone.name
    bone = arm.edit_bones.new('lip.B.R.001')
    bone.head[:] = -0.0124, -0.0938, 0.0488
    bone.tail[:] = -0.0236, -0.0877, 0.0519
    bone.roll = -0.0731
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lip.B.R']]
    bones['lip.B.R.001'] = bone.name
    bone = arm.edit_bones.new('brow.B.L.001')
    bone.head[:] = 0.0472, -0.0780, 0.1192
    bone.tail[:] = 0.0387, -0.0832, 0.1202
    bone.roll = 0.0192
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.B.L']]
    bones['brow.B.L.001'] = bone.name
    bone = arm.edit_bones.new('lid.T.L.001')
    bone.head[:] = 0.0474, -0.0785, 0.1136
    bone.tail[:] = 0.0394, -0.0838, 0.1147
    bone.roll = 0.0791
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.L']]
    bones['lid.T.L.001'] = bone.name
    bone = arm.edit_bones.new('brow.B.R.001')
    bone.head[:] = -0.0472, -0.0780, 0.1192
    bone.tail[:] = -0.0387, -0.0832, 0.1202
    bone.roll = -0.0192
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.B.R']]
    bones['brow.B.R.001'] = bone.name
    bone = arm.edit_bones.new('lid.T.R.001')
    bone.head[:] = -0.0474, -0.0785, 0.1136
    bone.tail[:] = -0.0394, -0.0838, 0.1147
    bone.roll = -0.0791
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.R']]
    bones['lid.T.R.001'] = bone.name
    bone = arm.edit_bones.new('forehead.L.001')
    bone.head[:] = 0.0321, -0.0663, 0.1646
    bone.tail[:] = 0.0394, -0.0828, 0.1310
    bone.roll = 0.9928
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['forehead.L']]
    bones['forehead.L.001'] = bone.name
    bone = arm.edit_bones.new('forehead.R.001')
    bone.head[:] = -0.0321, -0.0663, 0.1646
    bone.tail[:] = -0.0394, -0.0828, 0.1310
    bone.roll = -0.9928
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['forehead.R']]
    bones['forehead.R.001'] = bone.name
    bone = arm.edit_bones.new('cheek.T.L.001')
    bone.head[:] = 0.0379, -0.0834, 0.0816
    bone.tail[:] = 0.0093, -0.0846, 0.1002
    bone.roll = 0.0320
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.T.L']]
    bones['cheek.T.L.001'] = bone.name
    bone = arm.edit_bones.new('cheek.T.R.001')
    bone.head[:] = -0.0379, -0.0834, 0.0816
    bone.tail[:] = -0.0093, -0.0846, 0.1002
    bone.roll = -0.0320
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.T.R']]
    bones['cheek.T.R.001'] = bone.name
    bone = arm.edit_bones.new('tongue.001')
    bone.head[:] = 0.0000, -0.0620, 0.0567
    bone.tail[:] = 0.0000, -0.0406, 0.0584
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tongue']]
    bones['tongue.001'] = bone.name
    bone = arm.edit_bones.new('nose.002')
    bone.head[:] = 0.0000, -0.1193, 0.0771
    bone.tail[:] = 0.0000, -0.1118, 0.0739
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['nose.001']]
    bones['nose.002'] = bone.name
    bone = arm.edit_bones.new('chin.001')
    bone.head[:] = 0.0000, -0.0921, 0.0158
    bone.tail[:] = 0.0000, -0.0914, 0.0404
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['chin']]
    bones['chin.001'] = bone.name
    bone = arm.edit_bones.new('ear.L.002')
    bone.head[:] = 0.0804, 0.0065, 0.1189
    bone.tail[:] = 0.0808, 0.0056, 0.0935
    bone.roll = -0.0265
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.L.001']]
    bones['ear.L.002'] = bone.name
    bone = arm.edit_bones.new('ear.R.002')
    bone.head[:] = -0.0804, 0.0065, 0.1189
    bone.tail[:] = -0.0808, 0.0056, 0.0935
    bone.roll = 0.0265
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.R.001']]
    bones['ear.R.002'] = bone.name
    bone = arm.edit_bones.new('brow.B.L.002')
    bone.head[:] = 0.0387, -0.0832, 0.1202
    bone.tail[:] = 0.0295, -0.0826, 0.1179
    bone.roll = -0.0278
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.B.L.001']]
    bones['brow.B.L.002'] = bone.name
    bone = arm.edit_bones.new('lid.T.L.002')
    bone.head[:] = 0.0394, -0.0838, 0.1147
    bone.tail[:] = 0.0317, -0.0832, 0.1131
    bone.roll = -0.0356
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.L.001']]
    bones['lid.T.L.002'] = bone.name
    bone = arm.edit_bones.new('brow.B.R.002')
    bone.head[:] = -0.0387, -0.0832, 0.1202
    bone.tail[:] = -0.0295, -0.0826, 0.1179
    bone.roll = 0.0278
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.B.R.001']]
    bones['brow.B.R.002'] = bone.name
    bone = arm.edit_bones.new('lid.T.R.002')
    bone.head[:] = -0.0394, -0.0838, 0.1147
    bone.tail[:] = -0.0317, -0.0832, 0.1131
    bone.roll = 0.0356
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.R.001']]
    bones['lid.T.R.002'] = bone.name
    bone = arm.edit_bones.new('forehead.L.002')
    bone.head[:] = 0.0482, -0.0506, 0.1620
    bone.tail[:] = 0.0556, -0.0689, 0.1249
    bone.roll = 0.4509
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['forehead.L.001']]
    bones['forehead.L.002'] = bone.name
    bone = arm.edit_bones.new('forehead.R.002')
    bone.head[:] = -0.0482, -0.0506, 0.1620
    bone.tail[:] = -0.0556, -0.0689, 0.1249
    bone.roll = -0.4509
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['forehead.R.001']]
    bones['forehead.R.002'] = bone.name
    bone = arm.edit_bones.new('nose.L')
    bone.head[:] = 0.0093, -0.0846, 0.1002
    bone.tail[:] = 0.0118, -0.0966, 0.0757
    bone.roll = -0.0909
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.T.L.001']]
    bones['nose.L'] = bone.name
    bone = arm.edit_bones.new('nose.R')
    bone.head[:] = -0.0093, -0.0846, 0.1002
    bone.tail[:] = -0.0118, -0.0966, 0.0757
    bone.roll = 0.0909
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.T.R.001']]
    bones['nose.R'] = bone.name
    bone = arm.edit_bones.new('tongue.002')
    bone.head[:] = 0.0000, -0.0406, 0.0584
    bone.tail[:] = 0.0000, -0.0178, 0.0464
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['tongue.001']]
    bones['tongue.002'] = bone.name
    bone = arm.edit_bones.new('nose.003')
    bone.head[:] = 0.0000, -0.1118, 0.0739
    bone.tail[:] = 0.0000, -0.1019, 0.0733
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['nose.002']]
    bones['nose.003'] = bone.name
    bone = arm.edit_bones.new('ear.L.003')
    bone.head[:] = 0.0808, 0.0056, 0.0935
    bone.tail[:] = 0.0677, -0.0109, 0.0752
    bone.roll = 0.3033
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.L.002']]
    bones['ear.L.003'] = bone.name
    bone = arm.edit_bones.new('ear.R.003')
    bone.head[:] = -0.0808, 0.0056, 0.0935
    bone.tail[:] = -0.0677, -0.0109, 0.0752
    bone.roll = -0.3033
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.R.002']]
    bones['ear.R.003'] = bone.name
    bone = arm.edit_bones.new('brow.B.L.003')
    bone.head[:] = 0.0295, -0.0826, 0.1179
    bone.tail[:] = 0.0201, -0.0812, 0.1095
    bone.roll = 0.0417
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.B.L.002']]
    bones['brow.B.L.003'] = bone.name
    bone = arm.edit_bones.new('lid.T.L.003')
    bone.head[:] = 0.0317, -0.0832, 0.1131
    bone.tail[:] = 0.0237, -0.0826, 0.1058
    bone.roll = 0.0245
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.L.002']]
    bones['lid.T.L.003'] = bone.name
    bone = arm.edit_bones.new('brow.B.R.003')
    bone.head[:] = -0.0295, -0.0826, 0.1179
    bone.tail[:] = -0.0201, -0.0812, 0.1095
    bone.roll = -0.0417
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.B.R.002']]
    bones['brow.B.R.003'] = bone.name
    bone = arm.edit_bones.new('lid.T.R.003')
    bone.head[:] = -0.0317, -0.0832, 0.1131
    bone.tail[:] = -0.0237, -0.0826, 0.1058
    bone.roll = -0.0245
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.R.002']]
    bones['lid.T.R.003'] = bone.name
    bone = arm.edit_bones.new('temple.L')
    bone.head[:] = 0.0585, -0.0276, 0.1490
    bone.tail[:] = 0.0607, -0.0295, 0.0962
    bone.roll = -0.0650
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['forehead.L.002']]
    bones['temple.L'] = bone.name
    bone = arm.edit_bones.new('temple.R')
    bone.head[:] = -0.0585, -0.0276, 0.1490
    bone.tail[:] = -0.0607, -0.0295, 0.0962
    bone.roll = 0.0650
    bone.use_connect = False
    bone.parent = arm.edit_bones[bones['forehead.R.002']]
    bones['temple.R'] = bone.name
    bone = arm.edit_bones.new('nose.L.001')
    bone.head[:] = 0.0118, -0.0966, 0.0757
    bone.tail[:] = 0.0000, -0.1193, 0.0771
    bone.roll = 0.1070
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['nose.L']]
    bones['nose.L.001'] = bone.name
    bone = arm.edit_bones.new('nose.R.001')
    bone.head[:] = -0.0118, -0.0966, 0.0757
    bone.tail[:] = -0.0000, -0.1193, 0.0771
    bone.roll = -0.1070
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['nose.R']]
    bones['nose.R.001'] = bone.name
    bone = arm.edit_bones.new('nose.004')
    bone.head[:] = 0.0000, -0.1019, 0.0733
    bone.tail[:] = 0.0000, -0.1014, 0.0633
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['nose.003']]
    bones['nose.004'] = bone.name
    bone = arm.edit_bones.new('ear.L.004')
    bone.head[:] = 0.0677, -0.0109, 0.0752
    bone.tail[:] = 0.0616, -0.0083, 0.0886
    bone.roll = 0.1518
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.L.003']]
    bones['ear.L.004'] = bone.name
    bone = arm.edit_bones.new('ear.R.004')
    bone.head[:] = -0.0677, -0.0109, 0.0752
    bone.tail[:] = -0.0616, -0.0083, 0.0886
    bone.roll = -0.1518
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['ear.R.003']]
    bones['ear.R.004'] = bone.name
    bone = arm.edit_bones.new('lid.B.L')
    bone.head[:] = 0.0237, -0.0826, 0.1058
    bone.tail[:] = 0.0319, -0.0831, 0.1050
    bone.roll = -0.1108
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.L.003']]
    bones['lid.B.L'] = bone.name
    bone = arm.edit_bones.new('lid.B.R')
    bone.head[:] = -0.0237, -0.0826, 0.1058
    bone.tail[:] = -0.0319, -0.0831, 0.1050
    bone.roll = 0.1108
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.T.R.003']]
    bones['lid.B.R'] = bone.name
    bone = arm.edit_bones.new('jaw.L')
    bone.head[:] = 0.0607, -0.0295, 0.0962
    bone.tail[:] = 0.0451, -0.0338, 0.0533
    bone.roll = 0.0871
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['temple.L']]
    bones['jaw.L'] = bone.name
    bone = arm.edit_bones.new('jaw.R')
    bone.head[:] = -0.0607, -0.0295, 0.0962
    bone.tail[:] = -0.0451, -0.0338, 0.0533
    bone.roll = -0.0871
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['temple.R']]
    bones['jaw.R'] = bone.name
    bone = arm.edit_bones.new('lid.B.L.001')
    bone.head[:] = 0.0319, -0.0831, 0.1050
    bone.tail[:] = 0.0389, -0.0826, 0.1050
    bone.roll = -0.0207
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.B.L']]
    bones['lid.B.L.001'] = bone.name
    bone = arm.edit_bones.new('lid.B.R.001')
    bone.head[:] = -0.0319, -0.0831, 0.1050
    bone.tail[:] = -0.0389, -0.0826, 0.1050
    bone.roll = 0.0207
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.B.R']]
    bones['lid.B.R.001'] = bone.name
    bone = arm.edit_bones.new('jaw.L.001')
    bone.head[:] = 0.0451, -0.0338, 0.0533
    bone.tail[:] = 0.0166, -0.0758, 0.0187
    bone.roll = 0.0458
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['jaw.L']]
    bones['jaw.L.001'] = bone.name
    bone = arm.edit_bones.new('jaw.R.001')
    bone.head[:] = -0.0451, -0.0338, 0.0533
    bone.tail[:] = -0.0166, -0.0758, 0.0187
    bone.roll = -0.0458
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['jaw.R']]
    bones['jaw.R.001'] = bone.name
    bone = arm.edit_bones.new('lid.B.L.002')
    bone.head[:] = 0.0389, -0.0826, 0.1050
    bone.tail[:] = 0.0472, -0.0781, 0.1068
    bone.roll = 0.0229
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.B.L.001']]
    bones['lid.B.L.002'] = bone.name
    bone = arm.edit_bones.new('lid.B.R.002')
    bone.head[:] = -0.0389, -0.0826, 0.1050
    bone.tail[:] = -0.0472, -0.0781, 0.1068
    bone.roll = -0.0229
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.B.R.001']]
    bones['lid.B.R.002'] = bone.name
    bone = arm.edit_bones.new('chin.L')
    bone.head[:] = 0.0166, -0.0758, 0.0187
    bone.tail[:] = 0.0236, -0.0877, 0.0519
    bone.roll = 0.1513
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['jaw.L.001']]
    bones['chin.L'] = bone.name
    bone = arm.edit_bones.new('chin.R')
    bone.head[:] = -0.0166, -0.0758, 0.0187
    bone.tail[:] = -0.0236, -0.0877, 0.0519
    bone.roll = -0.1513
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['jaw.R.001']]
    bones['chin.R'] = bone.name
    bone = arm.edit_bones.new('lid.B.L.003')
    bone.head[:] = 0.0472, -0.0781, 0.1068
    bone.tail[:] = 0.0515, -0.0692, 0.1104
    bone.roll = -0.0147
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.B.L.002']]
    bones['lid.B.L.003'] = bone.name
    bone = arm.edit_bones.new('lid.B.R.003')
    bone.head[:] = -0.0472, -0.0781, 0.1068
    bone.tail[:] = -0.0515, -0.0692, 0.1104
    bone.roll = 0.0147
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['lid.B.R.002']]
    bones['lid.B.R.003'] = bone.name
    bone = arm.edit_bones.new('cheek.B.L')
    bone.head[:] = 0.0236, -0.0877, 0.0519
    bone.tail[:] = 0.0493, -0.0691, 0.0632
    bone.roll = 0.0015
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['chin.L']]
    bones['cheek.B.L'] = bone.name
    bone = arm.edit_bones.new('cheek.B.R')
    bone.head[:] = -0.0236, -0.0877, 0.0519
    bone.tail[:] = -0.0493, -0.0691, 0.0632
    bone.roll = -0.0015
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['chin.R']]
    bones['cheek.B.R'] = bone.name
    bone = arm.edit_bones.new('cheek.B.L.001')
    bone.head[:] = 0.0493, -0.0691, 0.0632
    bone.tail[:] = 0.0568, -0.0506, 0.1052
    bone.roll = -0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.B.L']]
    bones['cheek.B.L.001'] = bone.name
    bone = arm.edit_bones.new('cheek.B.R.001')
    bone.head[:] = -0.0493, -0.0691, 0.0632
    bone.tail[:] = -0.0568, -0.0506, 0.1052
    bone.roll = 0.0000
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.B.R']]
    bones['cheek.B.R.001'] = bone.name
    bone = arm.edit_bones.new('brow.T.L')
    bone.head[:] = 0.0568, -0.0506, 0.1052
    bone.tail[:] = 0.0556, -0.0689, 0.1249
    bone.roll = 0.1990
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.B.L.001']]
    bones['brow.T.L'] = bone.name
    bone = arm.edit_bones.new('brow.T.R')
    bone.head[:] = -0.0568, -0.0506, 0.1052
    bone.tail[:] = -0.0556, -0.0689, 0.1249
    bone.roll = -0.1990
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['cheek.B.R.001']]
    bones['brow.T.R'] = bone.name
    bone = arm.edit_bones.new('brow.T.L.001')
    bone.head[:] = 0.0556, -0.0689, 0.1249
    bone.tail[:] = 0.0394, -0.0828, 0.1310
    bone.roll = 0.2372
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.T.L']]
    bones['brow.T.L.001'] = bone.name
    bone = arm.edit_bones.new('brow.T.R.001')
    bone.head[:] = -0.0556, -0.0689, 0.1249
    bone.tail[:] = -0.0394, -0.0828, 0.1310
    bone.roll = -0.2372
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.T.R']]
    bones['brow.T.R.001'] = bone.name
    bone = arm.edit_bones.new('brow.T.L.002')
    bone.head[:] = 0.0394, -0.0828, 0.1310
    bone.tail[:] = 0.0144, -0.0912, 0.1236
    bone.roll = 0.0724
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.T.L.001']]
    bones['brow.T.L.002'] = bone.name
    bone = arm.edit_bones.new('brow.T.R.002')
    bone.head[:] = -0.0394, -0.0828, 0.1310
    bone.tail[:] = -0.0144, -0.0912, 0.1236
    bone.roll = -0.0724
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.T.R.001']]
    bones['brow.T.R.002'] = bone.name
    bone = arm.edit_bones.new('brow.T.L.003')
    bone.head[:] = 0.0144, -0.0912, 0.1236
    bone.tail[:] = 0.0003, -0.0905, 0.1125
    bone.roll = -0.0423
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.T.L.002']]
    bones['brow.T.L.003'] = bone.name
    bone = arm.edit_bones.new('brow.T.R.003')
    bone.head[:] = -0.0144, -0.0912, 0.1236
    bone.tail[:] = -0.0003, -0.0905, 0.1125
    bone.roll = 0.0423
    bone.use_connect = True
    bone.parent = arm.edit_bones[bones['brow.T.R.002']]
    bones['brow.T.R.003'] = bone.name

    bpy.ops.object.mode_set(mode='OBJECT')
    pbone = obj.pose.bones[bones['face']]
    pbone.rigify_type = 'game.super_face'
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.T.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.B.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['jaw']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.T.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.B.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['forehead.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['forehead.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['eye.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['eye.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.T.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.T.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['teeth.T']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['teeth.B']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.T.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.B.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['chin']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.T.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lip.B.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['forehead.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['forehead.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.T.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.T.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['chin.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.L.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.R.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.L.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.L.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.R.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.R.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['forehead.L.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['forehead.R.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['tongue.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.L.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.R.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.L.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.L.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.B.R.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.T.R.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['temple.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['temple.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['nose.004']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.L.004']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['ear.R.004']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['jaw.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['jaw.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['jaw.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['jaw.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.L.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.R.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['chin.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['chin.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.L.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['lid.B.R.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.B.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.B.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.B.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['cheek.B.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.L']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.R']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.L.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.R.001']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.L.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.R.002']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.L.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'
    pbone = obj.pose.bones[bones['brow.T.R.003']]
    pbone.rigify_type = ''
    pbone.lock_location = (False, False, False)
    pbone.lock_rotation = (False, False, False)
    pbone.lock_rotation_w = False
    pbone.lock_scale = (False, False, False)
    pbone.rotation_mode = 'QUATERNION'

    bpy.ops.object.mode_set(mode='EDIT')
    for bone in arm.edit_bones:
        bone.select = False
        bone.select_head = False
        bone.select_tail = False
    for b in bones:
        bone = arm.edit_bones[bones[b]]
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        arm.edit_bones.active = bone
