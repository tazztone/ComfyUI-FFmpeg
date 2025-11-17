from ..func import copy_images_to_directory

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")

class ImageCopy:
    """A node to copy a list of images to a specified directory.

    This node takes a list of image paths and copies them to a new location.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """Specifies the input types for the node.

        Returns:
            dict: A dictionary containing the input types.
        """
        return {
            "required": { 
                "image_paths": (any_type, {
                    "tooltip": "A list of image file paths to be copied."
                }),
                "output_path": ("STRING", {
                    "default": "C:/Users/Desktop/output",
                    "tooltip": "The directory where the images will be copied to."
                }),
            },
        }

    RETURN_TYPES = ("LIST","INT","STRING")
    RETURN_NAMES = ("image_paths","image_length","output_path")
    FUNCTION = "image_copy"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/auxiliary tool"
  
    def image_copy(self, image_paths, output_path):
        """Copies a list of images to a specified directory.

        Args:
            image_paths (list): A list of paths to the image files to copy.
            output_path (str): The directory to copy the images to.

        Returns:
            tuple: A tuple containing the list of new image paths, the number
                   of images copied, and the output path.
        """
        try:
            image_output_path = copy_images_to_directory(image_paths,output_path)
            return (image_output_path,len(image_output_path),output_path)
        except Exception as e:
            raise ValueError(e)