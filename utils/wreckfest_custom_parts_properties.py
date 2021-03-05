import ast

import bpy
import idprop


def poll_custom_part_property(self, object):
    return self is CustomPartsProperties


class CustomPartsProperties(bpy.types.PropertyGroup):
    name = "Custom Part Properties"

    custom_parts_collection: bpy.props.PointerProperty(
        name="Custom Part Collection",
        type=bpy.types.Collection
    )

    wheel_name_prefix: bpy.props.StringProperty(
        name="Wheel name prefix",
        default="tire_",
        description="The wheel name prefix.\r\n"
                    "Usually tire_ or wheel_.\r\n"
                    "(ie : tire_fl#part0)"
    )

    """Look through the scene to find the object with a name that fit with Wreckfest Custom Part naming convetion
    Then return it into a dictionnary under the form 
    {
        key:Custom Part Name
        Value:List[Custom Part Object #0, Custom Part Object #1]
    }
    """

    @staticmethod
    def fetch_custom_parts():
        custom_parts = {}
        for obj in bpy.context.scene.objects:
            if "#part" in obj.name:
                part_name = CustomPartsProperties.get_object_custom_part_name(obj)
                if part_name in custom_parts:
                    custom_parts[part_name].append(obj)
                else:
                    custom_parts[part_name] = [obj]

        for part, parts in custom_parts.items():
            parts.sort(key=CustomPartsProperties.sort_part)

        return custom_parts

    @staticmethod
    def sort_part(obj):
        return obj.name

    """Return the Custom Part name from the name. Basically remove the #partx suffix"""

    @staticmethod
    def get_custom_part_name(obj_name):
        if "#part" not in obj_name:
            return obj_name

        return obj_name[0:obj_name.index("#part")]

    """Return the Custom Part name of the object. Basically remove the #partx suffix"""

    @staticmethod
    def get_object_custom_part_name(obj):
        return CustomPartsProperties.get_custom_part_name(obj.name)

    """Look in the scene if a collection have the given name, if yes, return it.
    Else Create a new collection with the given name.
    If a parent is given, the new collection will be 
    linked to the given parent. Else, the collection will be linked to the scene root collection"""

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

    @staticmethod
    def register_custom_parts_properties(context: bpy.types.Context):
        scene = context.scene
        # If the property don't exist
        if scene.get("wftb_custom_parts_properties", None) is None:
            print("Register Custom Parts Property")
            bpy.types.Scene.wftb_custom_parts_properties = bpy.props.PointerProperty(
                name="WFTB Custom Parts Properties",
                type=CustomPartsProperties
            )
        # if the property is not of the good type
        elif isinstance(scene["wftb_custom_parts_properties"], idprop.types.IDPropertyGroup):
            serialized_custom_parts_properties = scene["wftb_custom_parts_properties"].to_dict()
            bpy.types.Scene.wftb_custom_parts_properties = bpy.props.PointerProperty(
                name="WFTB Custom Parts Properties",
                type=CustomPartsProperties
            )
            if 'custom_parts_collection' in serialized_custom_parts_properties:
                scene.wftb_custom_parts_properties.custom_part_collection = \
                    serialized_custom_parts_properties['custom_parts_collection']
            if 'wheel_name_prefix' in serialized_custom_parts_properties:
                scene.wftb_custom_parts_properties.wheel_name_prefix = \
                    serialized_custom_parts_properties['wheel_name_prefix']

            """
            elif scene["wftb_custom_parts_properties"].rna_type.name != "CustomPartsProperties":
            print("Restore Custom Parts Property")
            serialized_custom_parts_properties = ast.literal_eval(scene.get("wftb_custom_parts_properties"))
            scene.wftb_custom_parts_properties = bpy.props.PointerProperty(
                name="WFTB Custom Parts Properties",
                type=CustomPartsProperties
            )
            scene.wftb_custom_parts_properties.custom_part_collection = \
                serialized_custom_parts_properties['custom_part_collection']
            scene.wftb_custom_parts_properties.wheel_name_prefix = \
                serialized_custom_parts_properties['collection_name']
        """

        return context.scene.wftb_custom_parts_properties

    @staticmethod
    def is_custom_parts_properties_valid(context: bpy.types.Context):
        if context.scene.get("wftb_custom_parts_properties", None) is None or \
                not hasattr(bpy.types.Scene, "wftb_custom_parts_properties"):
            return False
        return isinstance(context.scene.wftb_custom_parts_properties, CustomPartsProperties)
