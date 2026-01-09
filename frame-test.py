import bpy

bpy.ops.object.mode_set(mode = 'OBJECT')

context = bpy.context
scene = context.scene

frame_cyl = bpy.data.objects.get("Cylinder-Sta53.001-JunkoTest")
frame_cross_section = bpy.data.objects.get("Cylinder-Sta53.001-JunkoTest")

def duplicate_object_to_cursor(object_name, suffix):
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
    new_obj = bpy.data.objects.new(f"{object_name}.{suffix}", new_obj_data)
    
    # 4. Link the new object to the active collection so it appears in the scene
    bpy.context.collection.objects.link(new_obj)
    
    # 5. Set the location of the new object to the cursor's location
    new_obj.location = cursor_location
    
    print(f"Duplicated '{object_name}' to {tuple(cursor_location)} as '{new_obj.name}'")
    
    



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
for i in range(32):
    frame_cyl.data.vertices[i].select = True
    bpy.ops.object.mode_set(mode = 'EDIT') 

    v_loc = frame_cyl.data.vertices[i]

    scene.cursor.location = frame_cyl.matrix_world @ v_loc.co

    duplicate_object_to_cursor('Sta53.5-CrossSect', i)