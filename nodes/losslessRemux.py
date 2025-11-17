import os
import subprocess
from ..func import set_file_name, video_type, audio_type

import os
import subprocess
import folder_paths

class RemuxVideo:
    """
    A node to change the container of a video file without re-encoding.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "container": (["mp4", "mkv", "mov", "webm"],),
                "filename": ("STRING", {"default": "remuxed_video.mkv"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "remux_video"
    CATEGORY = "🔥FFmpeg/Advanced"

    def remux_video(self, video, container, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ['ffmpeg', '-y', '-i', video, '-c', 'copy', '-f', container, output_path]

        subprocess.run(command, check=True)
        return (output_path,)
