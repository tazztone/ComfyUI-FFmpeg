import os
import subprocess
import shlex
import time

class Filtergraph:
    """
    A node to apply a raw FFmpeg filtergraph to a video.
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
                "video": ("STRING", {
                    "default": "video.mp4",
                    "tooltip": "Path to the input video file."
                }),
                "filtergraph": ("STRING", {
                    "default": "crop=iw/2:ih:0:0[left];[left]vflip[out]", "multiline": True,
                    "tooltip": "The FFmpeg filtergraph to apply. E.g., 'crop=iw/2:ih:0:0[left];[left]vflip[out]'. See FFmpeg documentation for more details."
                }),
                "output_path": ("STRING", {
                    "default": "output",
                    "tooltip": "The directory where the output video file will be saved."
                }),
                "output_ext": ("STRING", {
                    "default": "mp4",
                    "tooltip": "The file extension for the output video file (e.g., 'mp4', 'webm')."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_file_path",)
    FUNCTION = "execute_filtergraph"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def execute_filtergraph(self, video, filtergraph, output_path, output_ext):
        """
        Executes the FFmpeg command with the provided filtergraph.
        """
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_path = os.path.abspath(output_path).strip()

        file_name = f"{time.strftime('%Y%m%d%H%M%S')}.{output_ext.lstrip('.')}"
        output_file_path = os.path.join(output_path, file_name)

        try:
            command = [
                'ffmpeg', '-y',
                '-i', shlex.quote(video),
                '-filter_complex', filtergraph,
                shlex.quote(output_file_path)
            ]

            # Use subprocess.run and capture output
            result = subprocess.run(
                ' '.join(command),  # shell=True requires a string
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if not os.path.exists(output_file_path):
                 raise FileNotFoundError(f"FFmpeg command executed but the output file was not found: {output_file_path}\\nFFmpeg stderr: {result.stderr}")

            return (output_file_path,)

        except subprocess.CalledProcessError as e:
            # Construct a more informative error message
            error_message = (
                f"FFmpeg command failed with exit code {e.returncode}.\\n"
                f"Command: {' '.join(command)}\\n"
                f"Stdout:\\n{e.stdout}\\n"
                f"Stderr:\\n{e.stderr}"
            )
            raise ValueError(error_message)
        except Exception as e:
            raise ValueError(e)
