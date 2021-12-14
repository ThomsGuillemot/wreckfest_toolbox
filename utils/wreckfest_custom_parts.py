
import bpy
import array
import collections
from . import blender_scene_tools


class WFCustomParts():

    part_name_suffix = "#part"
    wheel_name_prefix = "tire_"
    root_collection_name = "#parts"


"""
Return a string list like : [part_name][part_number]
This function will raise a ValueError if the part_name is not formated like : part_name#part0
"""
def get_custom_part_name_and_number(part_name: str):
    if WFCustomParts.part_name_suffix not in part_name:
        #print("NO #part in the name. The part name is not correct. See the function doc. part_name = " + part_name)
        raise ValueError

    # Split the part name into [part_name][number]
    splitted_part_name = part_name.split(WFCustomParts.part_name_suffix)
    if len(splitted_part_name) != 2:
        #print("NO NUMBER in the name. The part name is not correct. See the function doc. part_name = " + part_name)
        raise ValueError

    try:
        splitted_part_name[1] = int( splitted_part_name[1] )
    except ValueError:
        #print("NUMBER IS NOT A NUMBER in the name. The part name is not correct. See the function doc. part_name = " + part_name)
        raise ValueError

    return splitted_part_name


def get_is_related_custom_part(part_name: str, other_part_name: str) -> bool:
    # If the part already is a custom part with a number
    if part_name == other_part_name:
        return False

    splitted_part_name = part_name.split(WFCustomParts.part_name_suffix)[0]
    try:
        splitted_other_part_name = get_custom_part_name_and_number(other_part_name)
    except ValueError:
        return False

    return splitted_part_name == splitted_other_part_name[0]


def format_custom_part_name(obj_name: str, part_index: str) -> str:
    return obj_name.split(WFCustomParts.part_name_suffix)[0] + WFCustomParts.part_name_suffix + part_index

"""Return an array with all the blender object 
that are related to the custom part given in parameter"""

def get_related_custom_parts(part_name: str) -> collections.Iterable[bpy.types.Object]:
    #iterate through every objects and return an array with all the parts in it
    custom_parts = []
    for obj in bpy.context.scene.objects:
        if blender_scene_tools.get_is_exportable(obj):
            if get_is_related_custom_part(part_name, obj.name):
                custom_parts.append(obj)
    
    return custom_parts

"""Return a sorted array of all the objects that correspond to the custom part"""
def get_related_custom_parts(part_name: str) -> collections.Iterable[bpy.types.Object]:
    #iterate through every objects and return an array with all the parts in it
    custom_parts = []
    for obj in bpy.context.scene.objects:
        if blender_scene_tools.get_is_exportable(obj):
            if get_is_related_custom_part(part_name, obj.name) or part_name == obj.name:
                custom_parts.append(obj)

    return custom_parts