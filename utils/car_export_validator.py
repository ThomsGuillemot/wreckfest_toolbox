import bpy


def get_collision_spheres(context: bpy.types.Context):
    spheres = []
    for obj in bpy.data.objects:
        if obj.name.lower().startswith("collision_sphere"):
            spheres.append(obj)

    return spheres



