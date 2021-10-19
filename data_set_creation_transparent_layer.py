'''
Procedure same as previous dataset creation file
here this code is to be run after running the pbr_onelayer_transparent.py
'''
import os
import bpy
import glob
import time
'''
Here it is assumed that PBR node setup is already done manually
How? First New Material -> click on Principled BSDF -> click Ctrl + Shift + T
Now save the name of this material as base_material2.001
'''
def get_materials(directory_name,part):
    '''
    takes in argument the directory_name as a string object and part 0: above layer, 1: below layer
    returns null
    '''
    base_material = bpy.data.materials['base_material2']
    all_nodes = base_material.node_tree.nodes
    cwd = os.getcwd()
    os.chdir('../../Pictures/blender_progression/textures/'+directory_name+'/textures/')
    #below scheme assumes that we have our files with correct nomenclature in our folder
    bi_file =  glob.glob('*diff*')[0]
    #change the above to color if the source web site changes from polyhaven to 
    ri_file =  glob.glob('*rough*')[0]
    ni_file =  glob.glob('*nor*')[0]
    di_file =  glob.glob('*disp*')[0]
    os.chdir(cwd)
    mix_shader = all_nodes.get('Mix Shader')
    principled_bsdf = mix_shader.inputs[1+part].links[0].from_node
    base_color = principled_bsdf.inputs[0].links[0].from_node
    base_img = bpy.data.images.load(filepath = '/home/supratik/Pictures/blender_progression/textures/'+directory_name+'/textures/'+bi_file)
    base_color.image = base_img
    #figuring thisout was very difficult ;)
    #roughness node:
    roughness = principled_bsdf.inputs[7].links[0].from_node
    rough_img = bpy.data.images.load(filepath = '/home/supratik/Pictures/blender_progression/textures/'+directory_name+'/textures/'+ri_file)
    roughness.image = rough_img
    #normal node:
    n_map1 = principled_bsdf.inputs[20].links[0].from_node
    normal_img = bpy.data.images.load(filepath = '/home/supratik/Pictures/blender_progression/textures/'+directory_name+'/textures/'+ni_file)
    normal = n_map1.inputs[1].links[0].from_node
    normal.image = normal_img
    #displacement node:
    mat_out = all_nodes.get('Material Output')
    disp_map = mat_out.inputs[2].links[0].from_node
    displacement = disp_map.inputs[0].links[0].from_node
    disp_img = bpy.data.images.load(filepath = '/home/supratik/Pictures/blender_progression/textures/'+directory_name+'/textures/'+di_file)
    displacement.image = disp_img


cwd = os.getcwd()
os.chdir('/home/supratik/Pictures/blender_progression/textures/')
directories = glob.glob('*blend*')
os.chdir(cwd)

scene = bpy.context.scene
'''
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "F:/image.png"
bpy.ops.render.render(write_still = 1)
'''
for name in directories:
    print(name)
for i in range(len(directories)):
    #for j in range(i,3):
    get_materials(directories[i],1)    
    #    get_materials(directories[j],1)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = '/home/supratik/Pictures/blender_progression/data_set/'+str(i)+'_'+'transparent.png'
    bpy.ops.render.render(write_still = 1)             
    print('rendered:')
    print(directories[i])
    #    print(directories[j])
    time.sleep(30)
    print('went to sleep for 30 seconds!')
