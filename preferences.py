"""Addon preferences that are saved inbetween sesions."""

import bpy


def preference_save(self, context):
    bpy.ops.wm.save_userpref()

class WreckfestPanelContext(bpy.types.PropertyGroup):
    """Properties that can be changed in panel"""
    panel_enums: bpy.props.EnumProperty(
        items=(
            ("EXPORT", "Export", "Export", "EXPORT", 0),
            ("SETTINGS", "Addon Settings", "Addon Settings", "PREFERENCES", 1),
        ),
        name="Addon Panels",
    )


class WreckfestToolboxAddonPreference(bpy.types.AddonPreferences):
    bl_idname = "wreckfest_toolbox"

    wreckfest_message_level = [
        ("VERBOSE", "Verbose", "", "", 1),
        ("WARNING", "Warning", "", "", 2),
        ("ERROR", "Error", "", "", 3)
    ]

    # Wreckfest path
    wf_path: bpy.props.StringProperty(
        name="Wreckfest Path",
        subtype="DIR_PATH",
        default=R"C:\Program Files (x86)\Steam\steamapps\common\Wreckfest",
        update=preference_save,
    )

    # Build assets tool path
    wf_build_asset_subpath: bpy.props.StringProperty(
        name="Wreckfest Build Asset Path",
        subtype='FILE_PATH',
        default=R"\tools\build_asset.bat"
    )

    export_message_level: bpy.props.EnumProperty(
        name="Export Message Level",
        items=wreckfest_message_level
    )

    apply_modifiers: bpy.props.BoolProperty(
        name="Apply Modifier",
        default=True,
        description="Apply modifier to the exported models"
    )

    auto_split_edge: bpy.props.BoolProperty(
        name="Split Edges",
        default=True,
        description="Add a Split edge modifier for sharp edges (marked) on export"
    )




