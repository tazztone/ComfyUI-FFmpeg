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
    """
    A node to extract frames from a video.
    This node takes a video file and extracts its frames as individual images.
    It also extracts the audio track and provides video metadata.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "sample.mp4"}),
                "max_width": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "save_frames": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "output_dir": ("STRING", {"default": "frames"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT")
    FUNCTION = "video_to_frames"
    CATEGORY = "🔥FFmpeg/Conversion"

    def video_to_frames(self, video, max_width, save_frames, output_dir="frames"):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        temp_dir = tempfile.mkdtemp()

        probe_cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'json', video
        ]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        video_info = json.loads(probe_result.stdout)
        width = video_info['streams'][0]['width']
        height = video_info['streams'][0]['height']

        scale_filter = ""
        if max_width > 0 and width > max_width:
            scale_filter = f"scale={max_width}:-1"

        ffmpeg_cmd = ['ffmpeg', '-i', video]
        if scale_filter:
            ffmpeg_cmd.extend(['-vf', scale_filter])
        ffmpeg_cmd.append(os.path.join(temp_dir, '%05d.png'))

        subprocess.run(ffmpeg_cmd, check=True)

        frame_files = sorted(glob.glob(os.path.join(temp_dir, '*.png')))
        images = [Image.open(f) for f in frame_files]

        if save_frames:
            os.makedirs(output_dir, exist_ok=True)
            for i, frame in enumerate(images):
                frame.save(os.path.join(output_dir, f'frame_{i:05d}.png'))

        tensors = [torch.from_numpy(np.array(img).astype(np.float32) / 255.0) for img in images]
        batch_tensor = torch.stack(tensors)

        shutil.rmtree(temp_dir)

        return (batch_tensor, len(images))
