import bpy
from .materials import plane_mat  # noqa
import math

def setup_renderer(denoising=True, oldrender=True):
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.data.scenes[0].render.engine = "CYCLES"
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "CUDA"
    bpy.context.scene.cycles.device = "GPU"
    bpy.context.preferences.addons["cycles"].preferences.get_devices()
    print(bpy.context.preferences.addons["cycles"].preferences.compute_device_type)

  # ← 关键

    if denoising:
        bpy.context.scene.cycles.use_denoising = True
        bpy.context.scene.cycles.denoising_store_passes = False

    bpy.context.scene.render.tile_x = 256
    bpy.context.scene.render.tile_y = 256
    bpy.context.scene.cycles.samples = 64
    # bpy.context.scene.cycles.denoiser = 'OPTIX' 
    
    bpy.context.scene.view_settings.gamma = 1.5
    bpy.context.scene.view_settings.exposure = -1
    bpy.context.scene.view_settings.view_transform = 'Standard'

    if not oldrender:
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.display_settings.display_device = 'sRGB'
        bpy.context.scene.view_settings.gamma = 1.2
        bpy.context.scene.view_settings.exposure = -0.75
        # bpy.context.scene.view_settings.exposure = 0.0
        # bpy.context.scene.view_settings.gamma = 1.0


def setup_scene_old(res="high", denoising=True, oldrender=True):
    scene = bpy.data.scenes['Scene']
    assert res in ["ultra", "high", "med", "low", "wide"]
    if res == "high":
        scene.render.resolution_x = 512
        scene.render.resolution_y = 512
    elif res == "med":
        scene.render.resolution_x = 1280//2
        scene.render.resolution_y = 1024//2
    elif res == "low":
        scene.render.resolution_x = 1280//4
        scene.render.resolution_y = 1024//4
    elif res == "ultra":
        scene.render.resolution_x = 1280*2
        scene.render.resolution_y = 1024*2
    elif res == "wide":
        scene.render.resolution_x = 1024
        scene.render.resolution_y = 600

    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value[:3] = (1.0, 1.0, 1.0)
    bg.inputs[1].default_value = 1.0
    # bpy.ops.wm.open_mainfile(filepath="./scene3.blend")
    # bpy.context.scene.render.resolution_x = 960  # width
    # bpy.context.scene.render.resolution_y = 540  # height
    # Remove default cube
    if 'Cube' in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()

    # bpy.data.objects['Light'].select_set(True)
    # bpy.ops.object.delete()
    
    bpy.ops.object.light_add(type='SUN', align='WORLD',
                             location=(0, 0, 0), scale=(1, 1, 1))
    # print(bpy.data.objects.keys())
    bpy.data.objects["Sun"].data.energy = 2.0
    bpy.ops.object.light_add(type='POINT', align='WORLD',
                             location=(0, -10, 1))
    # print(bpy.data.objects.keys())
    bpy.data.objects["Point"].data.energy = 500.0
    bpy.ops.object.light_add(type='POINT', align='WORLD',
                             location=(-10, 0, 1))
    bpy.data.objects["Point.001"].data.energy = 200.0
    # print(bpy.data.objects.keys())
    bpy.ops.object.light_add(type='SUN', align='WORLD',
                             location=(-2, 10, 0), scale=(1, 1, 1))
    # # print(bpy.data.objects.keys())
    bpy.data.objects["Sun.001"].data.energy = 1.0
    bpy.ops.object.light_add(type='SUN', align='WORLD',
                             location=(10, 5, 0), scale=(1, 1, 1))
    # # print(bpy.data.objects.keys())
    bpy.data.objects["Sun.002"].data.energy = 1.0
    bpy.ops.object.light_add(type='POINT', align='WORLD',
                             location=(0, 5, 0), scale=(1, 1, 1))
    # # print(bpy.data.objects.keys())
    # bpy.data.objects["Point.002"].data.energy = 3000
    # bpy.ops.object.light_add(type='POINT', align='WORLD',
    #                          location=(6, 0, 6))
    # # print(bpy.data.objects.keys())
    # bpy.data.objects["Point.001"].data.energy = 2000.0
    # bpy.ops.object.light_add(type='POINT', align='WORLD',
    #                          location=(6, 6, 6))
    # # # print(bpy.data.objects.keys())
    # bpy.data.objects["Point.002"].data.energy = 5000.0
    # bpy.ops.object.light_add(type='SUN', align='WORLD',
    #                          location=(6, 0, 0), scale=(1, 1, 1))
    # # # print(bpy.data.objects.keys())
    # bpy.data.objects["Sun.004"].data.energy = 3.0
    # bpy.ops.object.light_add(type='SUN', align='WORLD',
    #                          location=(0, 10, 0), scale=(1, 1, 1))
    # # # print(bpy.data.objects.keys())
    # bpy.data.objects["Sun.003"].data.energy = 3.0
    # bpy.ops.object.light_add(type='SUN', align='WORLD',
    #                          location=(10, 0, 0), scale=(1, 1, 1), rotation=(math.pi / 2, 0, math.pi - 0.2))
    # # print(bpy.data.objects.keys())
    # bpy.data.objects["Sun.002"].data.energy = 3.0
    # bpy.ops.object.light_add(type='SUN', align='WORLD',
    #                          location=(10, 0, 0), scale=(1, 1, 1), rotation=(math.pi / 2, 0, math.pi + 0.2))
    # # print(bpy.data.objects.keys())
    # bpy.data.objects["Sun.003"].data.energy = 3.0
    # bpy.ops.object.light_add(type='SUN', align='WORLD',
    #                          location=(10, 10, 5), scale=(1, 1, 1), rotation=(0.8, 0, -2))
    # # print(bpy.data.objects.keys())
    # bpy.data.objects["Sun.002"].data.energy = 3.0
    # print(bpy.data.objects["Light"].matrix_world[1, 3])
    # print(bpy.data.objects["Light"].matrix_world, bpy.data.objects["Light"].matrix_world.to_translation(), bpy.data.objects["Light"].matrix_world.to_euler(),)
    # rotate camera
    # bpy.data.objects['Light'].select_set(True)
    # bpy.ops.object.delete()
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.transform.resize(value=(10, 10, 10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                             orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1,
                             use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.scenes["Scene"].render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    setup_renderer(denoising=denoising, oldrender=oldrender)
    return scene


# Setup scene
def setup_scene(res="high", denoising=True, oldrender=True):
    scene = bpy.data.scenes['Scene']
    assert res in ["ultra", "high", "med", "low", "wide"]
    bpy.context.scene.render.resolution_x = 512  # width
    bpy.context.scene.render.resolution_y = 512  # height
    scene.render.resolution_percentage = 100 

    # scene.render.pixel_aspect_x = 1
    # scene.render.pixel_aspect_y = 1
    # scene.render.image_settings.dpi = 300

    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value[:3] = (1.0, 1.0, 1.0)
    bg.inputs[1].default_value = 1.0

    # Remove default cube
    if 'Cube' in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()

    bpy.ops.object.light_add(type='SUN', align='WORLD',
                             location=(0, 0, 0), scale=(1, 1, 1))
    bpy.data.objects["Sun"].data.energy = 1.0


    # # Sun: rotation matters (location doesn't)
    # sun = bpy.data.objects.get("Sun")
    # if sun:
    #     sun.rotation_euler = (math.radians(55), 0.0, math.radians(30))  # point downward
    #     sun.data.angle = math.radians(1.0)   # crisper light
    #     sun.data.energy = 3.0                # more light

    # rotate camera
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.transform.resize(value=(10, 10, 10), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                             orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False,
                             proportional_edit_falloff='SMOOTH', proportional_size=1,
                             use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.object.select_all(action='DESELECT')


    print("Scene setup complete with a white floor and light source.")
    setup_renderer(denoising=denoising, oldrender=oldrender)
    return scene
