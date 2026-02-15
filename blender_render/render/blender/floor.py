import bpy
from .materials import floor_mat


def get_trajectory(data, is_mesh):
    if is_mesh:
        # mean of the vertices
        trajectory = data[:, :, [0, 1]].mean(1)
    else:
        # get the root joint
        trajectory = data[:, 0, [0, 1]]
    return trajectory


# def plot_floor(data, big_plane=True):
#     # Create a floor
#     minx, miny, _ = data.min(axis=(0, 1))
#     maxx, maxy, _ = data.max(axis=(0, 1))
#     minz = 0

#     location = ((maxx + minx)/2, (maxy + miny)/2, 0)
#     scale = ((maxx - minx)/2, (maxy - miny)/2, 1)

#     bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

#     bpy.ops.transform.resize(value=scale, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
#                              constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
#                              proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
#                              use_proportional_projected=False, release_confirm=True)
#     obj = bpy.data.objects["Plane"]
#     obj.name = "SmallPlane"
#     obj.data.name = "SmallPlane"

#     if not big_plane:
#         obj.active_material = floor_mat(color=(0.2, 0.2, 0.2, 1))
#     else:
#         obj.active_material = floor_mat(color=(0.1, 0.1, 0.1, 1))

#     if big_plane:
#         location = ((maxx + minx)/2, (maxy + miny)/2, -0.01)
#         bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

#         bpy.ops.transform.resize(value=[2*x for x in scale], orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
#                                  constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
#                                  proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
#                                  use_proportional_projected=False, release_confirm=True)

#         obj = bpy.data.objects["Plane"]
#         obj.name = "BigPlane"
#         obj.data.name = "BigPlane"
#         obj.active_material = floor_mat(color=(0.2, 0.2, 0.2, 1))


def plot_floor_2(minsxy, big_plane=False):
    # Create a floor
    # minx, miny, _ = data.min(axis=(0, 1))
    # maxx, maxy, _ = data.max(axis=(0, 1))
    minx, maxx, miny, maxy = minsxy
    minz = 0
    coef = 2
    scale = (0.5, 0.5, 1)
    name_list = []
    coefx = int((maxx - minx))+1
    coefy = int((maxy - miny))+1
    startx = -coefx * 0.5
    starty = -coefy * 0.5
    for xx in range(coefx):
        for yy in range(coefy):
            location = (startx+(xx*2+1)*0.5, starty+(yy*2+1)*0.5, 0)
            # print(location)
            bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

            bpy.ops.transform.resize(value=scale, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                    constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
                                    proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                                    use_proportional_projected=False, release_confirm=True)
            obj = bpy.data.objects["Plane"]
            obj.name = "SmallPlane" + str((xx) * coefx + yy)
            obj.data.name = "SmallPlane" + str((xx) * coefx + yy)
            # if ((1+xx) * coef + yy+2) % 2 == 0:
            #     obj.active_material = floor_mat(color=(0.1, 0.1, 0.1, 1), image=True)
            # else:
            #     obj.active_material = floor_mat(color=(0.2, 0.2, 0.2, 1), image=True)
            
            obj.active_material = floor_mat(color=(1, 1, 1, 1), image=True)
            name_list.append(obj.name)
    return name_list


def plot_floor_teaser_video(minsxy, big_plane=True):
    # Create a floor
    # minx, miny, _ = data.min(axis=(0, 1))
    # maxx, maxy, _ = data.max(axis=(0, 1))
    minx, maxx, miny, maxy = minsxy
    minz = 0
    coef = 1
    scale = ((maxy - miny)/coef/2, (maxy - miny)/coef/2, 1)
    name_list = []
    for xx in range(0, int((maxx - minx) / ((maxy - miny)/coef)) + 2):
        for yy in range(0, int(coef)+1):
            location = ((2 * xx - 1.2) * (maxy - miny)/coef/2, (2 * yy - 1.2) * (maxy - miny)/coef/2, 0)
            # print(location)
            bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

            bpy.ops.transform.resize(value=scale, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                    constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
                                    proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                                    use_proportional_projected=False, release_confirm=True)
            obj = bpy.data.objects["Plane"]
            obj.name = "SmallPlane" + str((1+xx) * coef + yy+2)
            obj.data.name = "SmallPlane" + str((1+xx) * coef + yy+2)
            if ((1+xx) * coef + yy+2) % 2 == 0:
                obj.active_material = floor_mat(color=(0.1, 0.1, 0.1, 1), image=True)
            else:
                obj.active_material = floor_mat(color=(0.2, 0.2, 0.2, 1), image=True)

            name_list.append(obj.name)
    return name_list
    # if not big_plane:
    #     obj.active_material = floor_mat(color=(0.7, 0.7, 0.7, 1))
    # else:
    #     obj.active_material = floor_mat(color=(0.1, 0.1, 0.1, 1))

    # if big_plane:
    #     location = ((maxx + minx)/2, (maxy + miny)/2, -0.02)
    #     bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

    #     bpy.ops.transform.resize(value=[x*1.2 for x in scale], orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
    #                              constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
    #                              proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
    #                              use_proportional_projected=False, release_confirm=True)

    #     obj = bpy.data.objects["Plane"]
    #     obj.name = "BigPlane"
    #     obj.data.name = "BigPlane"
    #     obj.active_material = floor_mat(color=(0.2, 0.2, 0.2, 1))

from mathutils import Matrix

def plot_floor(data, big_plane=False, color=(0.2, 0.2, 0.2, 0), scale_factor=0.90, rotation_matrix=None):
    # Create a floor
    minx, miny, _ = data.min(axis=(0, 1))
    maxx, maxy, _ = data.max(axis=(0, 1))
    minz = 0
    scale_xy = max((maxx - minx), (maxy - miny)) * scale_factor
    location = ((maxx + minx) / 2, (maxy + miny) / 2, 0)
    scale = (scale_xy, scale_xy, 1)

    # Create the small plane
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
    bpy.ops.transform.resize(value=scale, orient_type='GLOBAL', release_confirm=True)
    obj = bpy.context.active_object
    obj.name = "SmallPlane"
    obj.data.name = "SmallPlane"
    obj.active_material = create_floor_material(color)
    # obj.active_material = floor_mat(color=(1, 1, 1, 1), image=True)
    # ✅ Apply rotation if provided
    if rotation_matrix is not None:
        rot_np = rotation_matrix.cpu().numpy()
        rot4x4 = Matrix.Identity(4)
        for i in range(3):
            for j in range(3):
                rot4x4[i][j] = rot_np[i][j]
        obj.matrix_world = rot4x4 @ obj.matrix_world

    # Create a larger plane if big_plane is True
    if big_plane:
        location = ((maxx + minx) / 2, (maxy + miny) / 2, -0.02)
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
        bpy.ops.transform.resize(value=[x * 1.4 for x in scale], orient_type='GLOBAL', release_confirm=True)
        obj = bpy.context.active_object
        obj.name = "BigPlane"
        obj.data.name = "BigPlane"
        obj.active_material = create_floor_material((0.1, 0.1, 0.1, 1))

        # ✅ Apply same rotation to BigPlane
        if rotation_matrix is not None:
            obj.matrix_world = rot4x4 @ obj.matrix_world


# def plot_floor(data, big_plane=False, color=(0.2, 0.2, 0.2, 1), scale_factor=0.85):
#     # Create a floor
#     minx, miny, _ = data.min(axis=(0, 1))
#     maxx, maxy, _ = data.max(axis=(0, 1))
#     minz = 0
#     scale_xy = max((maxx - minx), (maxy - miny)) * scale_factor
#     location = ((maxx + minx) / 2, (maxy + miny) / 2, 0)
#     scale = (scale_xy, scale_xy, 1)

#     # Create the small plane
#     bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
#     bpy.ops.transform.resize(value=scale, orient_type='GLOBAL', release_confirm=True)
#     obj = bpy.context.active_object
#     obj.name = "SmallPlane"
#     obj.data.name = "SmallPlane"

#     # Apply material with the specified color
#     obj.active_material = create_floor_material(color)

#     # Create a larger plane if big_plane is True
#     if big_plane:
#         location = ((maxx + minx) / 2, (maxy + miny) / 2, -0.02)
#         bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
#         bpy.ops.transform.resize(value=[x * 1.4 for x in scale], orient_type='GLOBAL', release_confirm=True)
#         obj = bpy.context.active_object
#         obj.name = "BigPlane"
#         obj.data.name = "BigPlane"
#         obj.active_material = create_floor_material((0.1, 0.1, 0.1, 1))  # Darker color for the big plane

# Helper function to create a material with a specific color
def create_floor_material(color):
    mat_name = "Custom_Floor_Material"
    if mat_name in bpy.data.materials:
        mat = bpy.data.materials[mat_name]
    else:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
    
    # Set the color in the Principled BSDF
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 0.6  # Slightly rough
    
    return mat

def plot_floor_teaser(minsxy, big_plane=False):
    # Create a floor
    # minx, miny, _ = data.min(axis=(0, 1))
    # maxx, maxy, _ = data.max(axis=(0, 1))
    minz = 0
    minx, maxx, miny, maxy = minsxy
    # minsxy = (minx * 3.5, maxx * 3.5, miny * 2.2, maxy * 2.2)
    location = ((maxx + minx)/2, (maxy + miny)/2, 0)
    scale = ((maxx - minx)/2, (maxy - miny)/2, 1)

    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

    bpy.ops.transform.resize(value=[(maxx - minx), (maxy - miny), 1], orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                             constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                             use_proportional_projected=False, release_confirm=True)

    obj = bpy.data.objects["Plane"]
    obj.name = "SmallPlane"
    obj.data.name = "SmallPlane"

    # MAT_NAME = "TackyGold"
    # bpy.data.materials.new(MAT_NAME)
    # material = bpy.data.materials[MAT_NAME]
    # material.use_nodes = True
    # material.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.3
    # material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)
    # material.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.3
    # if len(obj.data.materials.items()) != 0:
    #     obj.data.materials.clear()
    # else:
    #     obj.data.materials.append(material)

    # if not big_plane:
    obj.active_material = floor_mat(color=(0.6, 0.6, 0.6, 0.6))
    # else:
    #     obj.active_material = floor_mat(color=(0.1, 0.1, 0.1, 1))

    # if big_plane:
    location = ((maxx + minx)/2, (maxy + miny)/2, -0.1)
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))

    bpy.ops.transform.resize(value=[1.02*x for x in scale], orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False,
                                proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                                use_proportional_projected=False, release_confirm=True)

    obj = bpy.data.objects["Plane"]
    obj.name = "BigPlane"
    obj.data.name = "BigPlane"
    obj.active_material = floor_mat(color=(0.2, 0.2, 0.2, 0.6))

def show_traj(coords, id):
    # create the Curve Datablock
    curveData = bpy.data.curves.new('myCurve'+str(id), type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    # map coords to spline
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords)-1)
    material = bpy.data.materials.new("myCurve"+"_material")
    material.diffuse_color = (0.50,0.3,0,1.0)
    curveData.materials.append(material)
    for i, coord in enumerate(coords):
        x, y = coord
        polyline.points[i].co = (x, y, 0.001, 1)

    # create Object
    curveOB = bpy.data.objects.new('myCurve'+str(id), curveData)
    curveData.bevel_depth = 0.01
    bpy.context.collection.objects.link(curveOB)