import os
import sys
import shutil
from PIL import Image

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir)
from render.video import Video
import re

_num = re.compile(r'(\d+)')

def numeric_key(s: str):
    # splits into strings and integers so "frame_2.png" < "frame_10.png"
    return [int(t) if t.isdigit() else t for t in _num.split(s)]

def remove_alpha(input_dir, output_dir, bg_color=(200, 200, 200)):
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".png")]
    for i, fname in enumerate(sorted(files, key=numeric_key)):
        im = Image.open(os.path.join(input_dir, fname))
        if im.mode == 'RGBA':
            bg = Image.new("RGB", im.size, bg_color)
            bg.paste(im, mask=im.split()[3])
            # re-emit with our own padded name to lock ordering
            outname = f"frame_{i:06d}.png"
            bg.save(os.path.join(output_dir, outname))
        else:
            outname = f"frame_{i:06d}.png"
            im.convert("RGB").save(os.path.join(output_dir, outname))

# Set paths

def gen_video(frames_folder, name="video"):
    
    # frames_folder = "/media/volume/Sirui-2/blender/blender_render/save/behave_correct/Date01_Sub01_boxsmall_hand_810_2"
    frames_rgb_folder = f'{frames_folder}/frames_rgb'
    vid_path = f'{frames_folder}/{name}.mp4'

    # Process and save video
    remove_alpha(frames_folder, frames_rgb_folder)
    video = Video(frames_rgb_folder, fps=30)
    video.save(out_path=vid_path)

    # Remove the RGB folder after saving
    shutil.rmtree(frames_rgb_folder)

# gen_video("/media/volume/Sirui-2/arctic/render_out/s05_laptop_use_01_1/images/rgb", name="video")