import os.path
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir)
sys.path.append("/media/volume/Sirui-2/miniconda3/envs/interact/lib/python3.9/site-packages")
import random
import torch
import torch.nn.functional as F
from tqdm import tqdm
import yaml
import trimesh
from scipy.spatial.transform import Rotation
from copy import copy
from utils.markerset import *
import argparse

import shutil
from human_body_prior.body_model.body_model import BodyModel
from pytorch3d.transforms import *
import torch.nn.functional as F

from os.path import join as pjoin

import numpy as np
import os
from common.quaternion import *
from paramUtil import *
from generate_video import gen_video
try:
    import bpy
    sys.path.append(os.path.dirname(bpy.data.filepath))
    
except ImportError:
    raise ImportError("Blender is not properly installed or not launch properly. See README.md to have instruction on how to install and use blender.")


import launch.blender
import launch.prepare  # noqa

from render.blender import render_sequence
from render.video import Video
import logging
import hydra
from omegaconf import DictConfig
import torch
import numpy as np
import os
from pytorch3d.transforms import *
import trimesh
import smplx
from common.quaternion import rotation_6d_to_matrix_np

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
to_cpu = lambda tensor: tensor.detach().cpu().numpy()

MODEL_PATH = '/media/volume/Sirui-2/blender/blender_render/models'


device = torch.device('cuda:0')
smplh_model_male = smplx.create(MODEL_PATH, model_type='smplh',
                            gender="male",
                            use_pca=False,
                            ext='pkl').to(device)

smplh_model_female = smplx.create(MODEL_PATH, model_type='smplh',
                        gender="female",
                        use_pca=False,
                        ext='pkl').to(device)

smplh_model_neutral = smplx.create(MODEL_PATH, model_type='smplh',
                        gender="neutral",
                        use_pca=False,
                        ext='pkl').to(device)
smpl_models2 = {'male': smplh_model_male, 'female': smplh_model_female, 'neutral': smplh_model_neutral}

# render_pose_guidance
# @hydra.main(version_base=None, config_path="configs", config_name="render_pose_zguidance")
@hydra.main(version_base=None, config_path="configs", config_name="render_pose_ours_no_aug")
def _render_cli(cfg: DictConfig):
    return render_cli(cfg)

def render_cli(cfg: DictConfig) -> None:
    data_root = "/media/volume/Sirui-2/blender/data/augmentations"
    if cfg.dir_name is not None:
        data_names = [f for f in os.listdir(os.path.join(data_root, cfg.dir_name)) if f.endswith('.npz')]
        for data_name in data_names:
            dir_data = os.path.join(cfg.dir_name, data_name)
            # data_root = '/media/volume/Sirui-2/blender/data/w_o_aug_data'
            # data_root = "/media/volume/Sirui-2/blender/data/chairs_baseline_compare"
            # data_root = "/media/volume/Sirui-2/blender/data/baseline_comparison_grab"
            
            # data_root = "/media/volume/Sirui-2/blender/data/compare_guidance"
            # data_root = "/media/volume/Sirui-2/blender/data/comparisons/comparison_wbaseline"
            # data_root = "/media/volume/Sirui-2/blender/data/ours_fig3"
            # data_root = "/media/volume/Sirui-2/blender/data/zaugcp"
            npz_path = os.path.join(data_root, dir_data)
            dataset_name = dir_data.split('/')[-2]
            sequence_name = dir_data.split('/')[-1]
            # render_path =f'./save_wo_aug/{dataset_name}/{cfg.name}'
            # render_path =f'./save_compare_chairs/{cfg.name}'
            # render_path =f'./save_compare_grabs/{cfg.name}'
            # render_path =f'./save_compare_augcp/{cfg.name}'
            render_path =f'./save_imhd/{dir_data}'
            # data = dict(np.load(os.path.join(npz_path, 'human.npz'),allow_pickle=True))
            data = dict(np.load(npz_path,allow_pickle=True))
            poses =data['poses']
            betas = data['betas']
            trans = data['trans']
            # gender = data['gender']
            print(f"loading {npz_path}")
            output = smplh_model_male(
                global_orient= torch.from_numpy(poses[:, :3]).float().to(device),
                body_pose=     torch.from_numpy(poses[:, 3:66]).float().to(device),
                left_hand_pose=  torch.from_numpy(poses[:, 66:111]).float().to(device),
                right_hand_pose= torch.from_numpy(poses[:, 111:156]).float().to(device),
                transl= torch.from_numpy(trans).float().to(device),
                betas=  torch.from_numpy(betas).repeat(poses.shape[0], 1).float().to(device),
                )
            verts = output.vertices
            if 1:
                # obj_start = 52*3+52*6+4+3
                obj_start = 52*3
                
            else:
                obj_start = 52*3+4

            motion = data['motion']
            print("motion shape", motion.shape)
            length = data['lengths']
            verts = verts[:length]
            motion = motion[:length]
            seq_names = data['seq_name']

            dataset_name1, obj_name = str(seq_names).rsplit('_',1)
            dataset_name1 = dataset_name1.split('_')[0]
            mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/imhd/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/objects/chairs/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/grab/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/omomo/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/augmentations/", dir_data.replace('.npz', '.obj'))
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/behave/objects", obj_name, obj_name + ".obj")
            obj_mesh = trimesh.load(mesh_path)
            print(f"loading {mesh_path}")
            obj_verts,obj_face = obj_mesh.vertices, obj_mesh.faces
            obj_verts_raw= obj_verts
            

            motion_obj = motion[:,obj_start:]
            obj_angles = motion_obj[...,:6]
            # obj_angles = motion_obj[...,-9:-3]
            obj_trans = motion_obj[...,6:]
            # obj_trans = motion_obj[...,-3:]



            angle_matrix = rotation_6d_to_matrix_np(obj_angles)

            obj_verts = (obj_verts)[None, ...]
            # print(angle_matrix.shape,obj_verts.shape,obj_trans.shape,'JKJ')
            obj_verts = np.matmul(obj_verts, np.transpose(angle_matrix, (0, 2, 1))) + obj_trans[:, None, :]
            print(f'output saved at {render_path}')

            render_sequence.render_sequence(
                    verts=verts.detach().cpu().numpy(), 
                    obj_verts=obj_verts, 
                    faces=smplh_model_male.faces.astype(np.int64), 
                    obj_face=obj_face.astype(np.int64),
                    frames_folder=render_path,
                    denoising=cfg.denoising,
                    oldrender=cfg.oldrender,
                    res="high",
                    canonicalize=cfg.canonicalize,
                    exact_frame=cfg.exact_frame,
                    num=cfg.num,
                    mode=cfg.mode,
                    downsample=cfg.downsample,
                    always_on_floor=cfg.always_on_floor,
                    init=True,
                    gt=cfg.gt,
                    ind=cfg.ind
                )
            if cfg.mode == "video":
                gen_video(render_path, sequence_name)

            del verts
            # , faces, object_verts, rot, trans
            torch.cuda.empty_cache()
            print(data['text'])
            # 清理 trimesh
            # del OBJ_MESH

            # 清理 Python 层内存

            # gc.collect()
    else:
        # data_root = '/media/volume/Sirui-2/blender/data/w_o_aug_data'
        # data_root = "/media/volume/Sirui-2/blender/data/chairs_baseline_compare"
        # data_root = "/media/volume/Sirui-2/blender/data/baseline_comparison_grab"
        
        # data_root = "/media/volume/Sirui-2/blender/data/compare_guidance"
        # data_root = "/media/volume/Sirui-2/blender/data/comparisons/comparison_wbaseline"
        # data_root = "/media/volume/Sirui-2/blender/data/ours_fig3"
        # data_root = "/media/volume/Sirui-2/blender/data/zaugcp"
        for name in cfg.name_list:
            npz_path = os.path.join(data_root, name)
            # dataset_name = cfg.name.split('/')[-2]
            sequence_name = name.split('/')[-1]
            # render_path =f'./save_wo_aug/{dataset_name}/{cfg.name}'
            # render_path =f'./save_compare_chairs/{cfg.name}'
            # render_path =f'./save_compare_grabs/{cfg.name}'
            # render_path =f'./save_compare_augcp/{cfg.name}'
            render_path =f'./save_augmentations/{name}'
            # data = dict(np.load(os.path.join(npz_path, 'human.npz'),allow_pickle=True))
            data = dict(np.load(npz_path,allow_pickle=True))
            poses =data['poses']
            betas = data['betas']
            trans = data['trans']
            # gender = data['gender']
            print(f"loading {npz_path}")
            output = smplh_model_male(
                global_orient= torch.from_numpy(poses[:, :3]).float().to(device),
                body_pose=     torch.from_numpy(poses[:, 3:66]).float().to(device),
                left_hand_pose=  torch.from_numpy(poses[:, 66:111]).float().to(device),
                right_hand_pose= torch.from_numpy(poses[:, 111:156]).float().to(device),
                transl= torch.from_numpy(trans).float().to(device),
                betas=  torch.from_numpy(betas).repeat(poses.shape[0], 1).float().to(device),
                )
            verts = output.vertices
            if 1:
                # obj_start = 52*3+52*6+4+3
                obj_start = 52*3
                
            else:
                obj_start = 52*3+4

            motion = data['motion']
            print("motion shape", motion.shape)
            length = data['lengths']
            verts = verts[:length]
            motion = motion[:length]
            seq_names = data['seq_name']

            dataset_name1, obj_name = str(seq_names).rsplit('_',1)
            dataset_name1 = dataset_name1.split('_')[0]
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/interactcodes/gt/{dataset_name1}/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/objects/chairs/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/imhd/objects", obj_name, obj_name + ".obj")
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/omomo/objects", obj_name, obj_name + ".obj")
            mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/augmentations/", name.replace('.npz', '.obj'))
            # mesh_path = os.path.join(f"/media/volume/Sirui-2/blender/data/data_gt/behave/objects", obj_name, obj_name + ".obj")
            obj_mesh = trimesh.load(mesh_path)
            print(f"loading {mesh_path}")
            obj_verts,obj_face = obj_mesh.vertices, obj_mesh.faces
            obj_verts_raw= obj_verts
            

            motion_obj = motion[:,obj_start:]
            obj_angles = motion_obj[...,:6]
            # obj_angles = motion_obj[...,-9:-3]
            obj_trans = motion_obj[...,6:]
            # obj_trans = motion_obj[...,-3:]



            angle_matrix = rotation_6d_to_matrix_np(obj_angles)

            obj_verts = (obj_verts)[None, ...]
            # print(angle_matrix.shape,obj_verts.shape,obj_trans.shape,'JKJ')
            obj_verts = np.matmul(obj_verts, np.transpose(angle_matrix, (0, 2, 1))) + obj_trans[:, None, :]
            print(f'output saved at {render_path}')

            render_sequence.render_sequence(
                    verts=verts.detach().cpu().numpy(), 
                    obj_verts=obj_verts, 
                    faces=smplh_model_male.faces.astype(np.int64), 
                    obj_face=obj_face.astype(np.int64),
                    frames_folder=render_path,
                    denoising=cfg.denoising,
                    oldrender=cfg.oldrender,
                    res="high",
                    canonicalize=cfg.canonicalize,
                    exact_frame=cfg.exact_frame,
                    num=cfg.num,
                    mode=cfg.mode,
                    downsample=cfg.downsample,
                    always_on_floor=cfg.always_on_floor,
                    init=True,
                    gt=cfg.gt,
                    ind=cfg.ind
                )
            if cfg.mode == "video":
                gen_video(render_path, sequence_name)

            del verts
            # , faces, object_verts, rot, trans
            torch.cuda.empty_cache()
            print(data['text'])
            # 清理 trimesh
            # del OBJ_MESH

            # 清理 Python 层内存

            # gc.collect()


if __name__ == "__main__":
    _render_cli()