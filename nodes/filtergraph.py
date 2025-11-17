import os
import subprocess
import shlex
import time

import os
import subprocess
import shlex
import folder_paths

class ApplyFiltergraph:
    """
    A node to apply a raw FFmpeg filtergraph to a video.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "filtergraph": ("STRING", {"default": "vf hflip", "multiline": True}),
                "filename": ("STRING", {"default": "filtered_video.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "apply_filtergraph"
    CATEGORY = "🔥FFmpeg/Advanced"

    def apply_filtergraph(self, video, filtergraph, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ['ffmpeg', '-y', '-i', video, *shlex.split(filtergraph), output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return (output_path,)
