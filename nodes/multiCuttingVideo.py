import os
import subprocess
from ..func import video_type

import os
import subprocess
import folder_paths

class SplitVideo:
    """
    A node to cut a video into multiple segments of a specified duration.
    This node uses FFmpeg to split a video into smaller clips based on a given segment time.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {
                    "default": "video.mp4",
                    "tooltip": "The video file to split."
                }),
                "segment_duration": ("INT", {
                    "default": 10,
                    "min": 1,
                    "tooltip": "The duration of each video segment in seconds."
                }),
                "output_prefix": ("STRING", {
                    "default": "segment_",
                    "tooltip": "The prefix for the output video files."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "split_video"
    CATEGORY = "🔥FFmpeg/Editing"

    def split_video(self, video, segment_duration, output_prefix):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_dir = folder_paths.get_output_directory()
        output_pattern = os.path.join(output_dir, f"{output_prefix}%03d.mp4")

        command = [
            'ffmpeg', '-y', '-i', video,
            '-c', 'copy', '-map', '0', '-segment_time', str(segment_duration),
            '-f', 'segment', output_pattern
        ]

        subprocess.run(command, check=True)
        return (output_dir,)