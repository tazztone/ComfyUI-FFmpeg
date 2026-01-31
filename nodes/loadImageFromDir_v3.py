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
                io.Int.Input(
                    "start_index",
                    default=0,
                    min=0,
                    tooltip="The starting index of the images to load.",
                ),
                io.Int.Input(
                    "length",
                    default=0,
                    min=0,
                    tooltip="The number of images to load. 0 means all images from start_index.",
                ),
            ],
            outputs=[
                io.Image.Output(tooltip="The loaded images as a batch tensor."),
            ],
        )

    @classmethod
    def execute(cls, directory: str, start_index: int, length: int) -> io.NodeOutput:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # Basic logic taken from V1 node
        image_files = sorted(
            [f for f in os.listdir(directory) if f.endswith((".png", ".jpg", ".jpeg"))]
        )
        if not image_files:
            raise ValueError("No images found in the directory.")

        if start_index >= len(image_files):
            raise ValueError("start_index is out of bounds.")

        if length > 0:
            image_files = image_files[start_index : start_index + length]
        else:
            image_files = image_files[start_index:]

        images = [Image.open(os.path.join(directory, f)) for f in image_files]
        tensors = [
            torch.from_numpy(np.array(img).astype(np.float32) / 255.0) for img in images
        ]

        return io.NodeOutput(torch.stack(tensors))
