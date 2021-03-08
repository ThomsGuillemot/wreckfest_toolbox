import bpy
from mathutils import Vector



class WFTB_OT_car_export_validator(bpy.types.Operator):
    bl_idname = "wftb.car_export_validator"
    bl_label = "Car : Validate scene"

    def execute(self, context):

        return{'FINISHED'}
        
    @staticmethod
    def move_gameplay_object_to_collection(contex:bpy.types.Context, obj:bpy.types.Object, collection_name:str):
        if collection_name in bpy.data.collections and obj.name not in bpy.data.collections[collection_name].objects:
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
                
            collection = bpy.data.collections[collection_name]
            collection.objects.link(obj)


class WFTB_OT_create_car_collisions(bpy.types.Operator):
    """Check if the scene contain the top & bottom collision (objects named : collision_bottom & collision_top)
    If not, the operator will create them. And finally the operator will check if the good Custom Data was set"""
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
        
        WFTB_OT_car_export_validator.move_gameplay_object_to_collection(context, cube, "Collisions")

        if 'collision_top' not in bpy.data.objects:
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.active_object
            cube.name = 'collision_top'
            bpy.context.active_object.dimensions = [body.dimensions.x, body.dimensions.y/2, body.dimensions.z/2]
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

        collision_top = bpy.data.objects['collision_top']

        # TODO : Use WreckfestCustomDataGroup property instead of hard coding it
        collision_top["WF_IsCollisionModel"] = 1
        
        WFTB_OT_car_export_validator.move_gameplay_object_to_collection(context, cube, "Collisions")

        return {'FINISHED'}

class WFTB_OT_create_car_proxy(bpy.types.Operator):
    """Create an object that will be treated as proxy by Wreckfest Build Asset"""
    bl_idname="wftb.create_car_proxy"
    bl_label="Create Car Proxy"
    bl_options={"UNDO"}
    
    proxy_name: bpy.props.StringProperty(name="Proxy Name", default="body")
    
    def execute(self, context):
    
        if 'body' not in bpy.data.objects:
                return {'CANCELLED'}

        body = bpy.data.objects['body']
        # Create a cube
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        cube.name = "proxy_" + self.proxy_name
        context.active_object.dimensions = body.dimensions
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        context.active_object["WF_IsCollisionModel"] = True
        
        WFTB_OT_car_export_validator.move_gameplay_object_to_collection(context, cube, "Proxies")
            
        return {'FINISHED'}
        
    def draw(self, context):
        self.layout.prop(self, "proxy_name")