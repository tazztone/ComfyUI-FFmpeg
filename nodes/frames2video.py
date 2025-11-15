import os
import subprocess
import tempfile
import shutil
import torch
import torchaudio
from PIL import Image
import numpy as np
from ..func import get_image_size, generate_template_string

class Frames2Video:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """Specifies the input types for the node.

        Returns:
            dict: A dictionary containing the input types.
        """
        return {
            "required": {
                "fps": ("FLOAT", {"default": 30, "min": 1, "max": 120, "step": 1, "display": "number"}),
                "video_name": ("STRING", {"default": "new_video"}),
                "output_path": ("STRING", {"default": "C:/Users/Desktop/output"}),
                "device": (["CPU", "GPU"], {"default": "CPU",}),
            },
            "optional": {
                "images": ("IMAGE", {}),
                "audio": ("AUDIO", {}),
                "frame_path": ("STRING", {"default": ""}),
                "audio_path": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("frame_path", "output_path",)
    FUNCTION = "frames2video"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def frames2video(self, fps, video_name, output_path, device, images=None, audio=None, frame_path="", audio_path=""):
        temp_frame_dir = None
        temp_audio_file = None

        try:
            output_path = os.path.abspath(output_path).strip()
            if not os.path.isdir(output_path):
                raise ValueError(f"output_path: {output_path} is not a directory")

            output_path = os.path.join(output_path, f"{video_name}.mp4")

            if images is not None:
                temp_frame_dir = tempfile.mkdtemp()
                for i, img in enumerate(images):
                    img_np = (img.cpu().numpy() * 255).astype(np.uint8)
                    pil_img = Image.fromarray(img_np)
                    pil_img.save(os.path.join(temp_frame_dir, f"{i:05d}.png"))
                frame_source = temp_frame_dir
                width, height = get_image_size(os.path.join(temp_frame_dir, "00000.png"))
                img_template_string = "%05d.png"
            else:
                if not frame_path or not os.path.isdir(frame_path):
                    raise ValueError(f"frame_path: {frame_path} is not a valid directory")
                frame_source = os.path.abspath(frame_path).strip()
                valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
                image_files = [f for f in os.listdir(frame_source) if f.endswith(valid_extensions)]
                image_files.sort()
                if not image_files:
                    raise FileNotFoundError(f"No image files found in directory: {frame_source}")
                width, height = get_image_size(os.path.join(frame_source, image_files[0]))
                img_template_string = generate_template_string(image_files[0])

            if audio is not None:
                temp_audio_file = tempfile.mktemp(suffix='.wav')
                waveform = audio['waveform']
                sample_rate = audio['sample_rate']
                while waveform.dim() > 2:
                    waveform = waveform.squeeze(0)
                torchaudio.save(temp_audio_file, waveform.cpu(), sample_rate)
                audio_source = temp_audio_file
            elif audio_path and os.path.isfile(audio_path):
                audio_source = os.path.abspath(audio_path).strip()
            else:
                audio_source = None
            
            common_args = ['-framerate', str(fps), '-i', f'{frame_source}/{img_template_string}']
            if audio_source:
                common_args.extend(['-i', audio_source])
            
            common_args.extend(['-vf', f'scale={width}:{height}', '-pix_fmt', 'yuv420p', '-shortest', '-y', str(output_path)])

            if device == "CPU":
                cmd = ['ffmpeg'] + common_args + ['-c:v', 'libx264', '-crf', '28']
            else:
                cmd = ['ffmpeg'] + common_args + ['-c:v', 'h264_nvenc', '-preset', 'fast', '-cq', '22']

            result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if result.returncode != 0:
                raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                print(result.stdout)

            return (frame_source if images is None else "in-memory images", output_path)

        finally:
            if temp_frame_dir:
                shutil.rmtree(temp_frame_dir)
            if temp_audio_file:
                os.unlink(temp_audio_file)

        return ("", "")
