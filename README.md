# Thesis_Project_Utorornto
This Project contains my Blender Python Scripts for generation of Synthetic DataSet
I am using Python's Blender API for generating phases of different materials.
Project work done under the supervision of Dr. Sagi Eppel
1. For Running the latest scripts, go to large_scale_dataset branch and then to dataset_with_annotation1 folder, first run node_graph_creation.py, then setup pbr using steps listed in my preious mail and then the other script.

2. The file names are node_graph_creation.py and data_set_creation_annotation.py . First run node_graph_creation.py to initialize the graph, then run data_Set_creation_annotation.py for the dataset generation. These are to be run by pasting the code in blender's scripting panel and then pressing the run button.
3. Before running the dataset creation file, go to the shading tab in blender, click on the Principled BSDF nodes one by one. Do this for each Principled BSDF: after clicking on the node press, Ctrl+shift+T a dialog box appears to select the necessary PBR files, select the ones that are actually PBR files. Now disconnect the connection coming out of the generated Displacement node, add a Bump Node, to this connect output of Normal Map Node to Normal Input of Bump node and connect output of the Displacement node to the Height input of the bump node. Please see the attached png file for a visual representation of this PBR setup.
4. My directory setup: 
PBR textures are stored in : '/home/supratik/Pictures/blender_progression/textures/ambientcg'
Dataset is stored in: '/home/supratik/Pictures/blender_progression/data_set/'
Blender is running in: '/home/supratik/Downloads/blender'
Sample dataset can be found at this link: https://drive.google.com/drive/folders/10eAnbm4eHnkoIeNKqnkG19xnLS-TfWEN?usp=sharing
Also opencv does not work directly in Blender, if you have not used it earlier. To fix this, use this answer:
https://blender.stackexchange.com/a/122337
Thanks and Regards,
Supratik
