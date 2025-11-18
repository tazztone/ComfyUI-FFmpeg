import os
import torch
import gc
from concurrent.futures import ThreadPoolExecutor
from ..func import save_image,clear_memory
file_name_num_start = 0

import os
import torch
from PIL import Image
import numpy as np
import folder_paths

class SaveImages:
    """
    A node to save a batch of images to a specified directory.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {
                    "tooltip": "The images to be saved."
                }),
                "directory": ("STRING", {
                    "default": "saved_images",
                    "tooltip": "The directory to save the images to. This will be created in the ComfyUI output directory."
                }),
                "filename_prefix": ("STRING", {
                    "default": "image",
                    "tooltip": "The prefix for the saved image filenames."
                }),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/IO"

    def save_images(self, images, directory, filename_prefix):
        output_dir = os.path.join(folder_paths.get_output_directory(), directory)
        os.makedirs(output_dir, exist_ok=True)

        for i, image_tensor in enumerate(images):
            img_np = (image_tensor.cpu().numpy() * 255).astype(np.uint8)
            img = Image.fromarray(img_np)
            
            filepath = os.path.join(output_dir, f"{filename_prefix}_{i:05d}.png")
            img.save(filepath)
            
        return ()