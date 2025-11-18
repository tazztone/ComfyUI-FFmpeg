import os
import subprocess
import folder_paths
from ..func import set_file_name,video_type

current_path = os.path.abspath(__file__)
font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.normpath(__file__))), 'fonts')
folder_paths.folder_names_and_paths["fonts"] = ([font_dir], {'.ttf'})

class AddTextWatermark:
    """
    A node to add a text watermark to a video.
    This node overlays text onto a video at a specified position, with a
    customizable font, size, and color.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Specifies the input types for the node.
        Returns:
            dict: A dictionary containing the input types.
        """
        return {
            "required": {
                "video": ("STRING", {
                    "default": "sample.mp4",
                    "tooltip": "The video file to add the watermark to."
                }),
                "text": ("STRING", {
                    "default": "ComfyUI",
                    "tooltip": "The text to display as the watermark."
                }),
                "font_size": ("INT", {
                    "default": 48,
                    "min": 1,
                    "tooltip": "The font size of the watermark text."
                }),
                "font_color": ("STRING", {
                    "default": "white",
                    "tooltip": "The color of the watermark text."
                }),
                "position_x": ("INT", {
                    "default": 10,
                    "tooltip": "The x-coordinate of the watermark's position."
                }),
                "position_y": ("INT", {
                    "default": 10,
                    "tooltip": "The y-coordinate of the watermark's position."
                }),
                "font_file": (["default"] + folder_paths.get_filename_list("fonts"), {
                    "tooltip": "The font file to use for the watermark text."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "add_text_watermark"
    CATEGORY = "🔥FFmpeg/Watermark"

    def add_text_watermark(self, video, text, font_size, font_color, position_x, position_y, font_file):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), f"watermarked_{os.path.basename(video)}")

        font_path = "default"
        if font_file != "default":
            font_path = os.path.join(font_dir, font_file)

        command = [
            'ffmpeg', '-y', '-i', video,
            '-vf', f"drawtext=text='{text}':fontfile='{font_path}':fontsize={font_size}:fontcolor={font_color}:x={position_x}:y={position_y}",
            output_path
        ]
        
        subprocess.run(command, check=True)
        return (output_path,)