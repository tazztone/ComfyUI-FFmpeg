from ..func import get_image_paths_from_directory

import os
import folder_paths
from PIL import Image
import numpy as np
import torch


class LoadImagesFromDirectory:
    """
    A node to load all images from a directory and return them as an IMAGE tensor.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": (
                    "STRING",
                    {
                        "default": "images",
                        "tooltip": "The directory to load images from.",
                    },
                ),
                # TODO: Expose start_index and length inputs to support batch processing and avoid OOM
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_images"
    CATEGORY = "🔥FFmpeg/IO"

    def load_images(self, directory):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        # TODO: Use get_image_paths_from_directory() from func.py instead of re-implementing logic
        image_files = sorted(
            [f for f in os.listdir(directory) if f.endswith((".png", ".jpg", ".jpeg"))]
        )
        if not image_files:
            raise ValueError("No images found in the directory.")

        # TODO: Performance Warning - Loading all images into memory. Use batching/generator.
        images = [Image.open(os.path.join(directory, f)) for f in image_files]
        tensors = [
            torch.from_numpy(np.array(img).astype(np.float32) / 255.0) for img in images
        ]

        return (torch.stack(tensors),)
