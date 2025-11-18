import os
import subprocess
from ..func import has_audio,getVideoInfo,set_file_name,video_type
import torch
import math
import time

device = "cuda" if torch.cuda.is_available() else "cpu"

import os
import subprocess
import folder_paths

class StitchVideos:
    """
    A node to stitch two videos together, either horizontally or vertically.
    This node combines two video files side-by-side or one on top of the other.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video1": ("STRING", {
                    "default": "video1.mp4",
                    "tooltip": "The first video file to stitch."
                }),
                "video2": ("STRING", {
                    "default": "video2.mp4",
                    "tooltip": "The second video file to stitch."
                }),
                "layout": (["horizontal", "vertical"], {
                    "default": "horizontal",
                    "tooltip": "The layout for stitching the videos (side-by-side or top-to-bottom)."
                }),
                "audio_source": (["video1", "video2", "none"], {
                    "default": "video1",
                    "tooltip": "The audio source for the output video."
                }),
                "filename": ("STRING", {
                    "default": "stitched_video.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "stitch_videos"
    CATEGORY = "🔥FFmpeg/Editing"

    def stitch_videos(self, video1, video2, layout, audio_source, filename):
        if not os.path.exists(video1):
            raise FileNotFoundError(f"Video file not found: {video1}")
        if not os.path.exists(video2):
            raise FileNotFoundError(f"Video file not found: {video2}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        filter_complex = f"[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[v]" if layout == 'horizontal' \
                         else f"[0:v]pad=iw:ih*2[int];[int][1:v]overlay=0:H/2[v]"

        command = ['ffmpeg', '-y', '-i', video1, '-i', video2, '-filter_complex', filter_complex]

        if audio_source != "none":
            audio_map = {'video1': '0:a', 'video2': '1:a'}
            command.extend(['-map', '[v]', '-map', audio_map[audio_source]])
        else:
            command.extend(['-map', '[v]', '-an'])

        command.append(output_path)

        subprocess.run(command, check=True)
        return (output_path,)