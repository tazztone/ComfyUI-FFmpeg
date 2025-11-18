import os
import subprocess
from ..func import set_file_name,video_type,getVideoInfo,get_xfade_transitions,has_audio
import torch
    
device = "cuda" if torch.cuda.is_available() else "cpu"


import os
import subprocess
import folder_paths
from ..func import get_xfade_transitions

class VideoTransition:
    """
    A node to create a transition between two videos.
    This node uses FFmpeg's xfade filter to create a transition effect between two video clips.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video1": ("STRING", {
                    "default": "video1.mp4",
                    "tooltip": "The first video file for the transition."
                }),
                "video2": ("STRING", {
                    "default": "video2.mp4",
                    "tooltip": "The second video file for the transition."
                }),
                "transition": (get_xfade_transitions(), {
                    "default": "fade",
                    "tooltip": "The transition effect to use."
                }),
                "duration": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "tooltip": "The duration of the transition in seconds."
                }),
                "offset": ("FLOAT", {
                    "default": 2.0,
                    "min": 0.0,
                    "tooltip": "The time offset in the first video where the transition should start."
                }),
                "filename": ("STRING", {
                    "default": "transition_video.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "create_transition"
    CATEGORY = "🔥FFmpeg/Editing"

    def create_transition(self, video1, video2, transition, duration, offset, filename):
        if not os.path.exists(video1):
            raise FileNotFoundError(f"Video file not found: {video1}")
        if not os.path.exists(video2):
            raise FileNotFoundError(f"Video file not found: {video2}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            'ffmpeg', '-y', '-i', video1, '-i', video2,
            '-filter_complex',
            f"[0:v][1:v]xfade=transition={transition}:duration={duration}:offset={offset}[v];"
            f"[0:a][1:a]acrossfade=d={duration}[a]",
            '-map', '[v]', '-map', '[a]',
            output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)