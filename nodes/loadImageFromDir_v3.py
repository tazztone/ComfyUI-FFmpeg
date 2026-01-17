import os
import torch
import numpy as np
from PIL import Image
from comfy_api.latest import io


class LoadImagesFromDirectoryV3(io.ComfyNode):
    """
    A V3 node to load all images from a directory and return them as an IMAGE tensor.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="LoadImagesFromDirectoryV3",
            display_name="🔥Load Images from Directory (V3)",
            category="🔥FFmpeg/IO",
            inputs=[
                io.String.Input(
                    "directory",
                    tooltip="The directory to load images from.",
                ),
                # TODO: Expose start_index and length inputs when ready
            ],
            outputs=[
                io.Image.Output(tooltip="The loaded images as a batch tensor."),
            ],
        )

    @classmethod
    def execute(cls, directory: str) -> io.NodeOutput:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Basic logic taken from V1 node
        image_files = sorted(
            [f for f in os.listdir(directory) if f.endswith((".png", ".jpg", ".jpeg"))]
        )
        if not image_files:
            raise ValueError("No images found in the directory.")

        images = [Image.open(os.path.join(directory, f)) for f in image_files]
        tensors = [
            torch.from_numpy(np.array(img).astype(np.float32) / 255.0) for img in images
        ]

        return io.NodeOutput(torch.stack(tensors))
