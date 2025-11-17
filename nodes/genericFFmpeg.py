import os
import subprocess
import shlex
import time
import tempfile
import shutil
import torch
import torchaudio
from PIL import Image
import numpy as np

import os
import subprocess
import shlex
import folder_paths

class GenericFFmpeg:
    """
    A generic node to execute custom FFmpeg commands.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "ffmpeg_command": ("STRING", {"default": "-vf hflip", "multiline": True}),
                "filename": ("STRING", {"default": "generic_output.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute_ffmpeg"
    CATEGORY = "🔥FFmpeg/Advanced"

    def execute_ffmpeg(self, video, ffmpeg_command, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ['ffmpeg', '-y', '-i', video, *shlex.split(ffmpeg_command), output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return (output_path,)
