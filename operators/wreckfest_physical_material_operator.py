import bpy


class WFTB_OT_set_physical_material(bpy.types.Operator):
    bl_idname = "wftb.set_physical_material"
    bl_label = "Set Physical Material"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.context.active_object.active_material is None:
            return False
        return True

    def execute(self, context):
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        # prefs.refresh_physical_material_list()
        if prefs.get("wf_physical_material_list") is None:
            return {'CANCELLED'}

        material_name = bpy.context.active_object.active_material.name
        name_index = material_name.find('#')
        if name_index != -1:
            material_name = material_name[:name_index]

        material_name += "#"
        material_name += prefs.physical_materials[prefs.get("wf_physical_material_list")][0]
        # Change the name of the material again
        bpy.context.active_object.active_material.name = material_name

        return {'FINISHED'}

    def draw(self, context):
        # Draw a list of physical materials
        column = self.layout.column(align=True)
        column.label("Set Physical Material")
        return