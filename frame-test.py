import bpy
import math

bpy.ops.object.mode_set(mode = 'OBJECT')

context = bpy.context
scene = context.scene

ref_frame = "Cylinder-Sta53.001-JunkoTest"
ref_cross_section = "Sta53.5-CrossSect"

frame_cyl = bpy.data.objects.get(ref_frame)

# Function to duplicate object, move it to 3D cursor location, and rotate it appropriately
def duplicate_object_to_cursor(object_name, vertex_iter):
    # 1. Get the original object from bpy.data.objects
    original_obj = bpy.data.objects.get(object_name)
    if original_obj is None:
        print(f"Error: Object '{object_name}' not found.")
        return

    # 2. Get the 3D cursor's current location
    cursor_location = bpy.context.scene.cursor.location
    
    # 3. Duplicate the object using the data API (creates a new object data reference)
    # The new object will share the mesh data (linked duplicate by data API approach)
    new_obj_data = original_obj.data
    new_obj = bpy.data.objects.new(f"{object_name}.{vertex_iter}", new_obj_data)
    
    # 4. Link the new object to the active collection so it appears in the scene
    bpy.context.collection.objects.link(new_obj)
    
    # Set the location and rotation of the new object to the cursor's location
    new_obj.location = cursor_location
    new_obj.rotation_euler[1] += math.radians(90 + 360/64*vertex_iter)  # Rotate 90° (because reference cross section is not at vertex 0) plus 1/64th of 360 for each iteration around Y axis

# Set mode to edit
bpy.ops.object.mode_set(mode = 'EDIT') 
# Change select mode to vertices
bpy.ops.mesh.select_mode(type="VERT")
# Unselect everything
bpy.ops.mesh.select_all(action = 'DESELECT')
# Change to Object mode
bpy.ops.object.mode_set(mode = 'OBJECT')
# Select vertex i
i = 0
for i in range(64):
    # Select vertex i of reference frame cylinder to get its x, y, z location
    frame_cyl.data.vertices[i].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 
    v_loc = frame_cyl.data.vertices[i]

    # Move 3D cursor to vertex i
    scene.cursor.location = frame_cyl.matrix_world @ v_loc.co

    # Duplicate reference cross section to each vertex and rotate as needed
    duplicate_object_to_cursor(ref_cross_section, i)