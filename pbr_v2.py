import os
import bpy
import glob
'''
Here it is assumed that PBR node setup is already done manually
How? First New Material -> click on Principled BSDF -> click Ctrl + Shift + T
Now save the name of this material as bm.004
'''
bpy.ops.mesh.primitive_cube_add(size=4, location=(0,0,2))
cube = bpy.context.active_object
base_material = bpy.data.materials['bm.004']
all_nodes = base_material.node_tree.nodes
cwd = os.getcwd()
os.chdir('../castle_wall_slates_4k.blend/textures')
#below scheme assumes that we have our files with correct nomenclature in our folder
bi_file =  glob.glob('*diff*')[0]
ri_file =  glob.glob('*rough*')[0]
ni_file =  glob.glob('*nor*')[0]
di_file =  glob.glob('*disp*')[0]
os.chdir(cwd)
principled_bsdf = all_nodes.get('Principled BSDF')
base_color = principled_bsdf.inputs[0].links[0].from_node
base_img = bpy.data.images.load(filepath = '/home/supratik/Downloads/castle_wall_slates_4k.blend/textures/'+bi_file)
base_color.image = base_img
#figuring thisout was very difficult ;)
#roughness node:
roughness = principled_bsdf.inputs[7].links[0].from_node
rough_img = bpy.data.images.load(filepath = '/home/supratik/Downloads/castle_wall_slates_4k.blend/textures/'+ni_file)
roughness.image = rough_img
#normal node:
n_map1 = principled_bsdf.inputs[20].links[0].from_node
normal_img = bpy.data.images.load(filepath = '/home/supratik/Downloads/castle_wall_slates_4k.blend/textures/'+ri_file)
normal = n_map1.inputs[1].links[0].from_node
normal.image = normal_img
#displacement node:
mat_out = all_nodes.get('Material Output')
disp_map = mat_out.inputs[2].links[0].from_node
displacement = disp_map.inputs[0].links[0].from_node
disp_img = bpy.data.images.load(filepath = '/home/supratik/Downloads/castle_wall_slates_4k.blend/textures/'+di_file)
displacement.image = disp_img
