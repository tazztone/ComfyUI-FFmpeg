import os
import subprocess
from ..func import set_file_name, video_type, audio_type

class LosslessRemux:
    """
    A node to change the container of a video or audio file without re-encoding.
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
                "media_path": ("STRING", {}),
                "output_path": ("STRING", {"default": "output"}),
                "output_format": (["mp4", "mkv", "mov", "webm"],),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("media_complete_path",)
    FUNCTION = "remux_media"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def remux_media(self, media_path, output_path, output_format):
        """
        Changes the container of a media file without re-encoding.
        """
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            media_path = os.path.abspath(media_path).strip()
            output_path = os.path.abspath(output_path).strip()

            if not media_path.lower().endswith(video_type() + audio_type()):
                raise ValueError("media_path is not a valid media file.")
            if not os.path.isfile(media_path):
                raise ValueError("media_path does not exist.")

            file_name = os.path.splitext(os.path.basename(media_path))[0]
            output_file_path = os.path.join(output_path, f"{file_name}.{output_format}")

            command = ['ffmpeg', '-y', '-i', media_path, '-c', 'copy', output_file_path]

            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, text=True)

            return (output_file_path,)
        except subprocess.CalledProcessError as e:
            raise ValueError(f"FFmpeg error: {e.stderr}")
        except Exception as e:
            raise ValueError(e)
