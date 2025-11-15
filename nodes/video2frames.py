import json
import math
import os
import subprocess
import tempfile
import shutil
import glob
import torch
from PIL import Image
import numpy as np
from ..func import video_type

class Video2Frames:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
            },
            "optional": {
                "save_to_disk": ("BOOLEAN", {"default": False}),
                "output_path": ("STRING", {"default": ""}),
                "frames_max_width":("INT", {"default": 0, "min": 0, "max": 1920}),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "STRING")
    RETURN_NAMES = ("images", "frame_count", "output_path")
    FUNCTION = "video2frames"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def video2frames(self, video_path, save_to_disk=False, output_path="", frames_max_width=0):
        temp_dir = None
        try:
            video_path = os.path.abspath(video_path).strip()

            if not video_path.lower().endswith(video_type()):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            if not os.path.isfile(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")

            command = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                'stream=width,height', '-of', 'json', video_path
            ]
            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            data = json.loads(result.stdout.decode('utf-8').strip())
            stream = data['streams'][0]
            width = int(stream.get('width'))
            height = int(stream.get('height'))

            if frames_max_width > 0 and width > frames_max_width:
                out_width = frames_max_width
                out_height = int(height * frames_max_width / width)
            else:
                out_width = width
                out_height = height
            
            temp_dir = tempfile.mkdtemp()

            command = [
                'ffmpeg', '-i', video_path,
                '-vf', f'scale={out_width}:{out_height}',
                os.path.join(temp_dir, '%05d.png')
            ]
            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if result.returncode != 0:
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")

            frame_files = sorted(glob.glob(f'{temp_dir}/*.png'))
            images = []
            for frame_file in frame_files:
                pil_img = Image.open(frame_file)
                img_np = np.array(pil_img).astype(np.float32) / 255.0
                img_tensor = torch.from_numpy(img_np)
                images.append(img_tensor)

            image_batch = torch.stack(images)

            saved_path = ""
            if save_to_disk and output_path:
                if not os.path.isdir(output_path):
                    os.makedirs(output_path)
                for src in frame_files:
                    shutil.copy(src, output_path)
                saved_path = output_path

            return (image_batch, len(images), saved_path)

        finally:
            if temp_dir:
                shutil.rmtree(temp_dir)
