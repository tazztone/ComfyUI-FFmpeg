from ..func import get_image_paths_from_directory

class LoadImageFromDir:
    """A node to load a list of image paths from a directory.

    This node scans a directory for image files and returns a list of their
    paths. It allows specifying a starting index and the number of images to
    load.
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
                "images_path": ("STRING", {
                    "default":"C:/Users/Desktop/",
                    "tooltip": "The directory containing the image files to load."
                }),
                "start_index": ("INT",{
                    "default":0,"min":0,
                    "tooltip": "The starting index of the images to load from the directory."
                }),
                "length": ("INT",{
                    "default":0,"min":0,
                    "tooltip": "The number of images to load. Set to 0 to load all images."
                })
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("image_paths",)
    FUNCTION = "load_image_from_dir"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/auxiliary tool"
  
    def load_image_from_dir(self, images_path, start_index, length):
        """Loads a list of image paths from a directory.

        Args:
            images_path (str): The path to the directory containing the images.
            start_index (int): The starting index of the images to load.
            length (int): The number of images to load.

        Returns:
            tuple: A tuple containing a list of image paths.
        """
        try:
            image_paths = get_image_paths_from_directory(images_path, start_index, length)
            return (image_paths,)
        except Exception as e:
            raise ValueError(e)