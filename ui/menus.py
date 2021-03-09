import bpy
from wreckfest_toolbox.utils.wreckfest_custom_parts_properties import CustomPartsProperties

class WreckfestPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Wreckfest"
    bl_options = {"DEFAULT_CLOSED"}


# Create a Wreckfest menu on the right panel of 3D view
class WFTB_PT_wreckfest_toolbox_panel(WreckfestPanel, bpy.types.Panel):
    """Wreckfest modding Toolbox : A bunch of tools to speed up your wreckfest modding experience !"""
    bl_idname = "WFTB_PT_wreckfest_toolbox_panel"
    bl_label = "Wreckfest Modding Tools"

    def draw(self, context):
        """Draw the UI."""
        props = context.window_manager.WFTBPanel
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.scale_x = 1.5
        row.scale_y = 1.5
        row.prop(props, "panel_enums", icon_only=True, expand=True)


class WFTB_PT_wreckfest_custom_parts_panel(WreckfestPanel, bpy.types.Panel):
    bl_idname = "WFTB_PT_wreckfest_custom_parts_panel"
    bl_label = "Wreckfest Custom Parts"
    bl_parent_id = "WFTB_PT_wreckfest_toolbox_panel"

    @classmethod
    def poll(cls, context:bpy.types.Context):
        props = context.window_manager.WFTBPanel
        return props.panel_enums == "CAR_TOOLS"

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        row = layout.row(align=True)
        op = row.operator("wftb.switch_custom_part", text="Show all #parts0")
        op.custom_part_name = ""
        custom_parts = CustomPartsProperties.fetch_custom_parts()
        for custom_part_name, part_objects in custom_parts.items():
            inner_box = layout.box()
            row = inner_box.row(align=True)
            op = row.operator("wftb.switch_custom_part", text=custom_part_name + " : Empty", icon="CANCEL")
            op.custom_part_name = custom_part_name
            row = inner_box.row(align=True)
            c = 0
            for part in part_objects:
                op = row.operator("wftb.switch_custom_part", text=str(c))
                op.custom_part_name = part.name
                c += 1
                if ((c) % 5) == 0:
                    row = inner_box.row(align=True)


class WFTB_PT_wreckfest_export_panel(WreckfestPanel, bpy.types.Panel):
    bl_idname = "WFTB_PT_wreckfest_export_panel"
    bl_label = "Export Scene"
    bl_parent_id = "WFTB_PT_wreckfest_toolbox_panel"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        props = context.window_manager.WFTBPanel
        return props.panel_enums == "EXPORT"

    def draw(self, context: bpy.types.Context):
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        layout = self.layout
        # Export
        row = layout.row(align=True)
        row.label(text="Export :", icon="EXPORT")
        row = layout.row(align=True)
        row.prop(prefs, "apply_modifiers")
        row.prop(prefs, "build_after_export")
        # TODO : Implement this
        # row.prop(prefs, "auto_split_edge")
        row = layout.row(align=True)
        # Display the Bake option only if the export path was set before
        # TODO : Check if the path is valid
        # TODO : Use a string file to avoid typing "wftb_bgo_export_path" every time
        if context.scene.get("wftb_bgo_export_path"):
            row.label(text=context.scene.get("wftb_bgo_export_path"))
        row = layout.row(align=True)
        if context.scene.get("wftb_bgo_export_path"):
            row.operator("wftb.export_bgo", text="Direct Export", icon="EXPORT")
        row.operator("wftb.export_bgo_with_dialog", text="Set Path & Export", icon="FILEBROWSER")
        row.scale_y = 2


class WFTB_PT_wreckfest_car_export_validator_panel(WreckfestPanel, bpy.types.Panel):
    bl_idname = "WFTB_PT_wreckfest_car_export_validator_panel"
    bl_label = "Car : Validate Scene"
    bl_parent_id = "WFTB_PT_wreckfest_toolbox_panel"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        props = context.window_manager.WFTBPanel
        return props.panel_enums == "EXPORT"

    def draw_header(self, context: bpy.types.Context):
        self.layout.label(text="", icon="AUTO")
        self.layout.label(text="", icon="CHECKMARK")

    def draw(self, context: bpy.types.Context):
        # Collision Spheres
        row = self.layout.row()
        op = row.operator("wftb.validate_collision_spheres", icon="MESH_UVSPHERE")
        row = self.layout.row()
        row.prop(op, "use_collection")


class WFTB_PT_wreckfest_toolbox_settings_panel(WreckfestPanel, bpy.types.Panel):
    bl_idname = "WFTB_PT_wreckfest_toolbox_settings_panel"
    bl_label = "Addon Settings"
    bl_parent_id = "WFTB_PT_wreckfest_toolbox_panel"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        props = context.window_manager.WFTBPanel
        return props.panel_enums == "SETTINGS"

    def draw(self, context: 'Context'):
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        layout = self.layout
        # Paths
        row = layout.row(align=True)
        row.label(text="Paths :", icon="FILE_FOLDER")
        row = layout.row(align=True)
        row.prop(prefs, 'wf_path')


class WFTB_PT_wreckfest_material_panel(bpy.types.Panel):
    """Add a Wreckfest menu to the Material Panel"""
    bl_idname = "WFTB_PT_wreckfest_material_panel"
    bl_label = "Wreckfest Material Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        row = self.layout.row(align=True)
        row.prop(prefs, "wf_physical_material_list", text="Physical Material")
        row = self.layout.row(align=True)
        row.operator("wftb.set_physical_material", text="Apply", icon='CHECKMARK')


class WFTB_MT_object_context_menu(bpy.types.Menu):
    """Add a wreckfest menu to the Right Click"""
    bl_idname = "WFTB_MT_object_context_menu"
    bl_label = "Wreckfest"

    def draw(self, context):
        layout = self.layout

        if getattr(bpy.types, "WFTB_OT_toggle_wreckfest_custom_data", False):
            layout.operator("wftb.toggle_wreckfest_custom_data", icon="MODIFIER")
        if getattr(bpy.types, "WFTB_OT_set_custom_part", False):
            layout.operator("wftb.set_custom_part", icon="PRESET")
