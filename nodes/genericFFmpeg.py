import os
import subprocess
import shlex
import time
import tempfile
import shutil
import torch
import torchaudio
from PIL import Image
import numpy as np

class GenericFFmpeg:
    """
    A generic node to execute custom FFmpeg commands using a placeholder system.
    Now supports IMAGE and AUDIO data types.
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
                "ffmpeg_args": ("STRING", {
                    "default": default_args, "multiline": True,
                    "tooltip": "FFmpeg command arguments. Use placeholders like {media_in_1}, {media_in_2}, {image_in_1}, {audio_in_1}, and {output_file}."
                }),
                "output_path": ("STRING", {
                    "default": "output",
                    "tooltip": "Directory to save the output file."
                }),
                "output_ext": ("STRING", {
                    "default": "mp4",
                    "tooltip": "File extension for the output file (e.g., 'mp4', 'webm')."
                }),
            },
            "optional": {
                "media_in_1": ("STRING", {
                    "tooltip": "Path to the first input media file (for {media_in_1})."
                }),
                "media_in_2": ("STRING", {
                    "tooltip": "Path to the second input media file (for {media_in_2})."
                }),
                "images": ("IMAGE", {
                    "tooltip": "Image frames for the {image_in_1} placeholder (e.g., for creating a video from images)."
                }),
                "audio": ("AUDIO", {
                    "tooltip": "Audio data for the {audio_in_1} placeholder."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_file_path",)
    FUNCTION = "execute_ffmpeg"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def execute_ffmpeg(self, ffmpeg_args, output_path, output_ext, media_in_1=None, media_in_2=None, images=None, audio=None):
        """
        Executes a custom FFmpeg command with placeholders, handling file paths,
        IMAGE tensors, and AUDIO data.
        """
        temp_image_dir = None
        temp_audio_file = None

        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            output_path = os.path.abspath(output_path).strip()

            # Generate a unique output filename
            file_name = f"{time.strftime('%Y%m%d%H%M%S')}.{output_ext.lstrip('.')}"
            output_file_path = os.path.join(output_path, file_name)

            # --- Placeholder Substitution ---
            ffmpeg_args = ffmpeg_args.replace("{output_file}", shlex.quote(output_file_path))

            # Handle IMAGE input
            image_in_1_path = None
            if images is not None:
                temp_image_dir = tempfile.mkdtemp()
                for i, img_tensor in enumerate(images):
                    img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
                    img_pil = Image.fromarray(img_np)
                    img_pil.save(os.path.join(temp_image_dir, f"{i:05d}.png"))
                image_in_1_path = os.path.join(temp_image_dir, "%05d.png")

            # Handle AUDIO input
            audio_in_1_path = None
            if audio is not None:
                waveform = audio['waveform']
                sample_rate = audio['sample_rate']
                while waveform.dim() > 2:
                    waveform = waveform.squeeze(0)

                # Create and save temporary WAV file
                fd, temp_audio_file = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
                torchaudio.save(temp_audio_file, waveform.cpu(), sample_rate)
                audio_in_1_path = temp_audio_file

            # --- Placeholder Substitution ---
            placeholders = {
                "{media_in_1}": media_in_1,
                "{media_in_2}": media_in_2,
                "{image_in_1}": image_in_1_path,
                "{audio_in_1}": audio_in_1_path,
            }

            for placeholder, path in placeholders.items():
                if placeholder in ffmpeg_args:
                    if path is None:
                        raise ValueError(f"Placeholder {placeholder} is used, but no corresponding input is provided.")

                    # For image sequences, the path is a template string, not a real file/dir.
                    # We verify the directory part exists.
                    is_image_sequence = placeholder == "{image_in_1}"
                    check_path = os.path.dirname(path) if is_image_sequence else path

                    if not os.path.exists(check_path):
                         raise ValueError(f"Placeholder {placeholder} is used, but the path '{check_path}' is not valid.")

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
        finally:
            # Clean up temporary files and directories
            if temp_image_dir and os.path.isdir(temp_image_dir):
                shutil.rmtree(temp_image_dir)
            if temp_audio_file and os.path.isfile(temp_audio_file):
                os.unlink(temp_audio_file)
