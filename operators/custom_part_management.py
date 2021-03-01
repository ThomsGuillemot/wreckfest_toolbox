import bpy


class CustomPartManager:

    def __init__(self):
        self.custom_parts = {"no_custom_parts": []}

    def update_custom_parts(self, context):
        self.custom_parts = {}
        for obj in bpy.context.scene.objects:
            if "#part" in obj.name:
                part_name = self.get_object_custom_part_name(obj)
                if part_name in self.custom_parts:
                    self.custom_parts[part_name].append(obj)
                else:
                    self.custom_parts[part_name] = [obj]

        for part, parts in self.custom_parts.items():
            parts.sort(key=self.sort_part)

    # Manage the collections
    def update_custom_parts_collection(self):
        # Create a collection if it don't exist
        custom_parts_collection = self.get_or_create_collection('WF Custom Parts')
        for part_name, parts in self.custom_parts.items():
            # Check if the collection exist
            collection_name = 'part#' + part_name
            part_collection = self.get_or_create_collection(collection_name, custom_parts_collection)
            for part in parts:
                if part.name not in part_collection.objects:
                    part_collection.objects.link(part)




    @staticmethod
    def sort_part(obj):
        return obj.name

    @staticmethod
    def get_object_custom_part_name(obj):
        return CustomPartManager.get_custom_part_name(obj.name)

    @staticmethod
    def get_custom_part_name(obj_name):
        if "#part" not in obj_name:
            return obj_name

        return obj_name[0:obj_name.index("#part")]

    def is_custom_part(self, obj):
        return self.get_object_custom_part_name(obj) in self.custom_parts.keys()

    @staticmethod
    def get_or_create_collection(collection_name, parent: bpy.types.Collection = None):
        new_collection = None
        if collection_name in bpy.data.collections:
            new_collection = bpy.data.collections[collection_name]

        else:
            new_collection = bpy.data.collections.new(collection_name)

        if parent is None:
            parent = bpy.context.scene.collection

        if collection_name not in parent.children:
            parent.children.link(new_collection)

        return new_collection

class WFTB_OT_refresh_custom_part_manager(bpy.types.Operator):
    """Init the custom parts related data"""
    bl_idname = "wftb.refresh_custom_part_manager"
    bl_label = "Refresh Custom Parts"

    def execute(self, context):
        prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        # Refresh the data from
        prefs.custom_part_manager.update_custom_parts(context)
        # Create the collection
        prefs.custom_part_manager.update_custom_parts_collection()
        return {'FINISHED'}


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
        prefs.custom_part_manager.update_custom_parts(context)

        for obj in bpy.context.selected_objects:
            if CustomPartManager.is_custom_part(obj):
                pass
            else:

                obj.name += '#part'

        return {'FINISHED'}


class WFTB_OT_swith_custom_part(bpy.types.Operator):
    bl_idname = "wftb.switch_custom_part"
    bl_label = "Switch Custom Part"
    bl_options = {'REGISTER', 'UNDO'}
    bl_property = "custom_part_name"

    custom_part_name: bpy.props.StringProperty(
        name="Custom Part Name",
        options={'HIDDEN'}
    )

    def execute(self, context):
        cpm = bpy.context.preferences.addons["wreckfest_toolbox"].preferences.custom_part_manager
        if cpm is None:
            return {'CANCELLED'}
        part_name = CustomPartManager.get_custom_part_name(self.custom_part_name)
        if part_name in cpm.custom_parts.keys():
            for part in cpm.custom_parts[part_name]:
                visibility = part.name != self.custom_part_name
                print(part.name, visibility)
                part.hide_set(visibility)

        return {'FINISHED'}
