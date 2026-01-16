import os
import subprocess
import tempfile
import shutil
import torchaudio
from PIL import Image
import numpy as np
import folder_paths
from comfy_api.latest import io


class Frames2VideoV3(io.ComfyNode):
    """
    A V3 node to convert frames to a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="Frames2VideoV3",
            display_name="🔥Frames to Video (V3)",
            category="🔥FFmpeg/Conversion",
            inputs=[
                io.Image.Input("images", tooltip="Input images."),
                io.Int.Input("fps", default=24, min=1, tooltip="Frame rate."),
                io.Combo.Input(
                    "codec",
                    ["h264_cpu", "h265_cpu", "h264_nvidia", "h265_nvidia"],
                    tooltip="Video codec.",
                ),
                io.Int.Input(
                    "crf",
                    default=23,
                    min=0,
                    max=51,
                    tooltip="CRF (Quality, lower is better).",
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
                    tooltip="Encoding preset.",
                ),
                io.String.Input(
                    "filename", default="output.mp4", tooltip="Output filename."
                ),
                # Optional
                io.Audio.Input("audio", tooltip="Optional audio track."),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output video file."),
            ],
        )

    @staticmethod
    def _get_codec_options(codec, crf):
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
        cls, images, fps, codec, crf, preset, filename, audio=None
    ) -> io.NodeOutput:
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        try:
            # images is simple tensor stack usually, check logic
            for i, img_tensor in enumerate(images):
                img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
                Image.fromarray(img_np).save(os.path.join(temp_dir, f"{i:05d}.png"))

            cmd = [
                "ffmpeg",
                "-y",
                "-framerate",
                str(fps),
                "-i",
                os.path.join(temp_dir, "%05d.png"),
            ]

            audio_file = None
            if audio:
                audio_file = tempfile.mktemp(suffix=".wav")
                torchaudio.save(
                    audio_file, audio["waveform"].cpu(), audio["sample_rate"]
                )
                cmd.extend(["-i", audio_file])

            video_codec, crf_option = cls._get_codec_options(codec, crf)
            cmd.extend(
                [
                    "-c:v",
                    video_codec,
                    crf_option,
                    str(crf),
                    "-preset",
                    preset,
                    "-pix_fmt",
                    "yuv420p",
                ]
            )

            if audio:
                cmd.extend(["-c:a", "aac", "-shortest"])

            cmd.append(output_path)
            subprocess.run(cmd, check=True)

            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

        return io.NodeOutput(output_path)
