import os
import shutil
import folder_paths
from PIL import Image
import numpy as np

class CopyImages:
    """
    A node to copy a list of images to a specified directory.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {
                    "tooltip": "The images to be copied."
                }),
                "directory": ("STRING", {
                    "default": "copied_images",
                    "tooltip": "The directory to copy the images to. This will be created in the ComfyUI output directory."
                }),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "copy_images"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/IO"

    def copy_images(self, images, directory):
        output_dir = os.path.join(folder_paths.get_output_directory(), directory)
        os.makedirs(output_dir, exist_ok=True)

        for i, image_tensor in enumerate(images):
            img_np = (image_tensor.cpu().numpy() * 255).astype(np.uint8)
            img = Image.fromarray(img_np)

            filepath = os.path.join(output_dir, f"image_{i:05d}.png")
            img.save(filepath)

        return ()