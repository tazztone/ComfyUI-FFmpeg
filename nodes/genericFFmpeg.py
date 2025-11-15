import os
import subprocess
import shlex
import time
from ..func import video_type, audio_type

class GenericFFmpeg:
    """
    A generic node to execute custom FFmpeg commands using a placeholder system.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Specifies the input types for the node.
        """
        default_args = "-i {media_in_1} -c:v libx264 -preset slow -crf 22 -c:a copy {output_file}"
        return {
            "required": {
                "ffmpeg_args": ("STRING", {"default": default_args, "multiline": True}),
                "output_path": ("STRING", {"default": "output"}),
                "output_ext": ("STRING", {"default": "mp4"}),
            },
            "optional": {
                "media_in_1": ("STRING", {}),
                "media_in_2": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_file_path",)
    FUNCTION = "execute_ffmpeg"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def execute_ffmpeg(self, ffmpeg_args, output_path, output_ext, media_in_1=None, media_in_2=None):
        """
        Executes a custom FFmpeg command with placeholders.
        """
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            output_path = os.path.abspath(output_path).strip()

            # Generate a unique output filename
            file_name = f"{time.strftime('%Y%m%d%H%M%S')}.{output_ext.lstrip('.')}"
            output_file_path = os.path.join(output_path, file_name)

            # --- Placeholder Substitution ---

            # Handle output file placeholder
            ffmpeg_args = ffmpeg_args.replace("{output_file}", shlex.quote(output_file_path))

            # Handle input media placeholders
            placeholders = {
                "{media_in_1}": media_in_1,
                "{media_in_2}": media_in_2,
            }

            for placeholder, path in placeholders.items():
                if placeholder in ffmpeg_args:
                    if path is None or not os.path.isfile(path):
                        raise ValueError(f"Placeholder {placeholder} is used in arguments, but the corresponding input is not a valid file.")
                    abs_path = os.path.abspath(path).strip()
                    ffmpeg_args = ffmpeg_args.replace(placeholder, shlex.quote(abs_path))

            # Final command construction
            command = ['ffmpeg', '-y'] + shlex.split(ffmpeg_args)

            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, text=True, encoding='utf-8')

            if not os.path.exists(output_file_path):
                 raise FileNotFoundError(f"FFmpeg command executed but the output file was not found: {output_file_path}\\nFFmpeg stderr: {result.stderr}")

            return (output_file_path,)

        except subprocess.CalledProcessError as e:
            raise ValueError(f"FFmpeg error:\\nSTDOUT: {e.stdout}\\nSTDERR: {e.stderr}")
        except Exception as e:
            raise ValueError(e)
