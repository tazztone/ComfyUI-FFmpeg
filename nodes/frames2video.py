import os
import subprocess
import tempfile
import shutil
import torch
import torchaudio
from PIL import Image
import numpy as np
try:
    from ..func import get_output_path
except ImportError:
    from func import get_output_path

class Frames2Video:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {
                    "tooltip": "The images to convert to video."
                }),
                "fps": ("INT", {
                    "default": 24,
                    "min": 1,
                    "tooltip": "The frame rate of the output video."
                }),
                "codec": (["h264_cpu", "h265_cpu", "h264_nvidia", "h265_nvidia"], {
                    "tooltip": "The video codec to use for encoding."
                }),
                "crf": ("INT", {
                    "default": 23,
                    "min": 0,
                    "max": 51,
                    "tooltip": "The Constant Rate Factor (CRF) for the video encoding. Lower values mean better quality and larger file size."
                }),
                "preset": (["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], {
                    "tooltip": "The encoding preset, which affects the encoding speed and compression efficiency."
                }),
                "filename": ("STRING", {
                    "default": "output.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
            "optional": {
                "audio": ("AUDIO", {
                    "tooltip": "An optional audio track to add to the video."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "frames_to_video"
    CATEGORY = "🔥FFmpeg/Conversion"

    def frames_to_video(self, images, fps, codec, crf, preset, filename, audio=None):
        temp_dir = tempfile.mkdtemp()
        output_path = get_output_path(filename)

        try:
            for i, img_tensor in enumerate(images):
                img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
                Image.fromarray(img_np).save(os.path.join(temp_dir, f"{i:05d}.png"))

            cmd = ['ffmpeg', '-y', '-framerate', str(fps), '-i', os.path.join(temp_dir, '%05d.png')]

            audio_file = None
            if audio:
                audio_file = tempfile.mktemp(suffix=".wav")
                torchaudio.save(audio_file, audio['waveform'].cpu(), audio['sample_rate'])
                cmd.extend(['-i', audio_file])

            video_codec, crf_option = self._get_codec_options(codec, crf)
            cmd.extend(['-c:v', video_codec, crf_option, str(crf), '-preset', preset, '-pix_fmt', 'yuv420p'])

            if audio:
                cmd.extend(['-c:a', 'aac', '-shortest'])

            cmd.append(output_path)
            subprocess.run(cmd, check=True)

            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

        return (output_path,)

    def _get_codec_options(self, codec, crf):
        if codec == "h264_cpu":
            return "libx264", "-crf"
        elif codec == "h265_cpu":
            return "libx265", "-crf"
        elif codec == "h264_nvidia":
            return "h264_nvenc", "-cq"
        elif codec == "h265_nvidia":
            return "hevc_nvenc", "-cq"
        else:
            raise ValueError(f"Unsupported codec: {codec}")
