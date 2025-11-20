import os
import subprocess
import folder_paths
try:
    from ..func import validate_file_exists, get_output_path
except ImportError:
    from func import validate_file_exists, get_output_path

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
    RETURN_NAMES = ("video_path",)
    FUNCTION = "add_text_watermark"
    CATEGORY = "🔥FFmpeg/Watermark"

    def add_text_watermark(self, video, text, font_size, font_color, position_x, position_y, font_file):
        validate_file_exists(video, "Video")

        output_path = get_output_path(os.path.basename(video), prefix="watermarked_")

        font_path = "default"
        if font_file != "default":
            font_path = os.path.join(font_dir, font_file)
            # We can validate font exists too, though folder_paths likely handles it
            validate_file_exists(font_path, "Font")

        # Escape text for drawtext filter
        # FFmpeg drawtext filter special characters escaping
        text_escaped = text.replace(":", "\\:").replace("'", "")

        font_arg = f":fontfile='{font_path}'" if font_file != "default" else ""

        command = [
            'ffmpeg', '-y', '-i', video,
            '-vf', f"drawtext=text='{text_escaped}'{font_arg}:fontsize={font_size}:fontcolor={font_color}:x={position_x}:y={position_y}",
            output_path
        ]
        
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")

        return (output_path,)
