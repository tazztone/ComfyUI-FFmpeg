import json
import os
import subprocess
import tempfile
import shutil
import glob
import torch
from PIL import Image
import numpy as np
from comfy_api.latest import io


class Video2FramesV3(io.ComfyNode):
    """
    A V3 node to extract frames from a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="Video2FramesV3",
            display_name="🔥Video to Frames (V3)",
            category="🔥FFmpeg/Conversion",
            inputs=[
                io.String.Input("video", default="sample.mp4", tooltip="Video file."),
                io.Int.Input(
                    "max_width",
                    default=0,
                    min=0,
                    max=4096,
                    tooltip="Max width (0 for original).",
                ),
                io.Boolean.Input(
                    "save_frames",
                    default=False,
                    tooltip="Save extracted frames to disk.",
                ),
                io.String.Input(
                    "output_dir",
                    default="frames",
                    tooltip="Directory to save frames (if enabled).",
                ),
            ],
            outputs=[
                io.Image.Output(tooltip="The extracted frames."),
                io.Int.Output(tooltip="Number of frames."),
            ],
        )

    @classmethod
    def execute(cls, video, max_width, save_frames, output_dir="frames") -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        temp_dir = tempfile.mkdtemp()

        # Probe video
        probe_cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-of",
            "json",
            video,
        ]
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        video_info = json.loads(probe_result.stdout)
        width = video_info["streams"][0]["width"]

        scale_filter = ""
        if max_width > 0 and width > max_width:
            scale_filter = f"scale={max_width}:-1"

        ffmpeg_cmd = ["ffmpeg", "-i", video]
        if scale_filter:
            ffmpeg_cmd.extend(["-vf", scale_filter])
        ffmpeg_cmd.append(os.path.join(temp_dir, "%05d.png"))

        subprocess.run(ffmpeg_cmd, check=True)

        frame_files = sorted(glob.glob(os.path.join(temp_dir, "*.png")))
        images = [Image.open(f) for f in frame_files]

        if save_frames:
            os.makedirs(output_dir, exist_ok=True)
            for i, frame in enumerate(images):
                frame.save(os.path.join(output_dir, f"frame_{i:05d}.png"))

        tensors = [
            torch.from_numpy(np.array(img).astype(np.float32) / 255.0) for img in images
        ]

        # Check if we have frames, stack relies on non-empty list usually
        if tensors:
            batch_tensor = torch.stack(tensors)
        else:
            # Empty tensor?
            batch_tensor = torch.zeros((0, 1, 1, 3))  # Dummy structure

        shutil.rmtree(temp_dir)

        return io.NodeOutput(batch_tensor, len(images))
