import bpy


# Create a Wreckfest menu on the right panel of 3D view
class WFTB_PT_wreckfest_toolbox_panel(bpy.types.Panel):
    """Wreckfest modding Toolbox : A bunch of tools to speed up your wreckfest modding experience !"""
    bl_idname = "WFTB_PT_wreckfest_toolbox_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Wreckfest"
    bl_context = "objectmode"
    bl_label = "Wreckfest Modding Tools"

    def draw(self, context):
        """Draw the UI."""
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        props = context.window_manager.WFTBPanel
        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.scale_x = 1.5
        row.scale_y = 1.5
        row.prop(props, "panel_enums", icon_only=True, expand=True)

        if props.panel_enums == "EXPORT":
            row.label(text="Export")

            # Import/Export
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Export :", icon="EXPORT")
            row = box.row(align=True)
            row.prop(prefs, "apply_modifiers")
            # TODO : Implement this
            # row.prop(prefs, "auto_split_edge")
            row = box.row(align=True)
            # Display the Bake option only if the export path was set before
            # TODO : Check if the path is valid
            # TODO : Use a string file to avoid typing "wftb_bgo_export_path" every time
            if context.scene.get("wftb_bgo_export_path"):
                row.label(text=context.scene.get("wftb_bgo_export_path"))
            row = box.row(align=True)
            if context.scene.get("wftb_bgo_export_path"):
                row.operator("wftb.export_bgo", text="Direct Export", icon="EXPORT")
            row.operator("wftb.export_bgo_with_dialog", text="Set Path & Export", icon="FILEBROWSER")
            row.scale_y = 1.5

        elif props.panel_enums == "SETTINGS":
            row.label(text="Addon Settings")

            # Paths
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Paths :", icon="FILE_FOLDER")
            row = box.row(align=True)
            row.prop(prefs, 'wf_path')
            # TODO : Implement
            # row.prop(prefs, 'export_message_level')

class WFTB_PT_wreckfest_material_panel(bpy.types.Panel):
    """Add a Wreckfest menu to the Material Panel"""
    bl_idname = "WFTB_PT_wreckfest_material_panel"
    bl_label = "Wreckfest Material Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'

    def draw(self, context):
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        row = self.layout.row(align=True)
        row.label(text="Physical Material")
        row.prop(prefs, "wf_physical_material_list")
        row.operator("wftb.set_physical_material")

class WFTB_MT_object_context_menu(bpy.types.Menu):
    """Add a wreckfest menu to the Right Click"""
    bl_idname = "WFTB_MT_object_context_menu"
    bl_label = "Wreckfest"

    def draw(self, context):
        layout = self.layout

        if getattr(bpy.types, "WFTB_OT_toggle_wreckfest_custom_data", False):
            layout.operator("wftb.toggle_wreckfest_custom_data", icon="MODIFIER")
