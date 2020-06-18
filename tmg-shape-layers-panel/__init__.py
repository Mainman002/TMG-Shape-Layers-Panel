import bpy

from . sculpt_op import *
from . userprefs import *

from bpy.props import *
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, PropertyGroup, AddonPreferences

bl_info = {
    "name": "TMG_Shape_Layers_Panel",
    "author": "Johnathan Mueller",
    "descrtion": "Sculpt using shape keys as layers.",
    "blender": (2, 80, 0),
    "version": (0, 2, 4),
    "location": "View3D (EditMode) > Sidebar > Edit Tab",
    "warning": "",
    "category": "Sculpt"
}

#### shows the settings for shape keys #########################
bpy.types.Scene.shape_settings_menu = BoolProperty(name="Shape Key Settings",
                                                           default=False,
                                                           description="Shows the menu settings for shape key layers."
                                                           )

#### Sculpt Shape Keys Panel Mode Switch #########################
bpy.types.Scene.sculpt_shape_keys_icon_view = BoolProperty(name="Icon View",
                                                           default=False,
                                                           description="Switches the shape key panel from labeled buttons, to icons."
                                                           )


#### Sculpt Keframe Timeline #################################

bpy.types.Scene.keyframe_timeline = BoolProperty(name="Keframe Timeline",
                                                           default=False,
                                                           description="Keyframes timeline when you add a shape layer."
                                                           )


#### Sculpt Show Selected Shape Layer #########################
bpy.types.Scene.sculpt_single_shape_layer = BoolProperty(name="Only show selected shape layer.",
                                                         default=False,
                                                         update=sculpt_single_shape_layer_changed,
                                                         description="Only show selected shape layer.")


classes = (
    # Preferances Panel
    TMG_User_Preferences,
    Sculpt_OT_Show_TMG_Addon_Prefs,

    # Panels
    Sculpt_Shape_Layers_Panel,

    # Sculpt Operators
    Sculpt_OT_ADD_New_Shape_Layer,
    Sculpt_OT_Remove_Selected_Layer,
    Sculpt_OT_Shape_Key_Hide_Others,
    Sculpt_OT_Keyframe_Shape_Keys,
    Sculpt_OT_Clear_All_Keyframes,
    Sculpt_OT_Merge_Shape_Keys,
    Sculpt_OT_Apply_Shape_Keys,
)


def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)

def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)

if __name__ == "__main__":
    register()
