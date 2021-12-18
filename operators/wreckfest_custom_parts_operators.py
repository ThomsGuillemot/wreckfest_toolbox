import bpy

from wreckfest_toolbox.utils.wreckfest_custom_parts import format_custom_part_name, get_custom_part_name_and_number, get_related_custom_parts


class WFTB_OT_set_custom_part(bpy.types.Operator):
    """Change the name of the active object to become a custom part
    If a custom part already exist, it will adjust the id of the part
    ex : Selected hood -> if a part already named hood#part_0 the selected one will become hood#part1"""
    bl_idname = "wftb.set_custom_part"
    bl_label = "Set Custom Part"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if bpy.context.active_object is None:
            return False

        return True

    def execute(self, context):
        # Rename the object with #partxx suffix
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        # Get the possible custom parts
        current_object = bpy.context.active_object
        related_custom_parts = get_related_custom_parts(current_object.name)
        # Generate the index of the part by getting the last index of related parts
        part_index = 0
        for custom_part in related_custom_parts:
            index = get_custom_part_name_and_number(custom_part.name)[1] + 1
            if index > part_index :
                part_index = index

        current_object.name = format_custom_part_name(current_object.name, str(part_index))

        return {'FINISHED'}


class WFTB_OT_swith_custom_part_visibility(bpy.types.Operator):
    """Show the Custom part that have this index, and hide the other related parts"""
    bl_idname = "wftb.swith_custom_part_visibility"
    bl_label = "Switch Custom Part Visibility"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if bpy.context.active_object is None:
            return False

        #if not a custom part
        try:
            get_custom_part_name_and_number(bpy.context.active_object.name)
        except ValueError:
            return False
        
        return True

    # TODO : Display a menu to select the part number we want to display
    def execute(self, context):
        # Rename the object with #partxx suffix
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        # Get the possible custom parts
        current_object = bpy.context.active_object
        #if not a custom part
        try:
            get_custom_part_name_and_number(bpy.context.active_object.name)
        except ValueError:
            return {'CANCELLED'}

        related_custom_parts = get_related_custom_parts(current_object.name)

        for custom_part in related_custom_parts:
            custom_part.hide_set(True)

        return {'FINISHED'}

# TODO : Add a "Custom Part Cleaner" operator that remove "holes" in custom parts numbers

# TODO : Add a "Sort Custom Part By Collection" operator that sort all the custom parts in sub collections of a #parts collection