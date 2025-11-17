import os
import subprocess
import json

class StreamAnalysis:
    """
    A node to analyze the streams of a video file.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Specifies the input types for the node.
        """
        return {
            "required": {
                "video_path": ("STRING", {
                    "default": "C:/Users/Desktop/video.mp4",
                    "tooltip": "Path to the video file to be analyzed."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("stream_info",)
    FUNCTION = "analyze_streams"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def analyze_streams(self, video_path):
        """
        Analyzes the streams of a video file using ffprobe.
        """
        try:
            video_path = os.path.abspath(video_path).strip()
            if not os.path.isfile(video_path):
                raise ValueError(f"Video file not found: {video_path}")

            command = [
                'ffprobe', '-v', 'error', '-show_streams', '-of', 'json', video_path
            ]

            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, text=True, encoding='utf-8')
            stream_info = json.loads(result.stdout)

            return (json.dumps(stream_info, indent=4),)

        except subprocess.CalledProcessError as e:
            raise ValueError(f"ffprobe error:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        except Exception as e:
            raise ValueError(e)
