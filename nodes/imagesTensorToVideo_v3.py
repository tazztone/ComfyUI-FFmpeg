import os
import subprocess
import tempfile
import shutil
import torchaudio
from PIL import Image
import numpy as np
import folder_paths
from comfy_api.latest import io

class ImagesTensorToVideoV3(io.ComfyNode):
    """
    A V3 node to convert a batch of images (tensors) directly to a video file.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ImagesTensorToVideoV3",
            display_name="🔥Images (Tensor) to Video (V3)",
            category="🔥FFmpeg/Conversion",
            inputs=[
                io.Image.Input("images", tooltip="Input images (tensor batch)."),
                io.Int.Input("fps", default=24, min=1, tooltip="Frame rate."),
                io.Combo.Input(
                    "codec",
                    ["h264_cpu", "h265_cpu", "h264_nvidia", "h265_nvidia"],
                    tooltip="Video codec.",
                ),
                io.Int.Input(
                    "crf_or_cq",
                    default=23,
                    min=0,
                    max=51,
                    tooltip="Quality (CRF for CPU, CQ for NVIDIA). Lower is better.",
                ),
                io.Combo.Input(
                    "preset",
                    [
                        "ultrafast",
                        "superfast",
                        "veryfast",
                        "faster",
                        "fast",
                        "medium",
                        "slow",
                        "slower",
                        "veryslow",
                    ],
                    default="medium",
                    tooltip="Encoding preset.",
                ),
                io.String.Input(
                    "filename", default="tensor_video.mp4", tooltip="Output filename."
                ),
                io.Audio.Input("audio", tooltip="Optional audio track.", optional=True),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output video file."),
            ],
        )

    @staticmethod
    def _get_codec_options(codec):
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

    @classmethod
    def execute(
        cls, images, fps, codec, crf_or_cq, preset, filename, audio=None
    ) -> io.NodeOutput:
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        try:
            # images is [Batch, Height, Width, Channels]
            for i, img_tensor in enumerate(images):
                img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
                Image.fromarray(img_np).save(os.path.join(temp_dir, f"{i:05d}.png"))

            cmd = [
                "ffmpeg",
                "-y",
                "-framerate", str(fps),
                "-i", os.path.join(temp_dir, "%05d.png"),
            ]

            audio_file = None
            if audio:
                # audio is {"waveform": [Batch, Channels, Samples], "sample_rate": int}
                audio_file = tempfile.mktemp(suffix=".wav")
                # torchaudio.save expects [Channels, Samples], so we squeeze Batch if it's 1
                waveform = audio["waveform"]
                if waveform.dim() == 3:
                     waveform = waveform.squeeze(0)
                torchaudio.save(
                    audio_file, waveform.cpu(), audio["sample_rate"]
                )
                cmd.extend(["-i", audio_file])

            video_codec, quality_option = cls._get_codec_options(codec)
            cmd.extend([
                "-c:v", video_codec,
                quality_option, str(crf_or_cq),
                "-preset", preset,
                "-pix_fmt", "yuv420p",
            ])

            if audio:
                cmd.extend(["-c:a", "aac", "-shortest"])

            cmd.append(output_path)
            
            subprocess.run(cmd, check=True, capture_output=True, text=True)

            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg failed: {e.stderr}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

        return io.NodeOutput(output_path)
