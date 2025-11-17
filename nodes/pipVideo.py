import os
import subprocess
from ..func import has_audio,getVideoInfo,set_file_name,video_type
import torch
import math

device = "cuda" if torch.cuda.is_available() else "cpu"

import os
import subprocess
import folder_paths

class PictureInPicture:
    """
    A node to create a picture-in-picture (PiP) video.
    This node overlays one video on top of another, with options for positioning, scaling, and audio selection.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "background_video": ("STRING", {"default": "background.mp4"}),
                "foreground_video": ("STRING", {"default": "foreground.mp4"}),
                "position": (["top_left", "top_right", "bottom_left", "bottom_right", "center"],),
                "scale": ("FLOAT", {"default": 0.5, "min": 0.1, "max": 1.0}),
                "audio_source": (["background", "foreground", "none"], {"default": "background"}),
                "filename": ("STRING", {"default": "pip_video.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "create_pip_video"
    CATEGORY = "🔥FFmpeg/Editing"

    def create_pip_video(self, background_video, foreground_video, position, scale, audio_source, filename):
        if not os.path.exists(background_video):
            raise FileNotFoundError(f"Background video not found: {background_video}")
        if not os.path.exists(foreground_video):
            raise FileNotFoundError(f"Foreground video not found: {foreground_video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        position_map = {
            "top_left": "10:10",
            "top_right": "W-w-10:10",
            "bottom_left": "10:H-h-10",
            "bottom_right": "W-w-10:H-h-10",
            "center": "(W-w)/2:(H-h)/2",
        }

        filter_complex = f"[1:v]scale=iw*{scale}:-1[fg];[0:v][fg]overlay={position_map[position]}"

        command = ['ffmpeg', '-y', '-i', background_video, '-i', foreground_video, '-filter_complex', filter_complex]

        if audio_source != "none":
            audio_map = {"background": "0:a", "foreground": "1:a"}
            command.extend(['-map', '0:v', '-map', audio_map[audio_source], '-shortest'])

        command.append(output_path)

        subprocess.run(command, check=True)
        return (output_path,)