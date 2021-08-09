import bpy


class WreckfestWrapperNode(bpy.types.ShaderNodeCustomGroup):
    """Add wreckfest node"""
    bl_name = "wreckfest_wrapper_node"
    bl_label = "Wreckfest Wrapper"

    # Manage the node sockets
    def __nodeinterface_setup__(self):
        # Clear inputs
        self.node_tree.inputs.clear()

        # Functions Shortcuts
        add_input = self.node_tree.inputs.new
        add_output = self.node_tree.outputs.new
        g_input = self.inputs.get

        # <editor-fold desc="Inputs Creation">

        # Create inputs if no image was set

        if self.ao_image is None:
            add_input('NodeSocketFloat', 'AmbientOcclusion')
            g_input('AmbientOcclusion').default_value = 1.0

        if self.base_color_image is None:
            add_input('NodeSocketColor', 'BaseColor')
            g_input('BaseColor').default_value = [0.8, 0.8, 0.8, 1]

        if self.specular_color_image is None:
            add_input('NodeSocketColor', 'SpecularColor')
            g_input('SpecularColor').default_value = [0.8, 0.8, 0.8, 1]

        if self.specular_level_image is None:
            add_input('NodeSocketFloat', 'SpecularLevel')
            g_input('SpecularLevel').default_value = 0.5

        if self.glossiness_image is None:
            add_input('NodeSocketFloat', 'Glossiness')
            g_input('Glossiness').default_value = 0

        if self.self_illumination_image is None:
            add_input('NodeSocketColor', 'SelfIllumination')
            g_input('SelfIllumination').default_value = [0, 0, 0, 1]

        if self.opacity_image is None:
            add_input('NodeSocketFloat', 'Opacity')
            g_input('Opacity').default_value = 1

        if self.filter_color_image is None:
            add_input('NodeSocketColor', 'FilterColor')
            g_input('FilterColor').default_value = [0, 0, 0, 1]

        if self.bump_image is None:
            add_input('NodeSocketColor', 'Bump')
            g_input('Bump').default_value = [0.5, 0.5, 1, 1]

        if self.mrs_image is None:
            add_input('NodeSocketColor', 'MRS')
            g_input('MRS').default_value = [0, 0.4, 0.5, 1]

        if self.refraction_image is None:
            add_input('NodeSocketFloat', 'Refraction')
            g_input('Refraction').default_value = 1.45

        if self.displacement_image is None:
            add_input('NodeSocketColor', 'Displacement')
            g_input('Displacement').default_value = [0, 0, 0, 1]

        # </editor-fold>

        # <editor-fold desc="Inputs Creation">

        if self.node_tree.outputs.get('Shader Surface') is None:
            add_output('NodeSocketShader', 'Shader Surface')
        if self.node_tree.outputs.get('Displacement') is None:
            add_output('NodeSocketVector', 'Displacement')

        # </editor-fold>

    def __nodetree_setup__(self):

        # <editor-fold desc="Clear">

        # Clear all the links
        self.node_tree.links.clear()

        # Clear all the nodes
        for node in self.node_tree.nodes:
            if not node.name in ['Group Input', 'Group Output']:
                self.node_tree.nodes.remove(node)
        # </editor-fold>

        # <editor-fold desc="Node Creation">
        input_node = self.node_tree.nodes['Group Input']
        output_node = self.node_tree.nodes['Group Output']

        # Create function shortcuts
        add_node = self.node_tree.nodes.new
        link = self.node_tree.links.new

        # BSDF Shader node
        bsdf = add_node('ShaderNodeBsdfPrincipled')
        bsdf.location = (600, 0)

        # Split Metallic Roughness Specular node
        split_mrs = add_node('ShaderNodeSeparateRGB')
        split_mrs.name = 'Split MRS'
        split_mrs.location = (200, -200)

        # Mix Base Color with AO
        mix_rgb = add_node('ShaderNodeMixRGB')
        mix_rgb.name = 'Mix Albedo with AO'
        mix_rgb.blend_type = 'MULTIPLY'
        mix_rgb.location = (400, 0)

        # Invert Filter Color
        invert = add_node('ShaderNodeInvert')
        invert.name = 'Invert Filter'
        invert.location = (200, 0)

        # Normal Map Node
        normal_map = add_node('ShaderNodeNormalMap')
        normal_map.location = (200, -400)

        # Displacement Map
        displacement = add_node('ShaderNodeVectorDisplacement')
        displacement.location = (600, -600)
        # </editor-fold>

        # <editor-fold desc="Links">

        # Create Links
        g_input = self.inputs.get

        # Links input node or Create Texture Nodes
        if self.ao_image is None:
            link(input_node.outputs['AmbientOcclusion'], mix_rgb.inputs[2])
        else:
            ao_texture = add_node('ShaderNodeTexImage')
            ao_texture.name = 'AO Texture'
            ao_texture.image = self.ao_image
            link(ao_texture.outputs[0], mix_rgb.inputs[2])

        if self.base_color_image is None:
            link(input_node.outputs['BaseColor'], mix_rgb.inputs[1])
        else:
            base_color_texture = add_node('ShaderNodeTexImage')
            base_color_texture.name = 'Base Color Texture'
            base_color_texture.image = self.base_color_image
            link(base_color_texture.outputs[0], mix_rgb.inputs[1])

        if self.specular_color_image is None:
            pass

        if self.specular_level_image is None:
            link(input_node.outputs['SpecularLevel'], bsdf.inputs['Specular'])
        else:
            specular_level_texture = add_node('ShaderNodeTexImage')
            specular_level_texture.name = 'Specular Level Texture'
            specular_level_texture.image = self.specular_level_image
            link(specular_level_texture.outputs[0], bsdf.inputs['Specular'])

        if self.glossiness_image is None:
            link(input_node.outputs['Glossiness'], bsdf.inputs['Clearcoat'])
        else:
            glossiness_texture = add_node('ShaderNodeTexImage')
            glossiness_texture.name = 'Glossiness Texture'
            glossiness_texture.image = self.glossiness_image
            link(glossiness_texture.outputs[0], bsdf.inputs['Clearcoat'])

        if self.self_illumination_image is None:
            link(input_node.outputs['SelfIllumination'], bsdf.inputs['Emission'])
        else:
            self_illumination_texture = add_node('ShaderNodeTexImage')
            self_illumination_texture.name = 'Self Illumination Texture'
            self_illumination_texture.image = self.self_illumination_image
            link(self_illumination_texture.outputs[0], bsdf.inputs['Emission'])

        if self.opacity_image is None:
            link(input_node.outputs['Opacity'], bsdf.inputs['Alpha'])
        else:
            opacity_texture = add_node('ShaderNodeTexImage')
            opacity_texture.name = 'Opacity Texture'
            opacity_texture.image = self.opacity_image
            link(opacity_texture.outputs[0], bsdf.inputs['Alpha'])

        if self.filter_color_image is None:
            link(input_node.outputs['FilterColor'], invert.inputs[1])
        else:
            filter_color_texture = add_node('ShaderNodeTexImage')
            filter_color_texture.name = 'Filter Color Texture'
            filter_color_texture.image = self.filter_color_image
            link(filter_color_texture.outputs[0], invert.inputs[1])

        if self.bump_image is None:
            link(input_node.outputs['Bump'], normal_map.inputs[1])
        else:
            bump_texture = add_node('ShaderNodeTexImage')
            bump_texture.name = 'Bump Texture'
            bump_texture.image = self.bump_image
            link(bump_texture.outputs[0], normal_map.inputs[1])

        if self.mrs_image is None:
            link(input_node.outputs['MRS'], split_mrs.inputs[0])
        else:
            mrs_texture = add_node('ShaderNodeTexImage')
            mrs_texture.name = 'MRS Texture'
            mrs_texture.image = self.mrs_image
            link(mrs_texture.outputs[0], split_mrs.inputs[0])

        if self.refraction_image is None:
            link(input_node.outputs['Refraction'], bsdf.inputs['IOR'])
        else:
            refraction_texture = add_node('ShaderNodeTexImage')
            refraction_texture.name = 'Refraction Texture'
            refraction_texture.image = self.refraction_image
            link(refraction_texture.outputs[0], bsdf.inputs['IOR'])

        if self.displacement_image is None:
            link(input_node.outputs['Displacement'], displacement.inputs[0])
        else:
            displacement_texture = add_node('ShaderNodeTexImage')
            displacement_texture.name = 'Displacement Texture'
            displacement_texture.image = self.displacement_image
            link(displacement_texture.outputs[0], displacement.inputs[0])

        # -Normal Map
        link(normal_map.outputs[0], bsdf.inputs['Normal'])
        # -Apply AO on Base Color
        link(invert.outputs[0], mix_rgb.inputs[0])
        link(mix_rgb.outputs[0], bsdf.inputs['Base Color'])
        # -Separate Metallic Roughness Specular
        link(split_mrs.outputs[0], bsdf.inputs['Metallic'])
        link(split_mrs.outputs[1], bsdf.inputs['Roughness'])
        link(split_mrs.outputs[2], bsdf.inputs['Specular Tint'])
        # -outputs
        link(bsdf.outputs[0], output_node.inputs[0])
        link(displacement.outputs[0], output_node.inputs[1])

        # </editor-fold>

    def update_images(self, context):
        self.__nodeinterface_setup__()
        self.__nodetree_setup__()

    # <editor-fold desc="Image Properties">

    # Add props to fill the textures directly without having to connect nodes
    # Add an image data block that reference the image
    ao_image: bpy.props.PointerProperty(
        name="Ambient Occlusion",
        description="3ds Max : Ambient Color\n"
                    "Wreckfest Slot id : 0\n"
                    "File Suffix : _aoc.tga\n",
        type=bpy.types.Image,
        update=update_images
    )

    base_color_image: bpy.props.PointerProperty(
        name="Base Color",
        description="3ds Max : Diffuse Color\n"
                    "Wreckfest Slot id : 1\n"
                    "File Suffix : _c.tga or _c5.tga\n",
        type=bpy.types.Image,
        update=update_images
    )

    specular_color_image: bpy.props.PointerProperty(
        name="Specular Color",
        description="3ds Max : Specular Color\n"
                    "Wreckfest Slot id : 2",
        type=bpy.types.Image,
        update=update_images
    )

    specular_level_image: bpy.props.PointerProperty(
        name="Specular Level",
        description="3ds Max : Specular Level\n"
                    "Wreckfest Slot id : 3",
        type=bpy.types.Image,
        update=update_images
    )

    glossiness_image: bpy.props.PointerProperty(
        name="Glossiness",
        description="3ds Max : Glossiness\n"
                    "Wreckfest Slot id : 4",
        type=bpy.types.Image,
        update=update_images
    )

    self_illumination_image: bpy.props.PointerProperty(
        name="Self Illumination",
        description="3ds Max : Self-Illumination\n"
                    "Wreckfest Slot id : 5",
        type=bpy.types.Image,
        update=update_images
    )

    opacity_image: bpy.props.PointerProperty(
        name="Opacity",
        description="use the alpha of base color texture"
                    "3ds Max : Opacity\n"
                    "Wreckfest Slot id : 6\n"
                    "File Suffix : _c.tga",
        type=bpy.types.Image,
        update=update_images
    )

    filter_color_image: bpy.props.PointerProperty(
        name="Filter Color",
        description="3ds Max : Filter Color\n"
                    "Wreckfest Slot id : 7\n"
                    "File Suffix : _ao.tga",
        type=bpy.types.Image,
        update=update_images
    )

    bump_image: bpy.props.PointerProperty(
        name="Bump",
        description="3ds Max : Bump\n"
                    "Wreckfest Slot id : 8\n"
                    "File Suffix : _n.tga",
        type=bpy.types.Image,
        update=update_images
    )

    mrs_image: bpy.props.PointerProperty(
        name="Metalic Roughness Specular",
        description="Metallic = R channel | Roughness = G channel | Specular = B channel"
                    "3ds Max : Reflection\n"
                    "Wreckfest Slot id : 9\n"
                    "File Suffix : _s.tga",
        type=bpy.types.Image,
        update=update_images
    )

    refraction_image: bpy.props.PointerProperty(
        name="Refraction",
        description="3ds Max : Refraction\n"
                    "Wreckfest Slot id : 10",
        type=bpy.types.Image,
        update=update_images
    )

    displacement_image: bpy.props.PointerProperty(
        name="Displacement",
        description="3ds Max : Displacement\n"
                    "Wreckfest Slot id : 11",
        type=bpy.types.Image,
        update=update_images
    )

    # </editor-fold>

    def init(self, context):
        custom_node_name = "Wreckfes Wrapper"
        self.node_tree = bpy.data.node_groups.new('.' + self.bl_name, 'ShaderNodeTree')
        self.label = self.bl_label
        # Inputs
        # Add a node  group input to the group
        input_node = self.node_tree.nodes.new('NodeGroupInput')
        input_node.location = (0, 0)
        # Outputs
        output_node = self.node_tree.nodes.new('NodeGroupOutput')
        output_node.location = (1000, 0)
        self.__nodeinterface_setup__()
        self.__nodetree_setup__()
        self.width = 500

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.operator("image.open", icon="FILEBROWSER", text="Open Images")
        row = layout.row(align=True)
        row.label(text="Ambient Occlusion")
        row.label(text="Base Color")
        row.label(text="Emissive")
        row = layout.row(align=True)
        row.prop(self, "ao_image", text="")
        row.prop(self, "base_color_image", text="")
        row.prop(self, "self_illumination_image", text="")
        row = layout.row(align=True)
        row.label(text="Metalic Roughness Specular")
        row.label(text="Specular Color")
        row.label(text="Specular Level")
        row = layout.row(align=True)
        row.prop(self, "mrs_image", text="")
        row.prop(self, "specular_color_image", text="")
        row.prop(self, "specular_level_image", text="")
        row = layout.row(align=True)
        row.label(text="Gloss")
        row.label(text="Opacity")
        row.label(text="Refraction")
        row = layout.row(align=True)
        row.prop(self, "glossiness_image", text="")
        row.prop(self, "opacity_image", text="")
        row.prop(self, "refraction_image", text="")
        row = layout.row(align=True)
        row.label(text="Filter Color")
        row.label(text="Bump / Normal")
        row.label(text="Displacement")
        row = layout.row(align=True)
        row.prop(self, "filter_color_image", text="")
        row.prop(self, "bump_image", text="")
        row.prop(self, "displacement_image", text="")

    def copy(self, node):
        self.node_tree = node.node_tree.copy()

    def free(self):
        bpy.data.node_groups.remove(self.node_tree, do_unlink=True)




