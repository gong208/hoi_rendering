import bpy
from bpy import context, data, ops
import os

def clear_material(material):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()

# def colored_material_diffuse_BSDF(r, g, b, a=1, roughness=0.127451):
#     materials = bpy.data.materials
#     material = materials.new(name="body")
#     material.use_nodes = True
#     clear_material(material)
#     nodes = material.node_tree.nodes
#     links = material.node_tree.links
#     output = nodes.new(type='ShaderNodeOutputMaterial')
#     diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
#     diffuse.inputs["Color"].default_value = (r, g, b, a)
#     diffuse.inputs["Roughness"].default_value = roughness
#     links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])
#     return material

def colored_material_diffuse_BSDF(r, g, b, a=1, roughness=0.127451):
    materials = bpy.data.materials
    material = materials.new(name="body")
    material.use_nodes = True
    clear_material(material)

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Output
    output = nodes.new(type='ShaderNodeOutputMaterial')

    # Diffuse Shader
    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse.inputs["Color"].default_value = (r, g, b, a)
    diffuse.inputs["Roughness"].default_value = roughness

    if a >= 1.0:
        # Fully opaque — no need for transparency logic
        links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])
    else:
        # Transparent Shader
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        transparent.inputs['Color'].default_value = (r, g, b, 1)

        # Mix Shader
        mix = nodes.new(type='ShaderNodeMixShader')

        # Set mix factor to alpha
        mix.inputs['Fac'].default_value = a

        links.new(transparent.outputs['BSDF'], mix.inputs[1])
        links.new(diffuse.outputs['BSDF'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])

        # Important: enable blending
        material.blend_method = 'BLEND'
        material.shadow_method = 'HASHED'
        material.use_backface_culling = False

    return material


def colored_material_diffuse_BSDF_floor(r, g, b, a=1, roughness=0.127451):
    # materials = bpy.data.materials
    # material = materials.new(name="body")
    # material.use_nodes = True
    # # clear_material(material)
    # nodes = material.node_tree.nodes
    # links = material.node_tree.links

    # bsdf = nodes["Principled BSDF"]
    # if image == None:
    #     output = nodes.new(type='ShaderNodeOutputMaterial').inputs['Surface']
    # else:
    #     texture = nodes.new(type='ShaderNodeTexImage')
    #     texture.image = bpy.data.images.load('/Users/sirui/Codes/Human_Object_Interaction_Prediction/2145.jpg')
    #     output = texture.outputs['Color']
    # # output = nodes.new(type='ShaderNodeOutputMaterial')
    # # diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    # # diffuse.inputs["Color"].default_value = (r, g, b, a)
    # # diffuse.inputs["Roughness"].default_value = roughness
    # print(output)
    # links.new(bsdf.inputs['Base Color'], output)

    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    # texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    # # texImage.image = bpy.data.images.load("./floor.png")
    # texImage.image = bpy.data.images.load(r"C:/Users/DSC/Desktop/HOI/blender_render/blender_render/white_floor.png")
    # mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

    bsdf.inputs['Base Color'].default_value = (r, g, b, a)
    bsdf.inputs['Roughness'].default_value = roughness

    # # Add an Emission shader to ensure brightness
    # emission = mat.node_tree.nodes.new('ShaderNodeEmission')
    # emission.inputs['Color'].default_value = (r, g, b, a)
    # emission.inputs['Strength'].default_value = 1

    # # Mix the Emission shader with the Principled BSDF
    # mix_shader = mat.node_tree.nodes.new('ShaderNodeMixShader')
    # mat.node_tree.links.new(mix_shader.inputs[1], bsdf.outputs['BSDF'])
    # mat.node_tree.links.new(mix_shader.inputs[2], emission.outputs['Emission'])
    # mat.node_tree.links.new(mat.node_tree.nodes['Material Output'].inputs['Surface'], mix_shader.outputs['Shader'])


    # ob = context.view_layer.objects.active

    # # Assign it to object
    # if ob.data.materials:
    #     ob.data.materials[0] = mat
    # else:
    #     ob.data.materials.append(mat)
    return mat



# keys:
# ['Base Color', 'Subsurface', 'Subsurface Radius', 'Subsurface Color', 'Metallic', 'Specular', 'Specular Tint', 'Roughness', 'Anisotropic', 'Anisotropic Rotation', 'Sheen', 1Sheen Tint', 'Clearcoat', 'Clearcoat Roughness', 'IOR', 'Transmission', 'Transmission Roughness', 'Emission', 'Emission Strength', 'Alpha', 'Normal', 'Clearcoat Normal', 'Tangent']
DEFAULT_BSDF_SETTINGS = {"Subsurface": 0.15,
                         "Subsurface Radius": [1.1, 0.2, 0.1],
                         "Metallic": 0.7,
                         "Specular": 0.5,
                         "Specular Tint": 0.5,
                         "Roughness": 0.75,
                         "Anisotropic": 0.25,
                         "Anisotropic Rotation": 0.25,
                         "Sheen": 0.75,
                         "Sheen Tint": 0.5,
                         "Clearcoat": 0.5,
                         "Clearcoat Roughness": 0.5,
                         "IOR": 1.450,
                         "Transmission": 0.1,
                         "Transmission Roughness": 0.1,
                         "Emission": (0, 0, 0, 1),
                         "Emission Strength": 0.0,
                         "Alpha": 1.0}
import pdb
def body_material(r, g, b, a=1, name="body", oldrender=True):
    # pdb.set_trace() 
    if oldrender:
        material = colored_material_diffuse_BSDF(r, g, b, a=a)
    else:
        materials = bpy.data.materials
        material = materials.new(name=name)
        material.use_nodes = True
        nodes = material.node_tree.nodes
        diffuse = nodes["Principled BSDF"]
        inputs = diffuse.inputs

        settings = DEFAULT_BSDF_SETTINGS.copy()
        settings["Base Color"] = (r, g, b, a)
        settings["Subsurface Color"] = (r, g, b, a)
        settings["Subsurface"] = 0.0
        settings["Alpha"] = a

        for setting, val in settings.items():
            inputs[setting].default_value = val
    return material

def body_material_obj(obj_name):
    filepath = '../behave/objects/'+obj_name+'/'+obj_name+'.obj'
    bpy.ops.import_scene.obj(filepath=filepath)
    original_obj = bpy.context.selected_objects[0]
    materials = [mat for mat in original_obj.data.materials]
    # Delete the original object
    bpy.data.objects.remove(original_obj, do_unlink=True)
    return materials

def body_material_2(ind, name="body", oldrender=True):
    materials = bpy.data.materials
    material = materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    diffuse = nodes["Principled BSDF"]
    links = material.node_tree.links

    # Find texture node
    node_texture = None
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            node_texture = node
            break

    # Find shader node
    node_shader = None
    for node in nodes:
        if node.type.startswith('BSDF'):
            node_shader = node
            break
    # node_shader = material.node_tree.nodes["Principled BSDF"]
    
    print(node_texture, node_shader)
    texture_pathes = [('SMPLitex-texture-00000.png', 'SMPLitex-000', ''), ('SMPLitex-texture-00001.png', 'SMPLitex-001', ''), ('SMPLitex-texture-00002.png', 'SMPLitex-002', ''), ('SMPLitex-texture-00003.png', 'SMPLitex-003', ''), ('SMPLitex-texture-00004.png', 'SMPLitex-004', ''), ('SMPLitex-texture-00005.png', 'SMPLitex-005', ''), ('SMPLitex-texture-00006.png', 'SMPLitex-006', ''), ('SMPLitex-texture-00007.png', 'SMPLitex-007', ''), ('SMPLitex-texture-00008.png', 'SMPLitex-008', ''), ('SMPLitex-texture-00009.png', 'SMPLitex-009', ''), ('SMPLitex-texture-00010.png', 'SMPLitex-010', ''), ('SMPLitex-texture-00011.png', 'SMPLitex-011', ''), ('SMPLitex-texture-00012.png', 'SMPLitex-012', ''), ('SMPLitex-texture-00013.png', 'SMPLitex-013', ''), ('SMPLitex-texture-00014.png', 'SMPLitex-014', ''), ('SMPLitex-texture-00015.png', 'SMPLitex-015', ''), ('SMPLitex-texture-00016.png', 'SMPLitex-016', ''), ('SMPLitex-texture-00017.png', 'SMPLitex-017', ''), ('SMPLitex-texture-00018.png', 'SMPLitex-018', ''), ('SMPLitex-texture-00019.png', 'SMPLitex-019', ''), ('SMPLitex-texture-00020.png', 'SMPLitex-020', ''), ('SMPLitex-texture-00021.png', 'SMPLitex-021', ''), ('SMPLitex-texture-00022.png', 'SMPLitex-022', ''), ('SMPLitex-texture-00023.png', 'SMPLitex-023', ''), ('SMPLitex-texture-00024.png', 'SMPLitex-024', ''), ('SMPLitex-texture-00025.png', 'SMPLitex-025', ''), ('SMPLitex-texture-00026.png', 'SMPLitex-026', ''), ('SMPLitex-texture-00027.png', 'SMPLitex-027', ''), ('SMPLitex-texture-00028.png', 'SMPLitex-028', ''), ('SMPLitex-texture-00029.png', 'SMPLitex-029', ''), ('SMPLitex-texture-00030.png', 'SMPLitex-030', ''), ('SMPLitex-texture-00031.png', 'SMPLitex-031', ''), ('SMPLitex-texture-00032.png', 'SMPLitex-032', ''), ('SMPLitex-texture-00033.png', 'SMPLitex-033', ''), ('SMPLitex-texture-00034.png', 'SMPLitex-034', ''), ('SMPLitex-texture-00035.png', 'SMPLitex-035', ''), ('SMPLitex-texture-00036.png', 'SMPLitex-036', ''), ('SMPLitex-texture-00037.png', 'SMPLitex-037', ''), ('SMPLitex-texture-00038.png', 'SMPLitex-038', ''), ('SMPLitex-texture-00039.png', 'SMPLitex-039', ''), ('SMPLitex-texture-00040.png', 'SMPLitex-040', ''), ('SMPLitex-texture-00041.png', 'SMPLitex-041', ''), ('SMPLitex-texture-00042.png', 'SMPLitex-042', ''), ('SMPLitex-texture-00043.png', 'SMPLitex-043', ''), ('SMPLitex-texture-00044.png', 'SMPLitex-044', ''), ('SMPLitex-texture-00045.png', 'SMPLitex-045', ''), ('SMPLitex-texture-00046.png', 'SMPLitex-046', ''), ('SMPLitex-texture-00047.png', 'SMPLitex-047', ''), ('SMPLitex-texture-00048.png', 'SMPLitex-048', ''), ('SMPLitex-texture-00049.png', 'SMPLitex-049', ''), ('SMPLitex-texture-00050.png', 'SMPLitex-050', ''), ('SMPLitex-texture-00051.png', 'SMPLitex-051', ''), ('SMPLitex-texture-00052.png', 'SMPLitex-052', ''), ('SMPLitex-texture-00053.png', 'SMPLitex-053', ''), ('SMPLitex-texture-00054.png', 'SMPLitex-054', ''), ('SMPLitex-texture-00055.png', 'SMPLitex-055', ''), ('SMPLitex-texture-00056.png', 'SMPLitex-056', ''), ('SMPLitex-texture-00057.png', 'SMPLitex-057', ''), ('SMPLitex-texture-00058.png', 'SMPLitex-058', ''), ('SMPLitex-texture-00059.png', 'SMPLitex-059', ''), ('SMPLitex-texture-00060.png', 'SMPLitex-060', ''), ('SMPLitex-texture-00061.png', 'SMPLitex-061', ''), ('SMPLitex-texture-00062.png', 'SMPLitex-062', ''), ('SMPLitex-texture-00063.png', 'SMPLitex-063', ''), ('SMPLitex-texture-00064.png', 'SMPLitex-064', ''), ('SMPLitex-texture-00065.png', 'SMPLitex-065', ''), ('SMPLitex-texture-00066.png', 'SMPLitex-066', ''), ('SMPLitex-texture-00067.png', 'SMPLitex-067', ''), ('SMPLitex-texture-00068.png', 'SMPLitex-068', ''), ('SMPLitex-texture-00069.png', 'SMPLitex-069', ''), ('SMPLitex-texture-00070.png', 'SMPLitex-070', ''), ('SMPLitex-texture-00071.png', 'SMPLitex-071', ''), ('SMPLitex-texture-00072.png', 'SMPLitex-072', ''), ('SMPLitex-texture-00073.png', 'SMPLitex-073', ''), ('SMPLitex-texture-00074.png', 'SMPLitex-074', ''), ('SMPLitex-texture-00075.png', 'SMPLitex-075', ''), ('SMPLitex-texture-00076.png', 'SMPLitex-076', ''), ('SMPLitex-texture-00077.png', 'SMPLitex-077', ''), ('SMPLitex-texture-00078.png', 'SMPLitex-078', ''), ('SMPLitex-texture-00079.png', 'SMPLitex-079', ''), ('SMPLitex-texture-00080.png', 'SMPLitex-080', ''), ('SMPLitex-texture-00081.png', 'SMPLitex-081', ''), ('SMPLitex-texture-00082.png', 'SMPLitex-082', ''), ('SMPLitex-texture-00083.png', 'SMPLitex-083', ''), ('SMPLitex-texture-00084.png', 'SMPLitex-084', ''), ('SMPLitex-texture-00085.png', 'SMPLitex-085', ''), ('SMPLitex-texture-00086.png', 'SMPLitex-086', ''), ('SMPLitex-texture-00087.png', 'SMPLitex-087', ''), ('SMPLitex-texture-00088.png', 'SMPLitex-088', ''), ('SMPLitex-texture-00089.png', 'SMPLitex-089', ''), ('SMPLitex-texture-00090.png', 'SMPLitex-090', ''), ('SMPLitex-texture-00091.png', 'SMPLitex-091', ''), ('SMPLitex-texture-00092.png', 'SMPLitex-092', ''), ('SMPLitex-texture-00093.png', 'SMPLitex-093', ''), ('SMPLitex-texture-00094.png', 'SMPLitex-094', ''), ('SMPLitex-texture-00095.png', 'SMPLitex-095', ''), ('SMPLitex-texture-00096.png', 'SMPLitex-096', ''), ('SMPLitex-texture-00097.png', 'SMPLitex-097', ''), ('SMPLitex-texture-00098.png', 'SMPLitex-098', ''), ('SMPLitex-texture-00099.png', 'SMPLitex-099', ''), ('SMPLitex-texture-00100.png', 'SMPLitex-100', ''), ('SMPLitex-texture-00101.png', 'SMPLitex-101', ''), ('SMPLitex-texture-00102.png', 'SMPLitex-102', ''), ('SMPLitex-texture-00103.png', 'SMPLitex-103', ''), ('SMPLitex-texture-00104.png', 'SMPLitex-104', ''), ('SMPLitex-texture-00105.png', 'SMPLitex-105', ''), ('SMPLitex-texture-00106.png', 'SMPLitex-106', ''), ('SMPLitex-texture-00107.png', 'SMPLitex-107', ''), ('SMPLitex-texture-00108.png', 'SMPLitex-108', ''), ('SMPLitex-texture-00109.png', 'SMPLitex-109', ''), ('SMPLitex-texture-00110.png', 'SMPLitex-110', ''), ('SMPLitex-texture-00111.png', 'SMPLitex-111', ''), ('SMPLitex-texture-00112.png', 'SMPLitex-112', ''), ('SMPLitex-texture-00113.png', 'SMPLitex-113', ''), ('SMPLitex-texture-00114.png', 'SMPLitex-114', ''), ('SMPLitex-texture-00115.png', 'SMPLitex-115', ''), ('SMPLitex-texture-00116.png', 'SMPLitex-116', ''), ('SMPLitex-texture-00117.png', 'SMPLitex-117', ''), ('SMPLitex-texture-00118.png', 'SMPLitex-118', ''), ('SMPLitex-texture-00119.png', 'SMPLitex-119', ''), ('SMPLitex-texture-00120.png', 'SMPLitex-120', ''), ('SMPLitex-texture-00121.png', 'SMPLitex-121', ''), ('SMPLitex-texture-00122.png', 'SMPLitex-122', ''), ('SMPLitex-texture-00123.png', 'SMPLitex-123', ''), ('SMPLitex-texture-00124.png', 'SMPLitex-124', ''), ('SMPLitex-texture-00125.png', 'SMPLitex-125', ''), ('SMPLitex-texture-00126.png', 'SMPLitex-126', ''), ('SMPLitex-texture-00127.png', 'SMPLitex-127', ''), ('SMPLitex-texture-00128.png', 'SMPLitex-128', ''), ('SMPLitex-texture-00129.png', 'SMPLitex-129', ''), ('SMPLitex-texture-00130.png', 'SMPLitex-130', ''), ('SMPLitex-texture-00131.png', 'SMPLitex-131', ''), ('SMPLitex-texture-00132.png', 'SMPLitex-132', ''), ('SMPLitex-texture-00133.png', 'SMPLitex-133', ''), ('SMPLitex-texture-00134.png', 'SMPLitex-134', ''), ('SMPLitex-texture-00135.png', 'SMPLitex-135', ''), ('SMPLitex-texture-00136.png', 'SMPLitex-136', ''), ('SMPLitex-texture-00137.png', 'SMPLitex-137', ''), ('SMPLitex-texture-00138.png', 'SMPLitex-138', ''), ('SMPLitex-texture-00139.png', 'SMPLitex-139', ''), ('SMPLitex-texture-00140.png', 'SMPLitex-140', ''), ('SMPLitex-texture-00141.png', 'SMPLitex-141', ''), ('SMPLitex-texture-00142.png', 'SMPLitex-142', ''), ('SMPLitex-texture-00143.png', 'SMPLitex-143', ''), ('SMPLitex-texture-00144.png', 'SMPLitex-144', ''), ('SMPLitex-texture-00145.png', 'SMPLitex-145', ''), ('SMPLitex-texture-00146.png', 'SMPLitex-146', ''), ('SMPLitex-texture-00147.png', 'SMPLitex-147', ''), ('SMPLitex-texture-00148.png', 'SMPLitex-148', ''), ('SMPLitex-texture-00149.png', 'SMPLitex-149', ''), ('SMPLitex-texture-00150.png', 'SMPLitex-150', ''), ('SMPLitex-texture-00151.png', 'SMPLitex-151', ''), ('SMPLitex-texture-00152.png', 'SMPLitex-152', ''), ('SMPLitex-texture-00153.png', 'SMPLitex-153', ''), ('SMPLitex-texture-00154.png', 'SMPLitex-154', ''), ('SMPLitex-texture-00155.png', 'SMPLitex-155', ''), ('SMPLitex-texture-00156.png', 'SMPLitex-156', ''), ('SMPLitex-texture-00157.png', 'SMPLitex-157', ''), ('SMPLitex-texture-00158.png', 'SMPLitex-158', ''), ('SMPLitex-texture-00159.png', 'SMPLitex-159', ''), ('SMPLitex-texture-00160.png', 'SMPLitex-160', ''), ('SMPLitex-texture-00161.png', 'SMPLitex-161', ''), ('SMPLitex-texture-00162.png', 'SMPLitex-162', ''), ('SMPLitex-texture-00163.png', 'SMPLitex-163', ''), ('SMPLitex-texture-00164.png', 'SMPLitex-164', ''), ('SMPLitex-texture-00165.png', 'SMPLitex-165', ''), ('SMPLitex-texture-00166.png', 'SMPLitex-166', ''), ('SMPLitex-texture-00167.png', 'SMPLitex-167', ''), ('SMPLitex-texture-00168.png', 'SMPLitex-168', ''), ('SMPLitex-texture-00169.png', 'SMPLitex-169', ''), ('SMPLitex-texture-00170.png', 'SMPLitex-170', ''), ('SMPLitex-texture-00171.png', 'SMPLitex-171', ''), ('SMPLitex-texture-00172.png', 'SMPLitex-172', ''), ('SMPLitex-texture-00173.png', 'SMPLitex-173', ''), ('SMPLitex-texture-00174.png', 'SMPLitex-174', ''), ('SMPLitex-texture-00175.png', 'SMPLitex-175', ''), ('SMPLitex-texture-00176.png', 'SMPLitex-176', ''), ('SMPLitex-texture-00177.png', 'SMPLitex-177', ''), ('SMPLitex-texture-00178.png', 'SMPLitex-178', ''), ('SMPLitex-texture-00179.png', 'SMPLitex-179', ''), ('SMPLitex-texture-00180.png', 'SMPLitex-180', ''), ('SMPLitex-texture-00181.png', 'SMPLitex-181', ''), ('SMPLitex-texture-00182.png', 'SMPLitex-182', ''), ('SMPLitex-texture-00183.png', 'SMPLitex-183', ''), ('SMPLitex-texture-00184.png', 'SMPLitex-184', ''), ('SMPLitex-texture-00185.png', 'SMPLitex-185', ''), ('SMPLitex-texture-00186.png', 'SMPLitex-186', ''), ('SMPLitex-texture-00187.png', 'SMPLitex-187', ''), ('SMPLitex-texture-00188.png', 'SMPLitex-188', ''), ('SMPLitex-texture-00189.png', 'SMPLitex-189', ''), ('SMPLitex-texture-00190.png', 'SMPLitex-190', ''), ('SMPLitex-texture-00191.png', 'SMPLitex-191', ''), ('SMPLitex-texture-00192.png', 'SMPLitex-192', ''), ('SMPLitex-texture-00193.png', 'SMPLitex-193', ''), ('SMPLitex-texture-00194.png', 'SMPLitex-194', ''), ('SMPLitex-texture-00195.png', 'SMPLitex-195', ''), ('SMPLitex-texture-00196.png', 'SMPLitex-196', ''), ('SMPLitex-texture-00197.png', 'SMPLitex-197', ''), ('SMPLitex-texture-00198.png', 'SMPLitex-198', ''), ('SMPLitex-texture-00199.png', 'SMPLitex-199', '')]
    
    texture = texture_pathes[ind][0]
    if node_texture is None:
        node_texture = nodes.new(type="ShaderNodeTexImage")

    if texture not in bpy.data.images:
        # path = "."
        path = r"C:\Users\DSC\Desktop\HOI\blender_render\blender_render"
        texture_path = os.path.join(path, "texture", texture)
        print(texture_path)
        image = bpy.data.images.load(texture_path)
    else:
        image = bpy.data.images[texture]

    node_texture.image = image

    # Link texture node to shader node if not already linked
    if len(node_texture.outputs[0].links) == 0:
        # print(node_texture.outputs[0].links)
        links.new(node_texture.outputs['Color'], node_shader.inputs['Base Color'])

    # if bpy.context.space_data:
    #     if bpy.context.space_data.type == 'VIEW_3D':
    #         bpy.context.space_data.shading.type = 'MATERIAL'
    # inputs = diffuse.inputs

    # settings = DEFAULT_BSDF_SETTINGS.copy()
    # settings["Base Color"] = (r, g, b, a)
    # settings["Subsurface Color"] = (r, g, b, a)
    # settings["Subsurface"] = 0.0
    # settings["Alpha"] = a

    # for setting, val in settings.items():
    #     inputs[setting].default_value = val
    return material

def body_material_3(r, g, b, a=1, name="body", oldrender=False):
    if oldrender:
        material = colored_material_diffuse_BSDF(r, g, b, a=a)
    else:
        albedo_image_path = './texture/SMPLitex-texture-00000.png'
        normal_image_path = './SMPL/m_01_nrm.002.png'

        # Create a new material
        material = bpy.data.materials.new(name="AlbedoNormalMaterial")
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        texImage = material.node_tree.nodes.new('ShaderNodeTexImage')
        texImage.image = bpy.data.images.load(albedo_image_path)
        material.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
        print(albedo_image_path)
        # # Create and link albedo texture node
        # tex_image_albedo = material.node_tree.nodes.new('ShaderNodeTexImage')
        # tex_image_albedo.image = bpy.data.images.load(albedo_image_path)
        # # tex_image_albedo.location = (-300, 100)
        # material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image_albedo.outputs['Color'])
        # inputs = nodes["Principled BSDF"].inputs

        # settings = DEFAULT_BSDF_SETTINGS.copy()
        # settings["Base Color"] = (r, g, b, a)
        # settings["Subsurface Color"] = (r, g, b, a)
        # settings["Subsurface"] = 0.0
        # settings["Alpha"] = a

        # for setting, val in settings.items():
        #     inputs[setting].default_value = val
        # Create and link normal map node
        # tex_image_normal = material.node_tree.nodes.new('ShaderNodeTexImage')
        # tex_image_normal.image = bpy.data.images.load(normal_image_path)
        # # tex_image_normal.location = (-300, -100)
        # normal_map_node = material.node_tree.nodes.new('ShaderNodeNormalMap')
        # # normal_map_node.location = (-150, -100)
        # material.node_tree.links.new(normal_map_node.inputs['Color'], tex_image_normal.outputs['Color'])
        # material.node_tree.links.new(bsdf.inputs['Normal'], normal_map_node.outputs['Normal'])

        # materials = bpy.data.materials
        # material = materials.new(name=name)
        # material.use_nodes = True
        # nodes = material.node_tree.nodes
        # links = material.node_tree.links
        # # diffuse = nodes["Principled BSDF"]
        # # inputs = diffuse.inputs

        # # settings = DEFAULT_BSDF_SETTINGS.copy()
        # # settings["Base Color"] = (r, g, b, a)
        # # settings["Subsurface Color"] = (r, g, b, a)
        # # settings["Subsurface"] = 0.0
        # # settings["Alpha"] = a

        # # for setting, val in settings.items():
        # #     inputs[setting].default_value = val
        # # Clear default nodes
        # for node in nodes:
        #     nodes.remove(node)

        # # Create a Principled BSDF shader node
        # shader = nodes.new(type='ShaderNodeBsdfPrincipled')
        # shader.location = (0, 0)

        # # Add Texture nodes
        # albedo_node = nodes.new(type='ShaderNodeTexImage')
        # normal_node = nodes.new(type='ShaderNodeTexImage')
        # normal_map_node = nodes.new(type='ShaderNodeNormalMap')

        # albedo_node.location = (-300, 100)
        # normal_node.location = (-300, -100)
        # normal_map_node.location = (-150, -100)

        # # Load textures
        # albedo_image = bpy.data.images.load(albedo_path)
        # normal_image = bpy.data.images.load(normal_path)
        # print(albedo_image)

        # albedo_node.image = albedo_image
        # normal_node.image = normal_image

        # # Connect the nodes
        # links.new(shader.inputs['Base Color'], albedo_node.outputs['Color'])
        # links.new(normal_map_node.inputs['Color'], normal_node.outputs['Color'])
        # links.new(shader.inputs['Normal'], normal_map_node.outputs['Normal'])

    return material


def colored_material_bsdf(name, **kwargs):
    materials = bpy.data.materials
    material = materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    diffuse = nodes["Principled BSDF"]
    inputs = diffuse.inputs

    settings = DEFAULT_BSDF_SETTINGS.copy()
    for key, val in kwargs.items():
        settings[key] = val

    for setting, val in settings.items():
        inputs[setting].default_value = val

    return material


def floor_mat(name="floor_mat", color=(0.1, 0.1, 0.1, 1), roughness=0.127451, image=None):
    return colored_material_diffuse_BSDF_floor(color[0], color[1], color[2], a=color[3], roughness=roughness)


def plane_mat():
    materials = bpy.data.materials
    material = materials.new(name="plane")
    material.use_nodes = True
    clear_material(material)
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')
    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    checker = nodes.new(type="ShaderNodeTexChecker")
    checker.inputs["Scale"].default_value = 1024
    checker.inputs["Color1"].default_value = (0.8, 0.8, 0.8, 1)
    checker.inputs["Color2"].default_value = (0.3, 0.3, 0.3, 1)
    links.new(checker.outputs["Color"], diffuse.inputs['Color'])
    links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])
    diffuse.inputs["Roughness"].default_value = 0.127451
    return material


def plane_mat_uni():
    materials = bpy.data.materials
    material = materials.new(name="plane_uni")
    material.use_nodes = True
    clear_material(material)
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')
    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
    diffuse.inputs["Roughness"].default_value = 0.127451
    links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])
    return material
