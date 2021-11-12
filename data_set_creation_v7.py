import os
import bpy
import glob
import time
import random
'''
Here it is assumed that PBR node setup is already done manually
How? First New Material -> click on Principled BSDF -> click Ctrl + Shift + T
Textures downloaded from https://ambientcg.com
Hence the naming convention followed by the website is used
Now save the name of this material as base_material2.001
'''
'''
set the mix_rgb1 fac to 0.75
set the mix_rgb2 fac to 0.25
'''
def get_materials(directory_name,part):
    '''
    takes in argument the directory_name as a string object and part 0: above layer, 1: below layer
    returns null
    '''
    base_material = bpy.data.materials['base_material2.001']
    all_nodes = base_material.node_tree.nodes
    cwd = os.getcwd()
    os.chdir('../../Pictures/blender_progression/textures/ambientcg/'+directory_name)
    #below scheme assumes that we have our files with correct nomenclature in our folder
    bi_file =  glob.glob('*Color*')[0]
    ri_file =  glob.glob('*Rough*')[0]
    ni_file =  glob.glob('*NormalGL*')[0]
    di_file =  glob.glob('*Displacement*')[0]
    os.chdir(cwd)
    common_path = '/home/supratik/Pictures/blender_progression/textures/ambientcg/'
    mix_shader = all_nodes.get('Mix Shader')
    principled_bsdf = mix_shader.inputs[1+part].links[0].from_node
    base_color = principled_bsdf.inputs[0].links[0].from_node
    base_img = bpy.data.images.load(filepath = common_path+directory_name+'/'+bi_file)
    base_color.image = base_img
    #figuring thisout was very difficult ;)
    #roughness node:
    roughness = principled_bsdf.inputs[7].links[0].from_node
    rough_img = bpy.data.images.load(filepath = common_path+directory_name+'/'+ri_file)
    roughness.image = rough_img
    #normal node:co
    bump_node = all_nodes.get('Bump')
    n_map1 = all_nodes.get('Normal Map')
    normal_img = bpy.data.images.load(filepath = common_path+directory_name+'/'+ni_file)
    normal = n_map1.inputs[1].links[0].from_node
    normal.image = normal_img
    #displacement node:
    #mat_out = all_nodes.get('Material Output')
    #disp_map = mat_out.inputs[2].links[0].from_node
    displacement = bump_node.inputs[2].links[0].from_node
    disp_img = bpy.data.images.load(filepath = common_path+directory_name+'/'+di_file)
    displacement.image = disp_img
    '''
    n_map1 = principled_bsdf.inputs[20].links[0].from_node
    normal_img = bpy.data.images.load(filepath = common_path+directory_name+'/'+ni_file)
    normal = n_map1.inputs[1].links[0].from_node
    normal.image = normal_img
    #displacement node:
    mat_out = all_nodes.get('Material Output')
    disp_map = mat_out.inputs[2].links[0].from_node
    displacement = disp_map.inputs[0].links[0].from_node
    disp_img = bpy.data.images.load(filepath = common_path+directory_name+'/'+di_file)
    displacement.image = disp_img
    '''
selec_texture = {1:'ShaderNodeTexNoise',2:'ShaderNodeTexMusgrave',3:'ShaderNodeTexVoronoi'}
vornoi_distance = {1:'EUCLIDEAN',2:'MANHATTAN',3:'CHEBYCHEV'}
musgrave_types = {1:'MULTIFRACTAL',2:'FBM',3:'HETERO_TERRAIN'}


def edit_graph():
    base_material = bpy.data.materials['base_material2.001']
    all_nodes = base_material.node_tree.nodes
    tex_cord = all_nodes.get('Texture Coordinate')
    mix_shader1 = tex_cord.outputs[3].links[0].to_node
    present_node = mix_shader1.inputs[1].links[0].from_node
    selected_texture = random.randrange(1,4)
    selected_type = random.randrange(1,4)
    all_nodes.remove(present_node)
    next_node = all_nodes.new(selec_texture[selected_texture])
    next_node.location = (-1000,200)
    link = base_material.node_tree.links.new
    if selected_texture == 1:
        link(next_node.outputs[1],mix_shader1.inputs[1])
    else:
        link(next_node.outputs[0],mix_shader1.inputs[1])
    next_node.inputs[2].default_value = (random.randrange(0,15))
    if selected_texture == 2:
        next_node.musgrave_type = musgrave_types[selected_type]
    elif selected_texture == 3:
        next_node.distance = vornoi_distance[selected_type]
    selected_texture = random.randrange(1,4)
    selected_type = random.randrange(1,4)
    grad_cord = all_nodes.get('Gradient Texture')
    mix_shader2 = grad_cord.outputs[0].links[0].to_node
    mapping_node = grad_cord.inputs[0].links[0].from_node
    present_node = mix_shader2.inputs[2].links[0].from_node
    temp_loc = present_node.location
    all_nodes.remove(present_node)
    next_node = all_nodes.new(selec_texture[selected_texture])
    next_node.location = temp_loc
    link(next_node.inputs[0],mapping_node.outputs[0])
    if selected_texture == 1:
        link(next_node.outputs[1],mix_shader2.inputs[2])
    else:
        link(next_node.outputs[0],mix_shader2.inputs[2])
    next_node.inputs[2].default_value = (random.randrange(0,15))
    if selected_texture == 2:
        next_node.musgrave_type = musgrave_types[selected_type]
    elif selected_texture == 3:
        next_node.distance = vornoi_distance[selected_type]
    color_ramp1 = all_nodes.get('ColorRamp')
    b1 = random.randrange(0,450)
    c1 = random.randrange(b1+50,650)
    color_ramp1.color_ramp.elements[0].position = (b1/1000)
    color_ramp1.color_ramp.elements[1].position = (c1/1000)
    
cwd = os.getcwd()
os.chdir('/home/supratik/Pictures/blender_progression/textures/ambientcg')
directories = glob.glob('*JPG*')
os.chdir(cwd)

scene = bpy.context.scene
dir_len = len(directories)
for name in directories:
    print(name)
for i in range(dir_len-1):
    for j in range(i+1,dir_len):
        edit_graph()
        get_materials(directories[i],0)    
        get_materials(directories[j],1)
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = '/home/supratik/Pictures/blender_progression/data_set/'+directories[i]+'_'+directories[j]+'(1).png'
        bpy.ops.render.render(write_still = 1)             
        print('rendered:{} and {}'.format(directories[i],directories[j]))
        time.sleep(15)
        print('went to sleep for 15 seconds!')
