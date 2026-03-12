import numpy as np

from .materials import body_material, body_material_2, body_material_obj
import random
# green
# GT_SMPL = body_material(0.009, 0.214, 0.029)
GT_SMPL = body_material(0.035, 0.415, 0.122)

# blue
# GEN_SMPL = body_material(0.022, 0.129, 0.439)
# Blues => cmap(0.87)
GEN_SMPL = body_material(0.035, 0.322, 0.615)


# class Meshes:
#     def __init__(self, data, *, gt, mode, faces_path, canonicalize, always_on_floor, oldrender=True, **kwargs):
#         data = prepare_meshes(data, canonicalize=canonicalize, always_on_floor=always_on_floor)

#         self.faces = np.load(faces_path)
#         self.data = data
#         self.mode = mode
#         self.oldrender = oldrender

#         self.N = len(data)
#         self.trajectory = data[:, :, [0, 1]].mean(1)

#         if gt:
#             self.mat = GT_SMPL
#         else:
#             self.mat = GEN_SMPL

#     def get_sequence_mat(self, frac):
#         import matplotlib
#         cmap = matplotlib.cm.get_cmap('Blues')
#         # begin = 0.60
#         # end = 0.90
#         begin = 0.50
#         end = 0.90
#         rgbcolor = cmap(begin + (end-begin)*frac)
#         mat = body_material(*rgbcolor, oldrender=self.oldrender)
#         return mat

#     def get_root(self, index):
#         return self.data[index].mean(0)

#     def get_mean_root(self):
#         return self.data.mean((0, 1))

#     def load_in_blender(self, index, mat):
#         vertices = self.data[index]
#         faces = self.faces
#         name = f"{str(index).zfill(4)}"

#         from .tools import load_numpy_vertices_into_blender
#         load_numpy_vertices_into_blender(vertices, faces, name, mat)

#         return name

#     def __len__(self):
#         return self.N


class Meshes:
    def __init__(self, verts, faces, *, gt, mode, canonicalize, always_on_floor, oldrender=True, human=True, obj_name=None, ind = 0, rotation_matrix=None, **kwargs):
        self.rotation_matrix = rotation_matrix
        self.faces = faces
        self.data = verts[:, :, [0, 2, 1]]
        self.mode = mode
        self.oldrender = oldrender
        self.human = human
        self.N = len(verts)
        self.trajectory = self.data[:, :, [0, 1]].mean(1)
        self.gt = gt
        self.ind = ind
        self.obj_name = obj_name
        # if gt:
        #     self.mat = GT_SMPL
        # else:
        #     self.mat = GEN_SMPL

    def get_sequence_mat(self, frac):
        # import matplotlib
        # cmap1 = matplotlib.cm.get_cmap('gray')
        # cmap2 = matplotlib.cm.get_cmap('bone')
        # cmap3 = matplotlib.cm.get_cmap('pink')
        begin = 0.60
        end = 0.90
        begin = 0.60
        end = 0.40
        # if frac == 0:
        #     rgbcolor = (0.5, 0.5, 0.5, 1.0)
        index = 1 - frac
        ind = self.ind
        # if self.human:
        #     rgbcolor_1 = (0.55000000000000003, 0.5614583209634784, 0.6749998818750679, 1.0)
        #     rgbcolor_2 = (0.5, 0.5, 0.5, 1)
        # else:
        #     rgbcolor_1 = (0.6045917716877717, 0.4751095588105589, 0.3463816567126568, 1) # (0.556345443961444, 0.4781486013356014, 0.3324459883449883, 1.0)
        #     rgbcolor_2 = (0.3, 0.3, 0.3, 1)
        # rgbcolor = (rgbcolor_1[0] * (1 - index) + rgbcolor_2[0] * index, rgbcolor_1[1] * (1 - index) + rgbcolor_2[1] * index, rgbcolor_1[2] * (1 - index) + rgbcolor_2[2] * index, rgbcolor_1[3] * (1 - index) + rgbcolor_2[3] * index)
        
        # if self.human:
        #     mat = body_material_2(self.ind, oldrender=False)
        # else:
        #     mat = body_material(*rgbcolor, oldrender=self.oldrender)
        print("the read ind is :",ind)
        if self.human:
            # Set uniform color for human meshes
            if (ind==0):
                # rgbcolor_1 = (0.6, 0.35, 0.75, 1)       #ori(purple)
                rgbcolor_1 = (96.0/255, 181.0/255, 255.0/255, 1) #blue
            elif (ind==1):
                # rgbcolor_1 = (0.3, 0.55, 0.8, 1)     #flat(blue)
                rgbcolor_1 = (252.0/255, 199.0/255, 55.0/255, 1) # yellow
            elif (ind==2): # Our
                # rgbcolor_1 = (0.9, 0.5, 0.45, 1)     #mano(pink)
                rgbcolor_1 = (136.0/255, 158.0/255, 115.0/255, 1) # Sage
            elif (ind == 3):
                rgbcolor_1 = (254.0/255, 93.0/255, 38.0/255, 1) #Orange
            elif (ind == 4):
                rgbcolor_1 = (109.0/255, 225.0/255, 210.0/255, 1) #mint
            elif (ind == 5):
                rgbcolor_1 = (164.0/255, 204.0/255, 217.0/255, 1) # blue
            elif (ind == 6):
                # rgbcolor_1 = (0.4, 0.7, 0.3, 1)     #selected_2(green)
                rgbcolor_1 = (145.0/255, 18.0/255, 188.0/255, 1) # purple
            elif (ind == 7):
                rgbcolor_1 = (0.0/255, 128.0/255, 157.0/255, 1) # blue
            else:
                rgbcolor_1 = (70.0/255, 100.0/255, 255.0/255, 1) # blue
            mat = body_material(*rgbcolor_1, oldrender=self.oldrender)
            print('rgb:',rgbcolor_1)
        else:
            # Set uniform color for object meshes
            if (ind==0):
                # rgbcolor_2 = (0.75, 0.75, 0.25, 1)      #ori(yellow)
                rgbcolor_2 = (255.0/255, 145.0/255, 73.0/255, 1) #orange
            elif (ind==1):
                rgbcolor_2 = (231.0/255, 56.0/255, 121.0/255, 1) # pink
            elif (ind==2):
                # rgbcolor_2 = (0.3, 0.7, 0.35, 1)      #mano(green)
                rgbcolor_2 = (169.0/255, 74.0/255, 74.0/255, 1)
            elif (ind == 3):
                rgbcolor_2 = (242.0/255, 192.0/255, 120.0/255, 1) #Belge
            elif (ind == 4):
                rgbcolor_2 = (247.0/255, 90.0/255, 90.0/255, 1) #red
            elif (ind == 5):
                rgbcolor_2 = (249.0/255, 122.0/255, 0, 1) # yellow
            elif (ind == 6):
                rgbcolor_2 = (243.0/255, 159.0/255, 159.0/255, 1) # peach
            elif (ind == 7):
                rgbcolor_2 = (89.0/255, 172.0/255, 119.0/255, 1) # green
            else:
                rgbcolor_2 = (228.0/255, 218.0/255, 0.0/255, 1) # blue
                # rgbcolor_2 = (0.9, 0.45, 0.2, 1)    #selected_2(pink)
            mat = body_material(*rgbcolor_2, oldrender=self.oldrender)
            print('rgb:',rgbcolor_2)
        return mat
        # if self.human:
        #     rgbcolor_1 = (0.6545917716877717, 0.451095588105589, 0.2463816567126568, 1.0)
        #     rgbcolor_2 = (0.5, 0.5, 0.5, 1)
        # else:
        #     rgbcolor_1 = (0.35000000000000003, 0.4514583209634784, 0.6749998818750679, 1.0) # (0.7045917716877717, 0.5751095588105589, 0.4463816567126568, 1.0) # (0.556345443961444, 0.4781486013356014, 0.3324459883449883, 1.0)
        #     rgbcolor_2 = (0.6, 0.6, 0.6, 1)
    def get_root(self, index):
        return self.data[index].mean(0)

    def get_mean_root(self):
        return self.data.mean((0, 1))

    def load_in_blender(self, index, mat=None):
        vertices = self.data[index]
        faces = self.faces
        name = f"{str(index).zfill(4)}"

        from .tools import load_numpy_vertices_into_blender_object, load_numpy_vertices_into_blender_human
        from .tools import load_numpy_vertices_into_blender
        # if self.human:
        #     load_numpy_vertices_into_blender_human(vertices, faces, name, mat)
        # else:
        #     load_numpy_vertices_into_blender_object(vertices, faces, name, mat, self.obj_name)
        load_numpy_vertices_into_blender(vertices, faces, name, mat, rotation_matrix=self.rotation_matrix)
        return name

    def __len__(self):
        return self.N
    
def prepare_meshes(data, canonicalize=True, always_on_floor=False):
    if canonicalize:
        print("No canonicalization for now")

    # fix axis
    data[..., 1] = - data[..., 1]
    data[..., 0] = - data[..., 0]

    # Remove the floor
    data[..., 2] -= data[..., 2].min()

    # Put all the body on the floor
    if always_on_floor:
        data[..., 2] -= data[..., 2].min(1)[:, None]

    return data
