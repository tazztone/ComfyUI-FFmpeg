import os
import subprocess
import tempfile
import shutil
import torch
import numpy as np
from PIL import Image
from comfy_api.latest import io

class ThumbnailExtractV3(io.ComfyNode):
    """
    A V3 node to extract a single frame at a given timestamp as an IMAGE tensor.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ThumbnailExtractV3",
            display_name="🔥Thumbnail Extract (V3)",
            category="🔥FFmpeg/Conversion",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.String.Input("timestamp", default="00:00:01", tooltip="Timestamp to extract (HH:MM:SS or seconds)."),
                io.Int.Input("max_width", default=0, min=0, tooltip="Max width (0 for original)."),
            ],
            outputs=[
                io.Image.Output(tooltip="The extracted frame."),
            ],
        )

    @classmethod
    def execute(cls, video, timestamp, max_width) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        temp_dir = tempfile.mkdtemp()
        output_image = os.path.join(temp_dir, "thumb.png")

        # Build FFmpeg command
        # Use -ss before -i for fast seeking
        cmd = ["ffmpeg", "-y", "-ss", timestamp, "-i", video]
       
        vf = []
        if max_width > 0:
            vf.append(f"scale={max_width}:-1")
           
        if vf:
            cmd.extend(["-vf", ",".join(vf)])
           
        cmd.extend(["-vframes", "1", output_image])

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
           
            if not os.path.exists(output_image):
                raise RuntimeError(f"Failed to extract thumbnail at {timestamp}")
               
            img = Image.open(output_image).convert("RGB")
            tensor = torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0)
           
            return io.NodeOutput(tensor)
           
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
