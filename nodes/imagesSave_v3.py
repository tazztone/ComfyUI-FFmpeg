import os
import torch
from PIL import Image
import numpy as np
import folder_paths
from comfy_api.latest import io


class SaveImagesV3(io.ComfyNode):
    """
    A V3 node to save a batch of images to a specified directory.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="SaveImagesV3",
            display_name="🔥Save Images (V3)",
            category="🔥FFmpeg/IO",
            inputs=[
                io.Image.Input("images", tooltip="The images to be saved."),
                io.String.Input(
                    "directory",
                    default="saved_images",
                    tooltip="The directory to save the images to (in output dir).",
                ),
                io.String.Input(
                    "filename_prefix",
                    default="image",
                    tooltip="The prefix for the saved image filenames.",
                ),
            ],
            outputs=[],  # Output node returning nothing
        )

    @classmethod
    def execute(cls, images, directory, filename_prefix) -> io.NodeOutput:
        output_dir = os.path.join(folder_paths.get_output_directory(), directory)
        os.makedirs(output_dir, exist_ok=True)

        for i, image_tensor in enumerate(images):
            # Ensure tensor is CPU and numpy-compatible
            img_np = (image_tensor.cpu().numpy() * 255).astype(np.uint8)
            img = Image.fromarray(img_np)

            filepath = os.path.join(output_dir, f"{filename_prefix}_{i:05d}.png")
            img.save(filepath)

        return io.NodeOutput()
