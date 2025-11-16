import os
import subprocess
import shlex
import time

class Subtitle:
    """
    A node to handle subtitles.
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
                "video": ("STRING", {"default": "video.mp4"}),
                "subtitle_file": ("STRING", {"default": "subtitle.srt"}),
                "action": (["burn", "add", "extract"],),
                "output_path": ("STRING", {"default": "output"}),
                "output_ext": ("STRING", {"default": "mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_file_path",)
    FUNCTION = "execute_subtitle"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def execute_subtitle(self, video, subtitle_file, action, output_path, output_ext):
        """
        Executes the FFmpeg command for the specified subtitle action.
        """
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")
        if action != 'extract' and not os.path.exists(subtitle_file):
            raise FileNotFoundError(f"Subtitle file not found: {subtitle_file}")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_path = os.path.abspath(output_path).strip()

        file_name = f"{time.strftime('%Y%m%d%H%M%S')}"
        if action == 'extract':
            output_file_path = os.path.join(output_path, f"{file_name}.srt")
        else:
            output_file_path = os.path.join(output_path, f"{file_name}.{output_ext.lstrip('.')}")

        try:
            if action == 'burn':
                command = [
                    'ffmpeg', '-y',
                    '-i', shlex.quote(video),
                    '-vf', f"subtitles={shlex.quote(subtitle_file)}",
                    shlex.quote(output_file_path)
                ]
            elif action == 'add':
                command = [
                    'ffmpeg', '-y',
                    '-i', shlex.quote(video),
                    '-i', shlex.quote(subtitle_file),
                    '-c', 'copy',
                    '-c:s', 'mov_text',
                    shlex.quote(output_file_path)
                ]
            elif action == 'extract':
                command = [
                    'ffmpeg', '-y',
                    '-i', shlex.quote(video),
                    '-map', '0:s:0',
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
