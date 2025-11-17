import os
import subprocess
from ..func import has_audio,getVideoInfo,set_file_name,video_type
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

import os
import subprocess
import folder_paths

class MergeVideos:
    """
    A node to merge two video files into a single video.
    This node concatenates two video files, handling audio and resolution differences.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video1": ("STRING", {"default": "video1.mp4"}),
                "video2": ("STRING", {"default": "video2.mp4"}),
                "resolution": (["720p", "1080p", "4K"], {"default": "1080p"}),
                "filename": ("STRING", {"default": "merged_video.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge_videos"
    CATEGORY = "🔥FFmpeg/Editing"

    def merge_videos(self, video1, video2, resolution, filename):
        if not os.path.exists(video1):
            raise FileNotFoundError(f"Video file not found: {video1}")
        if not os.path.exists(video2):
            raise FileNotFoundError(f"Video file not found: {video2}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        resolution_map = {
            "720p": "1280:720",
            "1080p": "1920:1080",
            "4K": "3840:2160",
        }

        command = [
            'ffmpeg', '-y', '-i', video1, '-i', video2,
            '-filter_complex',
            f"[0:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v0];"
            f"[1:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];"
            f"[v0][0:a?][v1][1:a?]concat=n=2:v=1:a=1[v][a]",
            '-map', '[v]', '-map', '[a]',
            output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)