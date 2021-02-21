import bpy
from ShaderNodeBase import ShaderNodeBase

class ShaderNodeWreckfestConverter(ShaderNodeBase):

    bl_name='ShaderNodeWreckfestConverter'
    bl_label='Wreckfest Converter'
    bl_icon='NONE'

    def defaultNodeTree(self):
        #Nodes
        self.addNode('ShaderNodeBsdfPrincipled', {'name':'Principled BSDF', 'inputs[1].default_value':0.000, 'inputs[2].default_value':[1.000,0.200,0.100], 'inputs[3].default_value':[0.800,0.800,0.800,1.000], 'inputs[4].default_value':0.000, 'inputs[5].default_value':0.500, 'inputs[6].default_value':0.000, 'inputs[7].default_value':0.500, 'inputs[8].default_value':0.000, 'inputs[9].default_value':0.000, 'inputs[10].default_value':0.000, 'inputs[11].default_value':0.500, 'inputs[12].default_value':0.000, 'inputs[13].default_value':0.030, 'inputs[14].default_value':1.450, 'inputs[15].default_value':0.000, 'inputs[16].default_value':0.000, 'inputs[17].default_value':[0.000,0.000,0.000,1.000], 'inputs[18].default_value':1.000, 'inputs[19].default_value':[0.000,0.000,0.000], 'inputs[20].default_value':[0.000,0.000,0.000], 'inputs[21].default_value':[0.000,0.000,0.000]})
        self.addNode('ShaderNodeSeparateRGB', {'name':'Split MRS'})
        self.addNode('ShaderNodeMixRGB', {'name':'Mix', 'blend_type':'MULTIPLY', 'use_clamp':0.000, 'inputs[2].default_value':[0.000,0.000,0.000,1.000]})
        self.addNode('ShaderNodeInvert', {'name':'Invert', 'inputs[0].default_value':1.000})
        self.addNode('ShaderNodeNormalMap', {'name':'Normal Map', 'inputs[0].default_value':1.000})
        self.addNode('ShaderNodeVectorDisplacement', {'name':'Vector Displacement', 'inputs[1].default_value':0.000, 'inputs[2].default_value':1.000})
        #Inputs
        self.addInput('NodeSocketFloat', {'name':'Ambient Color', 'default_value':1.000, 'min_value':0.000, 'max_value':1.000})
        self.addInput('NodeSocketColor', {'name':'Base Color', 'default_value':[0.800,0.800,0.800,1.000]})
        self.addInput('NodeSocketColor', {'name':'Specular Color', 'default_value':[0.800,0.800,0.800,1.000]})
        self.addInput('NodeSocketFloat', {'name':'Specular Level', 'default_value':0.500, 'min_value':0.000, 'max_value':1.000})
        self.addInput('NodeSocketFloat', {'name':'Glossiness', 'default_value':0.000, 'min_value':0.000, 'max_value':1.000})
        self.addInput('NodeSocketColor', {'name':'Self  Illumination', 'default_value':[0.000,0.000,0.000,1.000]})
        self.addInput('NodeSocketFloat', {'name':'Opacity', 'default_value':1.000, 'min_value':0.000, 'max_value':1.000})
        self.addInput('NodeSocketColor', {'name':'Filter Color', 'default_value':[0.800,0.800,0.800,1.000]})
        self.addInput('NodeSocketColor', {'name':'Bump', 'default_value':[0.500,0.500,1.000,1.000]})
        self.addInput('NodeSocketFloat', {'name':'MRS (Reflection)', 'default_value':0.000, 'min_value':0.000, 'max_value':1.000})
        self.addInput('NodeSocketFloat', {'name':'Refraction', 'default_value':1.450, 'min_value':0.000, 'max_value':1000.000})
        self.addInput('NodeSocketColor', {'name':'DisplacementMap', 'default_value':[0.000,0.000,0.000,0.000]})
        #Outputs
        self.addOutput('NodeSocketShader', {'name':'Shader Surface'})
        self.addOutput('NodeSocketVector', {'name':'Displacement', 'default_value':[0.000,0.000,0.000], 'min_value':0.000, 'max_value':1.000})
        #Links
        self.addLink('nodes["Group Input"].outputs[1]', 'nodes["Mix"].inputs[1]')
        self.addLink('nodes["Group Input"].outputs[3]', 'nodes["Principled BSDF"].inputs[5]')
        self.addLink('nodes["Group Input"].outputs[4]', 'nodes["Principled BSDF"].inputs[12]')
        self.addLink('nodes["Group Input"].outputs[5]', 'nodes["Principled BSDF"].inputs[17]')
        self.addLink('nodes["Group Input"].outputs[6]', 'nodes["Principled BSDF"].inputs[18]')
        self.addLink('nodes["Group Input"].outputs[7]', 'nodes["Invert"].inputs[1]')
        self.addLink('nodes["Group Input"].outputs[8]', 'nodes["Normal Map"].inputs[1]')
        self.addLink('nodes["Group Input"].outputs[9]', 'nodes["Split MRS"].inputs[0]')
        self.addLink('nodes["Group Input"].outputs[10]', 'nodes["Principled BSDF"].inputs[14]')
        self.addLink('nodes["Group Input"].outputs[11]', 'nodes["Vector Displacement"].inputs[0]')
        #-Normal Map
        self.addLink('nodes["Normal Map"].outputs[0]', 'nodes["Principled BSDF"].inputs[19]')
        #-Apply AO on Base Color
        self.addLink('nodes["Invert"].outputs[0]', 'nodes["Mix"].inputs[0]')
        self.addLink('nodes["Mix"].outputs[0]', 'nodes["Principled BSDF"].inputs[0]')
        #-Separate Metallic Roughness Specular
        self.addLink('nodes["Split MRS"].outputs[0]', 'nodes["Principled BSDF"].inputs[4]')
        self.addLink('nodes["Split MRS"].outputs[1]', 'nodes["Principled BSDF"].inputs[7]')
        self.addLink('nodes["Split MRS"].outputs[2]', 'nodes["Principled BSDF"].inputs[6]')
        #-outputs
        self.addLink('nodes["Principled BSDF"].outputs[0]', 'nodes["Group Output"].inputs[0]')
        self.addLink('nodes["Vector Displacement"].outputs[0]', 'nodes["Group Output"].inputs[1]')
        
        

    def init(self, context):
        self.setupTree()

    #def copy(self, node):

    #def free(self):

    #def socket_value_update(self, context):

    #def update(self):

    #def draw_buttons(self, context, layout):

    #def draw_buttons_ext(self, contex, layout):

    #def draw_label(self):
    
    def draw_menu(self):
        return 'SH_WRECKFEST' , 'Wreckfest'
