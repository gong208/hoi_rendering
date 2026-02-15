import bpy
import numpy as np
import random
import os

def mesh_detect(data):
    # heuristic
    if data.shape[1] > 1000:
        return True
    return False


# see this for more explanation
# https://gist.github.com/iyadahmed/7c7c0fae03c40bd87e75dc7059e35377
# This should be solved with new version of blender
class ndarray_pydata(np.ndarray):
    def __bool__(self) -> bool:
        return len(self) > 0

# def load_numpy_vertices_into_blender(vertices, faces, name, mat):
#     mesh = bpy.data.meshes.new(name)
#     mesh.from_pydata(vertices, [], faces.view(ndarray_pydata))
#     mesh.validate()

#     obj = bpy.data.objects.new(name, mesh)
#     bpy.context.scene.collection.objects.link(obj)
    
#     # Create a UV Map
#     mesh.uv_layers.new(name="UVMap")

#     # Loop through each face and assign UV coordinates
#     for poly in mesh.polygons:
#         for loop_index in poly.loop_indices:
#             loop_vert_index = mesh.loops[loop_index].vertex_index
#             # Simple mapping for demonstration
#             uv_coords = (vertices[loop_vert_index][0], vertices[loop_vert_index][1])
#             mesh.uv_layers.active.data[loop_index].uv = uv_coords

#     bpy.ops.object.select_all(action='DESELECT')
#     obj.select_set(True)
#     # obj.active_material = mat
#     bpy.context.view_layer.objects.active = obj
#     if len(mesh.materials):
#         mesh.materials[0] = mat
#     else:
#         mesh.materials.append(mat)
#     # bpy.ops.object.shade_smooth()
#     # bpy.ops.object.select_all(action='DESELECT')

#     # Update the mesh
#     mesh.update(calc_edges=True)
#     return True

# def load_numpy_vertices_into_blender(vertices, faces, name, mat):
#     mesh = bpy.data.meshes.new(name)
#     mesh.from_pydata(vertices, [], faces.view(ndarray_pydata))
#     mesh.validate()

#     obj = bpy.data.objects.new(name, mesh)
#     bpy.context.scene.collection.objects.link(obj)
    
#     # Create a UV Map
#     mesh.uv_layers.new(name="UVMap")

#     # Loop through each face and assign UV coordinates
#     for poly in mesh.polygons:
#         for loop_index in poly.loop_indices:
#             loop_vert_index = mesh.loops[loop_index].vertex_index
#             # Simple mapping for demonstration
#             uv_coords = (vertices[loop_vert_index][0], vertices[loop_vert_index][1])
#             mesh.uv_layers.active.data[loop_index].uv = uv_coords

#     bpy.ops.object.select_all(action='DESELECT')
#     obj.select_set(True)
#     # obj.active_material = mat
#     bpy.context.view_layer.objects.active = obj
#     if len(mesh.materials):
#         mesh.materials[0] = mat
#     else:
#         mesh.materials.append(mat)
#     # bpy.ops.object.shade_smooth()
#     # bpy.ops.object.select_all(action='DESELECT')

#     # Update the mesh
#     mesh.update(calc_edges=True)
#     return True
# def load_numpy_vertices_into_blender(vertices, faces, name, mat):
#     mesh = bpy.data.meshes.new(name)
#     mesh.from_pydata(vertices, [], faces.view(ndarray_pydata))
#     mesh.validate()
    
#     obj = bpy.data.objects.new(name, mesh)
#     bpy.context.scene.collection.objects.link(obj)
#     # print(obj.type)
#     bpy.ops.object.select_all(action='DESELECT')
#     obj.select_set(True)
#     obj.active_material = mat
#     bpy.context.view_layer.objects.active = obj
#     bpy.ops.object.shade_smooth()
#     bpy.ops.object.select_all(action='DESELECT')
#     return True

from mathutils import Matrix

def load_numpy_vertices_into_blender(vertices, faces, name, mat, rotation_matrix=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices.tolist(), [], faces.tolist())
    mesh.validate()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    obj.active_material = mat
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')

    # ✅ Apply rotation if provided
    if rotation_matrix is not None:
        rot_np = rotation_matrix.cpu().numpy()
        rot4x4 = Matrix.Identity(4)
        for i in range(3):
            for j in range(3):
                rot4x4[i][j] = rot_np[i][j]
        obj.matrix_world = rot4x4 @ obj.matrix_world

    return True

def load_numpy_vertices_into_blender_object(vertices, faces, name, mat, obj_name):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces.view(ndarray_pydata))
    mesh.validate()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    filepath = './objects/'+obj_name+'/'+obj_name+'.obj'
    bpy.ops.import_scene.obj(filepath=filepath)
    uv_template = bpy.context.selected_objects[0]
    materials = [mat for mat in uv_template.data.materials]

    bpy.context.view_layer.objects.active = uv_template
    obj.select_set(True)
    bpy.ops.object.join_uvs()

    # Delete template object from scene
    obj.select_set(False)
    uv_template.select_set(True)
    bpy.ops.object.delete()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # print(obj.type)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    for ma in materials:
        obj.data.materials.append(ma)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')

    return True

def load_numpy_vertices_into_blender_human(vertices, faces, name, mat):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces.view(ndarray_pydata))
    mesh.validate()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    uv_template_path = "./SMPL/smpl_uv.obj"
    print("Creating UV map from UV template: " + uv_template_path)
    bpy.ops.import_scene.obj(filepath=uv_template_path)
    uv_template = bpy.context.selected_objects[0]

    bpy.context.view_layer.objects.active = uv_template
    obj.select_set(True)
    bpy.ops.object.join_uvs()

    # Delete template object from scene
    obj.select_set(False)
    uv_template.select_set(True)
    bpy.ops.object.delete()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # print(obj.type)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    obj.active_material = mat
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')
    return True

def delete_objs(names):
    if not isinstance(names, list):
        names = [names]
    # bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        for name in names:
            if obj.name.startswith(name) or obj.name.endswith(name):
                obj.select_set(True)
    bpy.ops.object.delete()
    bpy.ops.object.select_all(action='DESELECT')

def delete_all():
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
    bpy.ops.object.delete()
    bpy.ops.object.select_all(action='DESELECT')