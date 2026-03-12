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
                "start_index": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "step": 1,
                        "tooltip": "The starting index of the images to load.",
                    },
                ),
                "length": (
                    "INT",
                    {
                        "default": -1,
                        "min": -1,
                        "step": 1,
                        "tooltip": "The number of images to load. -1 for all.",
                    },
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_images"
    CATEGORY = "🔥FFmpeg/IO"

    def load_images(self, directory, start_index, length):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        image_files = get_image_paths_from_directory(directory, start_index, length)
        if not image_files:
            raise ValueError("No images found in the directory.")

        images = [Image.open(f) for f in image_files]
        tensors = [
            torch.from_numpy(np.array(img).astype(np.float32) / 255.0) for img in images
        ]

        return (torch.stack(tensors),)
