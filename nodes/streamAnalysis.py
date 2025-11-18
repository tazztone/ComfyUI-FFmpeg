import os
import subprocess
import json

import os
import subprocess
import json

class AnalyzeStreams:
    """
    A node to analyze the streams of a video file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {
                    "default": "video.mp4",
                    "tooltip": "The video file to analyze."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "analyze_streams"
    CATEGORY = "🔥FFmpeg/Advanced"

    def analyze_streams(self, video):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        command = ['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', video]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return (json.dumps(json.loads(result.stdout), indent=4),)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFprobe error: {e.stderr}")
