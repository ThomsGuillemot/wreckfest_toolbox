import bpy


"""Look in the scene if a collection have the given name, if yes, return it.
Else Create a new collection with the given name.
If a parent is given, the new collection will be 
linked to the given parent. Else, the collection will be linked to the scene root collection"""

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


def get_is_exportable(blender_object: bpy.types.Object):
    for collection in blender_object.users_collection:
        if collection.name.endswith("#exclude"):
            return False
    return True
