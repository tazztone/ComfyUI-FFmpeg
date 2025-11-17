import os
import subprocess
import shlex
import time

import os
import subprocess
import shlex
import folder_paths

class ApplyStreamMap:
    """
    A node to apply stream mapping to a video.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "stream_map": ("STRING", {"default": "-map 0:v -map 0:a:0?", "multiline": True}),
                "filename": ("STRING", {"default": "mapped_video.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "apply_stream_map"
    CATEGORY = "🔥FFmpeg/Advanced"

    def apply_stream_map(self, video, stream_map, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ['ffmpeg', '-y', '-i', video, *shlex.split(stream_map), '-c', 'copy', output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return (output_path,)
