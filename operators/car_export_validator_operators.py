import bpy
from mathutils import Vector



class WFTB_OT_car_export_validator(bpy.types.Operator):
    bl_idname = "wftb.car_export_validator"
    bl_label = "Car : Validate scene"

    def execute(self, context):

        return{'FINISHED'}


class WFTB_OT_create_car_collisions(bpy.types.Operator):
    """Check if the scene contain the top & bottom collision (objects named : collision_bottom & collision_top)"""
    bl_idname = "wftb.create_car_collisions"
    bl_label = "Car : Validate/Create collisions"

    def execute(self, context):
        if 'body' not in bpy.data.objects:
            return {'CANCELLED'}

        body = bpy.data.objects['body']

        if 'collision_bottom' not in bpy.data.objects:
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.active_object
            cube.name = 'collision_bottom'
            bpy.context.active_object.dimensions = body.dimensions
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        collision_bottom = bpy.data.objects['collision_bottom']

        # TODO : Use WreckfestCustomDataGroup property instead of hard coding it
        collision_bottom["WF_IsCollisionModel"] = 1

        if 'collision_top' not in bpy.data.objects:
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.active_object
            cube.name = 'collision_top'
            bpy.context.active_object.dimensions = [body.dimensions.x, body.dimensions.y/2, body.dimensions.z/2]
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        collision_top = bpy.data.objects['collision_top']

        # TODO : Use WreckfestCustomDataGroup property instead of hard coding it
        collision_top["WF_IsCollisionModel"] = 1

        return {'FINISHED'}
