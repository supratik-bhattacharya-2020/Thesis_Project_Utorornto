'''
Transparent layer below, pbr layer above!!
'''
import bpy
import math
import random
bpy.ops.mesh.primitive_plane_add(size = 10)
plane = bpy.context.active_object
bpy.ops.mesh.primitive_cube_add(size=5, location=(0,0,2.5))
cube = bpy.context.active_object
###created a cube and a plane
base_material = bpy.data.materials.new(name = "base_material2")
base_material.use_nodes = True
##base_material created
bpy.context.object.active_material = base_material
#bpy.context.scene.objects.active = some_obj from SO answer
#bpy.context.scene.objects.active = cube
#shortcut_nodes:
all_nodes = base_material.node_tree.nodes
link = base_material.node_tree.links.new
##important for linking the nodes!
mix_shader1 = all_nodes.new('ShaderNodeMixShader')
#bpy.ops.node.add_node(type="ShaderNodeMixShader", use_transform=True)
#bpy.ops.node.add_node(type="ShaderNodeOutputMaterial", use_transform=True)
out_node = all_nodes.get("Material Output")
del_node = all_nodes.get("Principled BSDF")
all_nodes.remove(del_node)
out_node.location = (400,380)
mix_shader1.location = (400,210)
link(mix_shader1.outputs[0],out_node.inputs[0])
#works fine till above line
#bpy.ops.node.add_node(type="ShaderNodeBsdfGlass", use_transform=True)
#bpy.ops.node.add_node(type="ShaderNodeBsdfGlossy", use_transform=True)
#**************RANDOMLY CHOOSING A NODE*******************#
#shader_s = random.randrange(1,6)
shader_s = 4
choice_of_shader = {1:'ShaderNodeBsdfGlass',2:'ShaderNodeBsdfDiffuse',3:'ShaderNodeEmission',
                    4:'ShaderNodeBsdfPrincipled',5:'ShaderNodeBsdfGlossy'}
chosen_shader = all_nodes.new(choice_of_shader[shader_s])
if shader_s in [2,3,4,5]:
    chosen_shader.inputs[0].default_value = (random.random(),random.random(),random.random(),1)
if shader_s == 3:
    chosen_shader.inputs[1].default_value = (random.randrange(1,4))
if shader_s == 4:
    #4:metallic
    #7:roughness
    #15:transmission
    chosen_shader.inputs[4].default_value = (random.randrange(0,2))
    chosen_shader.inputs[7].default_value = (random.random())
    chosen_shader.inputs[15].default_value = (random.random())
if shader_s == 5:
    chosen_shader.inputs[1].default_value = (random.random())
chosen_shader.location = (300,-290)
link(chosen_shader.outputs[0],mix_shader1.inputs[2])
#mix_shader2 = all_nodes.new('ShaderNodeMixShader')
#mix_shader2.location = (0,-200)
#link(mix_shader2.outputs[0],mix_shader1.inputs[1])
#bpy.ops.node.add_node(type="ShaderNodeBsdfDiffuse", use_transform=True)
#sec_shader = random.randrange(1,6)
sec_shader = 1
#choice_of_shader = {1:'ShaderNodeBsdfGlass',2:'ShaderNodeBsdfDiffuse',3:'ShaderNodeEmission',
#                    4:'ShaderNodeBsdfPrincipled',5:'ShaderNodeBsdfGlossy'}
chosen_shader2 = all_nodes.new(choice_of_shader[sec_shader])
if sec_shader in [2,3,4,5]:
    chosen_shader2.inputs[0].default_value = (random.random(),random.random(),random.random(),1)
if sec_shader == 3:
    chosen_shader2.inputs[1].default_value = (random.randrange(1,4))
if sec_shader == 4:
    #4:metallic
    #7:roughness
    #15:transmission
    chosen_shader2.inputs[4].default_value = (random.randrange(0,2))
    chosen_shader2.inputs[7].default_value = (random.random())
    chosen_shader2.inputs[15].default_value = (random.random())
if sec_shader == 5:
    chosen_shader2.inputs[1].default_value = (random.random())
chosen_shader2.location = (-40,-10)
link(chosen_shader2.outputs[0],mix_shader1.inputs[1])
#diffuse_bsdf = all_nodes.new('ShaderNodeBsdfDiffuse')
#diffuse_bsdf.location = (0,500)
##changeable
#*************USED RANDOM NUMBERS HERE***********************************#
#diffuse_bsdf.inputs[0].default_value = (random.random(),random.random(),random.random(),1)
#link(diffuse_bsdf.outputs[0],mix_shader2.inputs[1])
#link(glass_shader.outputs[0],mix_shader2.inputs[2])
#mix_shader2.inputs[0].default_value = (1.0)
##bpy.ops.node.add_node(type="ShaderNodeValToRGB", use_transform=True)
color_ramp1 = all_nodes.new('ShaderNodeValToRGB')
color_ramp1.location = (200,380)
link(color_ramp1.outputs[0],mix_shader1.inputs[0])
###how to control coloramp???
color_ramp1.color_ramp.elements[0].position = (0.450)
color_ramp1.color_ramp.elements[1].position = (0.650)
###above can be randomised
#bpy.ops.node.add_node(type="ShaderNodeMixRGB", use_transform=True)
mix_rgb = all_nodes.new('ShaderNodeMixRGB')
mix_rgb.location = (-200,400)
link(mix_rgb.outputs[0],color_ramp1.inputs[0])
#bpy.ops.node.add_node(type="ShaderNodeTexGradient", use_transform=True)
#bpy.ops.node.add_node(type="ShaderNodeTexNoise", use_transform=True)
gradient_node = all_nodes.new('ShaderNodeTexGradient')
gradient_node.location = (-300,400)
noise_node = all_nodes.new('ShaderNodeTexNoise')
noise_node.location = (-300,200)
#*************USED RANDOM NUMBERS HERE***********************************#
noise_node.inputs[2].default_value = (random.randrange(0,50))
link(gradient_node.outputs[0],mix_rgb.inputs[1])
link(noise_node.outputs[1],mix_rgb.inputs[2])
#bpy.ops.node.add_node(type="ShaderNodeMapping", use_transform=True)
mapping_node = all_nodes.new('ShaderNodeMapping')
mapping_node.location = (-600,300)
mapping_node.inputs[2].default_value = (0,math.radians(90),0)
link(mapping_node.outputs[0],gradient_node.inputs[0])
link(mapping_node.outputs[0],noise_node.inputs[0])
mix_rgb1 = all_nodes.new('ShaderNodeMixRGB')
mix_rgb1.location = (-800,400)
link(mix_rgb1.outputs[0],mapping_node.inputs[0])
#bpy.ops.node.add_node(type="ShaderNodeTexCoord", use_transform=True)
tex_cord = all_nodes.new('ShaderNodeTexCoord')
tex_cord.location = (-1000,400)
noise_node1 = all_nodes.new('ShaderNodeTexNoise')
noise_node1.location = (-1200,200)
#*************USED RANDOM NUMBERS HERE***********************************#
noise_node1.inputs[2].default_value = (random.randrange(0,50))
link(noise_node1.outputs[0],mix_rgb1.inputs[1])
link(tex_cord.outputs[3],mix_rgb1.inputs[2])
