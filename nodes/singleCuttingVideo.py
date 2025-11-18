import os
import subprocess
from datetime import datetime
from ..func import video_type,set_file_name,validate_time_format

import os
import subprocess
import folder_paths

class TrimVideo:
    """
    A node to cut a single segment from a video.
    This node extracts a portion of a video based on a specified start and end time.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {
                    "default": "video.mp4",
                    "tooltip": "The video file to trim."
                }),
                "start_time": ("STRING", {
                    "default": "00:00:00",
                    "tooltip": "The start time of the trim in HH:MM:SS format."
                }),
                "end_time": ("STRING", {
                    "default": "00:00:10",
                    "tooltip": "The end time of the trim in HH:MM:SS format."
                }),
                "filename": ("STRING", {
                    "default": "trimmed_video.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "trim_video"
    CATEGORY = "🔥FFmpeg/Editing"

    def trim_video(self, video, start_time, end_time, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            'ffmpeg', '-y', '-i', video,
            '-ss', start_time, '-to', end_time,
            '-c', 'copy', output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)