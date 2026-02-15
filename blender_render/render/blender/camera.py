import bpy
import math

class Camera:
    def __init__(self, *, first_root, mode, is_mesh = True):
        camera = bpy.data.objects['Camera']

        ## initial position
        camera.location.x = 0
        camera.location.y = 0
        camera.rotation_euler[2] = -math.pi // 2 + 0.43
        # camera.rotation_euler[2] = - math.pi // 2 + 1.8
        
        # camera.rotation_euler[0] = 1.04
        camera.rotation_euler[0] = 1.3

        print(camera.rotation_euler)
        # print(camera.rotation_euler)
        # camera.rotation_euler[0] = c[0] * math.pi / 180
        # camera.rotation_euler[1] = c[1] * math.pi / 180
        # camera.rotation_euler[2] = c[2] * math.pi / 180
        if is_mesh:
            # camera.location.z = 4.6
            camera.location.z = 2.0
            # camera.location.z = 3.74 # for augdata behave
            # camera.location.z = 4.34 #for augdata omomo
            # camera.location.z = 4.1


        else:
            camera.location.z = 5.2

        camera.data.lens = 90
        # wider point of view
        # if mode == "sequence":
        #     if is_mesh:
        #         camera.data.lens = 100
        #     else:
        #         camera.data.lens = 85
        # elif mode == "frame":
        #     if is_mesh:
        #         camera.data.lens = 130
        #     else:
        #         camera.data.lens = 140
        # elif mode == "video":
        #     if is_mesh:
        #         camera.data.lens = 50
        #     else:
        #         camera.data.lens = 140

        # camera.location.x += 0.75

        self.mode = mode
        self.camera = camera

        self.camera.location.x += first_root[0]
        self.camera.location.y += first_root[1]

        self._root = first_root

    def update(self, newroot, ratio=1):
        delta_root = newroot - self._root

        self.camera.location.x += delta_root[0]
        self.camera.location.y += delta_root[1]

        # self.camera.rotation_euler[2] = ratio * 2 * math.pi
        self.camera.rotation_euler[2] = ratio * 2 * math.pi + math.radians(15)

        # self.camera.location.x = 5 * math.sin(self.camera.rotation_euler[2])
        # self.camera.location.y = -5 * math.cos(self.camera.rotation_euler[2])

        # self.camera.location.x = 6.7 * math.sin(self.camera.rotation_euler[2])
        self.camera.location.x = 5.7 * math.sin(self.camera.rotation_euler[2])
        # self.camera.location.x = -8.58 * math.sin(self.camera.rotation_euler[2])
        self.camera.location.y = -5.1 * math.cos(self.camera.rotation_euler[2])
        # self.camera.location.y = -17.48 * math.cos(self.camera.rotation_euler[2])
        self._root = newroot
    def update_2(self, ratio=1):
        self.camera.rotation_euler[2] +=  math.radians(0.3)
        self.camera.location.x += 0.06 * math.sin(self.camera.rotation_euler[2])

