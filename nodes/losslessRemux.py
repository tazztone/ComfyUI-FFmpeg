import os
import subprocess
from ..func import set_file_name, video_type, audio_type

class LosslessRemux:
    """
    A node to change the container of a video or audio file without re-encoding.
    Accepts a standard media path or a VHS_FILENAMES tuple.
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
                "output_path": ("STRING", {
                    "default": "output",
                    "tooltip": "Directory to save the remuxed media file."
                }),
                "output_format": (["mp4", "mkv", "mov", "webm"], {
                    "tooltip": "The container format for the output file."
                }),
            },
            "optional": {
                "media_path": ("STRING", {
                    "default": "",
                    "tooltip": "Path to the media file to be remuxed. Used if 'media_in' is not provided."
                }),
                "media_in": ("VHS_FILENAMES", {
                    "tooltip": "VHS_FILENAMES tuple from an upstream node. Takes priority over 'media_path'."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("media_complete_path",)
    FUNCTION = "remux_media"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def remux_media(self, output_path, output_format, media_path="", media_in=None):
        """
        Changes the container of a media file without re-encoding.
        Prioritizes media_in (VHS_FILENAMES) over media_path.
        """
        try:
            # --- Determine input source ---
            source_path = ""
            if media_in is not None:
                # Check if media_in is a valid VHS_FILENAMES tuple (bool, [paths])
                if isinstance(media_in, tuple) and len(media_in) == 2 and isinstance(media_in[1], list) and media_in[1]:
                    # Get the last file path from the list
                    source_path = media_in[1][-1]
                    print(f"📥 Received media from VHS_FILENAMES: {source_path}")
                else:
                    raise ValueError("media_in (VHS_FILENAMES) is not in the expected format (True, [\"path/to/file\"]).")
            elif media_path:
                source_path = media_path
                print(f"📁 Using media_path: {source_path}")
            else:
                raise ValueError("No media input provided. Connect either `media_path` or `media_in`.")

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            source_path = os.path.abspath(source_path).strip()
            output_path = os.path.abspath(output_path).strip()

            if not source_path.lower().endswith(video_type() + audio_type()):
                raise ValueError("Input path is not a valid media file.")
            if not os.path.isfile(source_path):
                raise ValueError(f"Input file does not exist: {source_path}")

            file_name = os.path.splitext(os.path.basename(source_path))[0]
            output_file_path = os.path.join(output_path, f"{file_name}.{output_format}")

            command = ['ffmpeg', '-y', '-i', source_path, '-c', 'copy', output_file_path]

            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, text=True)

            return (output_file_path,)
        except subprocess.CalledProcessError as e:
            raise ValueError(f"FFmpeg error: {e.stderr}")
        except Exception as e:
            raise ValueError(e)
