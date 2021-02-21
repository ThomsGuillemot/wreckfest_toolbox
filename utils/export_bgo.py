# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2016 Dummiesman
# Copyright (c) 2020 TheSpacebarRider, Mazay
#
# This software is released under the MIT License.
# http://opensource.org/licenses/MIT
#
# ##### END MIT LICENSE BLOCK #####

import os, time, struct, bpy, bmesh, mathutils, bpy_extras
from bpy_extras.io_utils import ExportHelper
from mathutils import *
import os.path as path
from math import radians

from .material_node import WreckfestWrapperNode
from .. import preferences

wf_custom_data = {
    "IsCollisionModel",
    "OtherWay",
}

wf_slots = {
    'ao_image': 0,
    'base_color_image': 1,
    'specular_color_image': 2,
    'specular_level_image': 3,
    'glossiness_image': 4,
    'self_illumination_image': 5,
    'opacity_image': 6,
    'filter_color_image': 7,
    'bump_image': 8,
    'mrs_image': 9,
    'refraction_image': 10,
    'displacement_image': 11
}
wf_bsdf_slots = {
    # Ambiant Oclusion
    'Transmission': 0,
    # Diffuse / Base Color
    'Base Color': 1,
    # Specular Color
    'Specular': 2,
    # Specular Level
    'Specular Tint': 3,
    # Glossiness
    'Roughness': 4,
    # Self Illumination
    'Emission': 5,
    # Opacity
    'Alpha': 6,
    # Filter Color
    'Anisotropic': 7,
    # Bump
    'Normal': 8,
    # Reflection
    'Clearcoat': 9,
    # Refraction
    'IOR': 10,
    # Displacement
    'Tangent': 11
}

# Add a scene property to store the export path
bpy.types.Scene.wftb_bgo_export_path = bpy.props.StringProperty(
    name="BGO",
    subtype='FILE_PATH'
)


class WFTB_OP_export_bgo_with_dialog(bpy.types.Operator, ExportHelper):
    """Export the visible scene to a BGO File"""
    bl_idname = "wftb.export_bgo_with_dialog"
    bl_label = "Export"

    filename_ext = ".bgo3"

    filter_glob: bpy.props.StringProperty(
        default='*.bgo3',
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        if not bpy.context.scene.get('wftb_bgo_export_path'):
            context.scene["wftb_bgo_export_path"] = self.filepath

        bpy.ops.wftb.export_bgo()

        return {'FINISHED'}

class WFTB_OP_export_bgo(bpy.types.Operator):
    """Export the visible scene to a BGO File"""
    bl_idname = "wftb.export_bgo"
    bl_label = "Export"
    bl_description = "Export all the objects in the file excepted the ones placed in a collection with #exclude suffix"
    bl_options = {'BLOCKING'}

    prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences

    def __init__(self):
        self.prefs = bpy.context.preferences.addons["wreckfest_toolbox"].preferences
        # Get if the scene have a custom property referencing the export path
        self.export_path = bpy.context.scene.get('wftb_bgo_export_path')

    def execute(self, context):
        """The exporter will export every objects,
         as long as they are not part of any collection that have the suffix #exclude"""
        if not self.export_path:
            return {'CANCELLED'}

        print("----------------------------------------")
        print('exporting BGO: %r...' % self.export_path)

        # Force object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        time1 = time.clock()

        with open(self.export_path, 'wb') as file:
            file.write(struct.pack('I', 0))
            file.write(bytes('MAIN', 'utf-8'))
            self.write_info(file)
            self.write_materials(file)
            self.write_objects(file)
            self.write_filelen(0, file)

        self.show_message('export done in %.4f sec.' % (time.clock() - time1))
        print("----------------------------------------")
        return {'FINISHED'}

    def show_message(self, message="", message_type='INFO'):
        def draw(self, context):
            self.layout.label(text=message)

        bpy.context.window_manager.popup_menu(draw, title='BGO Exporter', icon=message_type)
        print(message_type, " : ", message)

    @staticmethod
    def object_has_pivot(ob):
        for cs in ob.constraints:
            if cs.type == 'PIVOT':
                return cs

    @staticmethod
    def flip_axes(ob):
        new_rot = (
            ob.rotation_euler[0] * -1, ob.rotation_euler[2] * -1, ob.rotation_euler[1] * -1)
        ob.rotation_euler = mathutils.Vector(new_rot)
        new_scl = (
            ob.scale[0], ob.scale[2], ob.scale[1])
        ob.scale = mathutils.Vector(new_scl)
        bpy.context.view_layer.update()

    @staticmethod
    def get_relative_texpath(absolute_path):
        splts = absolute_path.replace('\\', '/').lower().split('/')
        relative_path = None
        if 'data' in splts:
            relative_path = ('/').join(splts[splts.index('data'):])
        return relative_path

    @staticmethod
    def reorder_objects(lst, pred):
        return_list = [
                          None] * len(pred)
        for v in lst:
            try:
                return_list[pred.index(v.name)] = v
            except:
                return_list.append(v)

        return [x for x in return_list if x is not None]

    @staticmethod
    def create_blank_matrix():
        mat_loc = mathutils.Matrix.Translation((0.0, 0.0, 0.0))
        mat_sca = mathutils.Matrix.Scale(1, 4, (1.0, 1.0, 1.0))
        mat_rot = mathutils.Matrix.Rotation(0, 4, 'X')
        # Deprecated : return mat_loc * mat_rot * mat_sca
        # https://blender.stackexchange.com/questions/129473/typeerror-element-wise-multiplication-not-supported-between-matrix-and-vect
        return mat_loc @ mat_rot @ mat_sca

    @staticmethod
    def get_material_offset(mtl):
        coffset = 0
        for mat in bpy.data.materials:
            if mtl.name == mat.name:
                return coffset
            coffset += 1

        return -1


    @staticmethod
    def get_exportables():
        """Get all the objects in the scene"""
        exportables = []
        # get all the objects of the file
        for obj in bpy.data.objects:
            if (obj.type == 'MESH' or obj.type == 'EMPTY') and ('PivotObject' not in obj):
                is_exportable = True
                for collection in obj.users_collection:
                    if collection.name.endswith("#exclude"):
                        is_exportable = False
                if is_exportable:
                    exportables.append(obj)

        return exportables

    @staticmethod
    def get_undupe_name(name):
        nidx = name.rfind('.')
        if nidx != -1:
            return name[:nidx]
        return name

    @staticmethod
    def write_matrix(matrix, file, sub_vector=None):
        m2 = matrix.transposed()
        lx = matrix[0][3]
        ly = matrix[2][3]
        lz = matrix[1][3]
        if sub_vector is not None:
            lx -= sub_vector[0]
            ly -= sub_vector[2]
            lz -= sub_vector[1]
        file.write(struct.pack('ffff', matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0]))
        file.write(struct.pack('ffff', matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1]))
        file.write(struct.pack('ffff', matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2]))
        file.write(struct.pack('ffff', lx, ly, lz, matrix[3][3]))

    @staticmethod
    def write_flipped_matrix(matrix, file):  # Matrix with Y and Z swapped
        file.write(struct.pack('ffff', matrix[0][0], matrix[2][0], matrix[1][0], matrix[3][0]))
        file.write(struct.pack('ffff', matrix[0][2], matrix[2][2], matrix[1][2], matrix[3][2]))
        file.write(struct.pack('ffff', matrix[0][1], matrix[2][1], matrix[1][1], matrix[3][1]))
        file.write(struct.pack('ffff', matrix[0][3], matrix[2][3], matrix[1][3], matrix[3][3]))

    @staticmethod
    def write_filelen(offset, file, additional_adding=0):
        final_filelen = file.tell() - offset + additional_adding
        file.seek(offset)
        file.write(struct.pack('I', final_filelen))
        file.seek(0, 2)
        return final_filelen

    @staticmethod
    def write_cstring(string, file):
        file.write(bytes(string + '\x00', 'utf-8'))

    @staticmethod
    def write_color3f(color, file):
        file.write(struct.pack('fff', color[0], color[1], color[2]))

    @staticmethod
    def create_header(header_name, header_size, file):
        file.write(struct.pack('L', header_size))
        file.write(bytes(header_name, 'utf-8'))
        return file.tell() - 8

    def write_info(self, file):
        info_start_offset = self.create_header('INFO', 0, file)
        file.write(struct.pack('I', 777))
        self.write_cstring('BGO', file)
        my_username = os.environ['USERNAME'] if 'USERNAME' in os.environ else 'UNKNOWN_USERNAME'
        self.write_cstring(my_username, file)
        self.write_filelen(info_start_offset, file)

    def write_materials(self, file):
        mlst_start_offset = self.create_header('MLST', 0, file)
        file.write(struct.pack('L', len(bpy.data.materials)))
        for mtl in bpy.data.materials:
            self.write_material_individual(mtl, file)

        self.write_filelen(mlst_start_offset, file)

    def write_material_individual(self, mat, file):
        """Write a material in the file"""
        matc_start_offset = self.create_header('MATC', 0, file)
        file.write(bytes('\x00' * 32, 'utf-8'))
        self.write_color3f(mat.diffuse_color, file)
        self.write_color3f(mat.diffuse_color, file)
        self.write_color3f(mat.specular_color, file)
        file.write(struct.pack('f', mat.specular_intensity))
        file.write(struct.pack('f', mat.roughness))
        mat_alpha = 1
        if mat.diffuse_color[3] < 1:
            mat_alpha = mat.diffuse_color[3]  # hopefully fixed right
            # mat_alpha -= mat.alpha # crashes
        file.write(struct.pack('f', mat_alpha))
        file.write(struct.pack('I', 2))
        file.write(bytes('\x00\x00\x00\x00', 'utf-8'))
        file.write(struct.pack('I', 0))
        file.write(bytes('\x00\x00\x00\x00', 'utf-8'))
        self.write_cstring(mat.name, file)

        is_material_written = False
        if mat.node_tree is not None:
            # Find the wreckfest node
            for nd in mat.node_tree.nodes:
                if nd.name == 'Wreckfest Wrapper':
                    self.write_wreckfest_wrapper_node(nd, file)
                    is_material_written = True
                    break
            # if no wreckfest node found, look for principled_bsdf
            if not is_material_written:
                for nd in mat.node_tree.nodes:
                    if nd.type == 'BSDF_PRINCIPLED':
                        self.write_bsdf_node(nd, mat, file)
                        is_material_written = True
                        break
        # if no wreckfest node was found just close the material struct
        if not is_material_written:
            # print("No correct nodes found in material : " + mat.name)
            file.write(struct.pack('I', 0))

        self.write_filelen(matc_start_offset, file)

    def write_wreckfest_wrapper_node(self, node, file):
        """For each WF slot, look if a texture was registered, if yes, write it"""
        texture_paths = {}
        for key in wf_slots:
            image = node.get(key)
            if type(image) is bpy.types.Image:
                absolute_texture_path = os.path.abspath(bpy.path.abspath(image.filepath))
                texture_path = self.get_relative_texpath(absolute_texture_path)
                texture_paths[wf_slots[key]] = texture_path

        file.write(struct.pack('I', len(texture_paths)))

        for slot in texture_paths:
            self.write_texture_individual(slot, texture_paths[slot], file)

    def write_bsdf_node(self, node, mat, file):
        # Create a dictionary of linked TEX_IMAGE Node (Shader input : TEX_Node)
        tex_nodes = {}

        # Go through shader node inputs
        for sh_in in node.inputs:
            if sh_in.is_linked:
                # WARNING : This can skip texture if people link smtg else than a TEX_IMAGE and/or link multiple things
                if sh_in.links[0].from_socket.node.type == 'TEX_IMAGE':
                    tex_nodes[sh_in.name] = sh_in.links[0].from_socket.node

        # Just take the len of linked Tex Nodes
        file.write(struct.pack('I', len(tex_nodes)))

        # Go through registered texture nodes with their link
        for tn in tex_nodes:
            try:
                self.write_texture_node_individual(tex_nodes[tn], wf_bsdf_slots[tn], file)
            except KeyError:
                self.show_message(
                    'Texture in incorrect slot "' + tn + '" in material: "' + mat.name + '"',
                    'ERROR')
                self.write_texture_node_individual(tex_nodes[tn], 1, file)  # default to slot 1

    # This method take a  TEX Node in param, and it's slot_id from Princ BSDF to WF dict

    def write_texture_node_individual(self, node, slotid, file):
        texture_path = None
        if node.image is not None and node.image.filepath is not None:
            # Get the image Path
            absolute_texture_path = os.path.abspath(bpy.path.abspath(node.image.filepath))
            texture_path = self.get_relative_texpath(absolute_texture_path)
        if texture_path is None:
            texture_path = 'data/art/textures/tmp_red_c.tga'

        self.write_texture_individual(slotid, texture_path, file)

    def write_texture_individual(self, slotid, texture_path, file):
        texc_start_offset = self.create_header('TEXC', 0, file)
        file.write(struct.pack('III', slotid, 1, 0))
        file.write(struct.pack('ffff', 1, 0, 0, 0))
        file.write(struct.pack('ffff', 0, 1, 0, 0))
        file.write(struct.pack('ffff', 0, 0, 1, 0))
        file.write(struct.pack('ffff', 0, 0, 0, 1))
        self.write_cstring(texture_path, file)
        self.write_filelen(texc_start_offset, file)

    def write_gmesh(self, ob, file):
        # print('writing mesh for ' + ob.name)
        gmesh_start_offset = self.create_header('GMSH', 0, file)
        bm = bmesh.new()
        # TODO : See to_mesh to use preserve all data layer
        # temp_mesh = ob.to_mesh()
        # bm.from_mesh(temp_mesh)
        depsgraph = bpy.context.view_layer.depsgraph
        bm.from_object(object=ob, depsgraph=depsgraph, deform=self.prefs.get("apply_modifiers", True))

        bm_tris = bm.calc_loop_triangles()
        uv_layers = len(bm.loops.layers.uv)
        file.write(struct.pack('LL', len(bm_tris), uv_layers))
        for tri in bm_tris:
            mat_index = 0
            try:
                mat_index = float(self.get_material_offset(ob.data.materials[tri[0].face.material_index]))
            except:
                mat_index = 0

            for loop in tri[::-1]:
                file.write(struct.pack('ffff', mat_index, loop.vert.co[0], loop.vert.co[2], loop.vert.co[1]))
                for uvl in range(uv_layers):
                    uv_data = loop[bm.loops.layers.uv[uvl]].uv
                    c1p = loop.vert.normal.cross(mathutils.Vector((0.0, 0.0, 1.0)))
                    c2p = loop.vert.normal.cross(mathutils.Vector((0.0, 1.0, 0.0)))
                    loop_tang = c2p
                    if c1p.length > c2p.length:
                        loop_tang = c1p
                    loop_binormal = loop.vert.normal.cross(loop_tang)
                    file.write(struct.pack('fffffffffff',  # combining struck.pack is faster
                                           uv_data[0], ((uv_data[1] - 1) * -1),
                                           loop.vert.normal[0], loop.vert.normal[2], loop.vert.normal[1],
                                           loop_tang[0], loop_tang[2], loop_tang[1],
                                           loop_binormal[0], loop_binormal[2], loop_binormal[1]))

        # bpy.data.meshes.remove(temp_mesh) No longer needed
        bm.free()
        self.write_filelen(gmesh_start_offset, file, -8)

    @staticmethod
    def find_xref_path(self, obname, exporting_to_path=""):  # Find xref path from object name
        name = obname.replace('\\', '/')
        name = name.replace("#xref", "")
        name = name.replace(" ", "")
        name = name.rstrip('1234567890.')  # remove .001 from end
        # replace ob/ and le/ shorts
        if name[:3].lower() == "ob/": name = "data/art/objects/" + name[3:]
        if name[:3].lower() == "le/": name = "data/art/levels/" + name[3:]
        if name[:2].lower() == "//": name = exporting_to_path + name[2:]
        return name

    @staticmethod
    def fake_xref_name(self, name):  # fake 3dsmax style name
        name = name.replace('\\', '/').split("/")[-1]
        name = name.replace(".scne.", "#xref")
        name = name.replace(".scne", "#xref")
        return name

    def get_custom_data(self, obj):
        custom_data = ""
        if 'CustomData' in obj:
            custom_data = obj['CustomData']
            custom_data += "\r"

        for key, value in obj.items():
            if key.startswith("WFTB_"):
                prop_value = bool(value)
                custom_data += key[5:] + " = " + str(prop_value).lower() + "\r"

        return custom_data

    def write_objects(self, file):
        """Get all the objects that are not in a collection with the suffix #exclude"""
        hier_start_offset = self.create_header('HIER', 0, file)
        exportables = self.get_exportables()
        file.write(struct.pack('L', len(exportables)))
        objects_id_dictionary = {}
        objects_id_current = 1
        objects_id_mesh = -1
        for obj in exportables:
            print('writing object ' + obj.name)
            object_type = ''
            is_xref_subscene = obj.name.strip().startswith("#xref")
            # Set the type of object
            if is_xref_subscene or (obj.data is not None and obj.data.library is not None):
                object_type = 'OBJX'
            else:
                if obj.type == 'MESH':
                    object_type = 'OBJM'
                    objects_id_mesh += 1
                else:
                    if obj.type == 'EMPTY':
                        object_type = 'OBJD'
                    else:
                        continue

            objects_id_dictionary[obj.name] = objects_id_current
            object_offset = self.create_header(object_type, 0, file)
            if obj.parent is not None:
                file.write(struct.pack('I', objects_id_dictionary[obj.parent.name]))
            else:
                file.write(struct.pack('I', 0))
            file.write(struct.pack('I', 0))

            pivot = self.object_has_pivot(obj)
            if pivot is not None:  # If special pivot constraint used?
                self.flip_axes(obj)  # slow
                self.write_matrix(obj.matrix_local, file)
                print('using pivot matrix from ' + pivot.target.name + ' for ' + obj.name)
                self.flip_axes(pivot.target)
                self.write_matrix(pivot.target.matrix_local, file, obj.location)
                self.flip_axes(pivot.target)
                self.flip_axes(obj)
            else:  # normal model
                self.write_flipped_matrix(obj.matrix_local, file)
                self.write_matrix(self.create_blank_matrix(), file)

            file.write(struct.pack('II', 0, 3))
            if is_xref_subscene:
                self.write_cstring(self.fake_xref_name(obj.name), file)
            else:
                self.write_cstring(obj.name, file)

            # Write custom data

            customdata = self.get_custom_data(obj)

            self.write_cstring(str(customdata).replace('|', '\r\n'), file)
            if object_type == 'OBJM':
                file.write(struct.pack('I', objects_id_mesh))
                self.write_gmesh(obj, file)
            if object_type == 'OBJX':
                if is_xref_subscene:  # Xref Subscene (Unofficial)
                    self.write_cstring(self.find_xref_path(obj.name)[:-5] + '.scn', file)
                else:  # File > link Subscene
                    apth = os.path.abspath(bpy.path.abspath(obj.data.library.filepath))
                    self.write_cstring(str(self.get_relative_texpath(apth.replace(".blend", ".ble"))), file)
            objects_id_current += 1
            self.write_filelen(object_offset, file, -8)


