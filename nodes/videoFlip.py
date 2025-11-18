import os
import subprocess
from ..func import set_file_name,video_type

import os
import subprocess
import folder_paths

class VideoFlip:
    """
    A node to flip a video horizontally, vertically, or both.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {
                    "default": "sample.mp4",
                    "tooltip": "The video file to flip."
                }),
                "flip_type": (["horizontal", "vertical", "both"], {
                    "tooltip": "The type of flip to apply."
                }),
                "filename": ("STRING", {
                    "default": "flipped_video.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "flip_video"
    CATEGORY = "🔥FFmpeg/Editing"

    def flip_video(self, video, flip_type, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        flip_map = {
            "horizontal": "hflip",
            "vertical": "vflip",
            "both": "hflip,vflip",
        }

        command = [
            'ffmpeg', '-y', '-i', video,
            '-vf', flip_map[flip_type],
            output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)