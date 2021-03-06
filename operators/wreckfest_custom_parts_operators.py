import bpy
from wreckfest_toolbox.utils.wreckfest_custom_parts_properties import CustomPartsProperties

class WFTB_OT_use_custom_parts(bpy.types.Operator):
    bl_idname = "wftb.use_custom_parts"
    bl_label = "Use Wreckfest Custom Parts"
    bl_description = "Car Mod Oriented Tool" \
                     "Add the Wreckfest Custom Part objects in the defined collection." \
                     "If no collection is defined, a new collection will be created." \
                     "The collection will be splitted in sub collection nammed part#nameOfThePart" \
                     "Where the name of the part is defined from the object name"
    bl_options = {"UNDO_GROUPED"}

    def execute(self, context):
        # Get or create the the custom part properties
        CustomPartsProperties.register_custom_parts_properties(context)

        # Check if the scene already have a collection with the good name
        # custom_part_properties.custom_part_collection = CustomPartsProperties.get_or_create_collection(
        #     custom_part_properties.collection_name)
        # bpy.ops.wftb.refresh_custom_part_manager()
        return {'FINISHED'}


class WFTB_OT_refresh_custom_parts_manager(bpy.types.Operator):
    bl_idname = "wftb.refresh_custom_part_manager"
    bl_label = "Refresh Custom Parts"

    def execute(self, context):
        # Check if custom parts property was initialized
        if not CustomPartsProperties.is_custom_parts_properties_valid(context):
            return {'CANCELLED'}
        # Fetch the custom Parts
        self.__update_custom_parts_collection(CustomPartsProperties.fetch_custom_parts(), context)
        return {'FINISHED'}

    @staticmethod
    # Manage the collections
    def __update_custom_parts_collection(custom_parts, context):
        # Create a collection if it don't exist
        custom_parts_collection = context.scene.wftb_custom_parts_properties.custom_parts_collection
        for part_name, parts in custom_parts.items():
            # Check if the collection exist
            collection_name = 'part#' + part_name
            part_collection = CustomPartsProperties.get_or_create_collection(collection_name, custom_parts_collection)
            for part in parts:
                if part.name not in part_collection.objects:
                    part_collection.objects.link(part)


class WFTB_OT_set_custom_part(bpy.types.Operator):
    """Change the name of selected object to become a custom part"""
    bl_idname = "wftb.set_custom_part"
    bl_label = "Set Custom Part"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if bpy.context.selected_objects is None:
            return False

        return True

    def execute(self, context):
        # Rename the object with #partxx suffix
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        # Refresh the custom parts

        return {'FINISHED'}


class WFTB_OT_swith_custom_part(bpy.types.Operator):
    """Show the Custom part that have this number, and hide the other related parts"""
    bl_idname = "wftb.switch_custom_part"
    bl_label = "Switch Custom Part"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "custom_part_name"

    custom_part_name: bpy.props.StringProperty(
        name="Custom Part Name",
        options={'HIDDEN'}
    )

    def execute(self, context):
        custom_parts = CustomPartsProperties.fetch_custom_parts()
        part_name = CustomPartsProperties.get_custom_part_name(self.custom_part_name)
        if part_name in custom_parts.keys():
            for part in custom_parts[part_name]:
                if part.name in context.view_layer.objects:
                    part.hide_set(part.name != self.custom_part_name)
            return {'FINISHED'}
        elif len(part_name) == 0:
            for custom_part, parts in custom_parts.items():
                for part in parts:
                    if part.name in context.view_layer.objects:
                        part.hide_set("#part0" not in part.name)
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

