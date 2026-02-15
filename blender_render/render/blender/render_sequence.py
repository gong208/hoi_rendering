import bpy
import os
import sys
import numpy as np
import math
import torch
# sys.path.remove('/Applications/Blender.app/Contents/Resources/2.93/python/lib/python3.9')
sys.path.append(
    '/Users/sirui/.local/lib/python3.9'
)
from .scene import setup_scene, setup_scene_old  # noqa
from .floor import show_traj, plot_floor, get_trajectory
from .vertices import prepare_vertices
from .tools import load_numpy_vertices_into_blender, delete_objs, mesh_detect
from .camera import Camera
from .sampler import get_frameidx
from tqdm import tqdm
import random

from PIL import Image

def clean_blender_scene():
    # 只选中非 Camera 的对象并删除
    for obj in bpy.data.objects:
        if obj.name != "Camera":
            bpy.data.objects.remove(obj, do_unlink=True)

    # 清理未被使用的数据块（mesh、材质等）
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)

    for block in bpy.data.lights:
        if block.users == 0:
            bpy.data.lights.remove(block)


    # 可选：清理 curve, textures 等也可以加上


def render_and_save_with_dpi(output_path, dpi=300):
    # Render the image
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

    # Set DPI with PIL (Pillow)
    image = Image.open(output_path)
    image.save(output_path, dpi=(dpi, dpi))
    # print(f"Image saved at {output_path} with {dpi} DPI.")


def render_current_frame(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(use_viewport=True, write_still=True)
    # file_path = path+'.blend'
    # bpy.ops.wm.save_as_mainfile(filepath=file_path)

    
def render_sequence(
    verts, obj_verts, faces, obj_face, frames_folder, *, 
    mode, gt=False, exact_frame=None, num=8, downsample=True,
    canonicalize=True, always_on_floor=False, denoising=True,
    oldrender=False, res="high", init=True, ind = 0, continue_render=0, dpi=512
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Convert inputs to GPU tensors
    verts = torch.tensor(verts, device=device, dtype=torch.float32)
    obj_verts = torch.tensor(obj_verts, device=device, dtype=torch.float32)
    faces = torch.tensor(faces, device=device, dtype=torch.int32)
    obj_face = torch.tensor(obj_face, device=device, dtype=torch.int32)

    # Calculate min and max coordinates using PyTorch
    min_xyz = torch.min(verts.min(dim=1)[0].min(dim=0)[0], 
                        obj_verts.min(dim=1)[0].min(dim=0)[0])
    max_xyz = torch.max(verts.max(dim=1)[0].max(dim=0)[0], 
                        obj_verts.max(dim=1)[0].max(dim=0)[0])

    minx, miny = min_xyz[0].item(), min_xyz[2].item()
    maxx, maxy = max_xyz[0].item(), max_xyz[2].item()

    # Height offset using GPU
    height_offset = torch.min(verts[:, :, 1].min(), obj_verts[:, :, 1].min()).item()
    
    # Apply transformations on GPU
    verts[:, :, 1] -= height_offset
    obj_verts[:, :, 1] -= height_offset
    verts[:, :, 0] -= (minx + maxx) / 2
    obj_verts[:, :, 0] -= (minx + maxx) / 2
    verts[:, :, 2] -= (miny + maxy) / 2
    obj_verts[:, :, 2] -= (miny + maxy) / 2

    # Step 1: 镜像 X
    # M_mirror_x = torch.tensor([
    #     [-1, 0, 0],
    #     [ 0, 1, 0],
    #     [ 0, 0, 1]
    # ], dtype=torch.float32, device=device)

    # # Step 2: 绕 Z 轴顺时针 45°
    # theta_z = math.radians(-205)
    # Rz = torch.tensor([
    #     [ math.cos(theta_z), -math.sin(theta_z), 0],
    #     [ math.sin(theta_z),  math.cos(theta_z), 0],
    #     [ 0,                 0,                  1]
    # ], dtype=torch.float32, device=device)

    # # Step 3: 绕 X 轴 -15°（抬起视角）
    # phi_x = math.radians(-15)
    # Rx = torch.tensor([
    #     [1, 0, 0],
    #     [0, math.cos(phi_x), -math.sin(phi_x)],
    #     [0, math.sin(phi_x),  math.cos(phi_x)]
    # ], dtype=torch.float32, device=device)

    # # Final: Rx @ Rz @ MirrorX
    # rotation_matrix = Rx @ Rz @ M_mirror_x

    # Apply Rotation using GPU (rotation matrix)
    rotation_matrix = torch.tensor([[1, 0, 0], [0, 1, 0], [0, 0, -1]], device=device, dtype=torch.float32)

    verts_rotated = torch.matmul(verts.reshape(-1, 3), rotation_matrix.T).reshape(verts.shape)
    obj_verts_rotated = torch.matmul(obj_verts.reshape(-1, 3), rotation_matrix.T).reshape(obj_verts.shape)
    # verts_rotated = verts
    # obj_verts_rotated = obj_verts

    # Convert back to CPU and NumPy for Blender rendering
    verts_np = verts_rotated.cpu().numpy()
    obj_verts_np = obj_verts_rotated.cpu().numpy()
    faces_np = faces.cpu().numpy()
    obj_face_np = obj_face.cpu().numpy()

    # GPU optimized operations are done, now using CPU for Blender
    if init:
        clean_blender_scene()

        setup_scene_old(res=res, denoising=denoising, oldrender=oldrender)

    # Build mesh list for Blender (CPU)
    from .meshes_sequence import Meshes
    # if gt:
    #     ind = 2
    # else:
    #     ind = 5
    ind = ind
    human_data = Meshes(verts_np, faces_np, gt='without' in frames_folder, mode=mode,
               canonicalize=canonicalize, always_on_floor=always_on_floor,
               human=True, oldrender=oldrender, ind=ind)
    obj_data = Meshes(obj_verts_np, obj_face_np, gt='without' in frames_folder, mode=mode,
               canonicalize=canonicalize, always_on_floor=always_on_floor,
               human=False, oldrender=oldrender, ind=ind)
    mesh_list = [human_data, obj_data]

    plot_floor(human_data.data, color=(1.0, 1.0, 1.0, 0))

    camera = Camera(first_root=human_data.get_root(0), mode=mode)
    camera.update(human_data.get_mean_root())
    # Render each frame
    nframes = verts.shape[0]
    imported_obj_names = []

    for index in range(0, nframes, (downsample + 1) + (downsample * 8)):
        # if index in range(29, 69):
        #     camera.update_2()
        if index >= continue_render:
            for data in mesh_list:
                frameidx = index
                frac = frameidx / (nframes - 1)
                mat = data.get_sequence_mat(frac)
                objname = data.load_in_blender(frameidx, mat)
                # Modify color intensity based on frame index
                # Modify color intensity based on frame index (darkening the original color)
                # if data.human:  # Only modify human mesh color
                #     darkness_factor = 0.3 + 0.7 * (index / nframes)  # 0.3 (lightest) to 1.0 (darkest)
                    
                #     # Retrieve the original color
                #     mat = bpy.data.objects[objname].active_material
                #     original_color = mat.diffuse_color[:3]  # Only RGB values

                #     # Apply darkness factor to the original color
                #     darkened_color = tuple([c * darkness_factor for c in original_color]) + (1.0,)
                #     mat.diffuse_color = darkened_color

                #     print(f"Adjusted human color for frame {index}: {darkened_color}")

                imported_obj_names.append(objname)

            name = f"{str(index).zfill(4)}"
            path_i = os.path.join(frames_folder, f"frame_{name}.png")
            render_current_frame(path_i)
            image = Image.open(path_i)
            image.save(path_i, dpi=(dpi, dpi))
            # print(f"Image saved at {path_i} with {dpi} DPI.")
            delete_objs(imported_obj_names)
            for mesh in list(bpy.data.meshes):
                if mesh.users == 0:
                    bpy.data.meshes.remove(mesh)

            for mat in list(bpy.data.materials):
                if mat.users == 0:
                    bpy.data.materials.remove(mat)
            # print(f"[DEBUG] frame {index}")
            # print(f"  - objects: {len(bpy.data.objects)}")
            # print(f"  - meshes: {len(bpy.data.meshes)}")
            # print(f"  - images: {len(bpy.data.images)}")
            # print(f"  - materials: {len(bpy.data.materials)}")


    delete_objs(["Plane", "Cylinder", "日光", "日光.001", "日光.002", "日光.003", "日光.004", "点光", "点光.001", "点光.002"])

    if mode == "video":
        return frames_folder
    else:
        return frames_folder
