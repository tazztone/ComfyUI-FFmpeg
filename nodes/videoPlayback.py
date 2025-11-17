import os
import subprocess
from ..func import set_file_name,video_type

import os
import subprocess
import folder_paths

class ReverseVideo:
    """
    A node to reverse a video.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "reverse_audio": ("BOOLEAN", {"default": True}),
                "filename": ("STRING", {"default": "reversed_video.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "reverse_video"
    CATEGORY = "🔥FFmpeg/IO"

    def reverse_video(self, video, reverse_audio, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ['ffmpeg', '-y', '-i', video, '-vf', 'reverse']
        if reverse_audio:
            command.extend(['-af', 'areverse'])
            
        command.append(output_path)

        subprocess.run(command, check=True)
        return (output_path,)