import os
import subprocess
import folder_paths

class AddImgWatermark:
    """
    A node to add an image watermark to a video.
    This node overlays an image onto a video at a specified position and size.
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
                "watermark_image": ("STRING", {
                    "default": "logo.png",
                    "tooltip": "The image file to use as a watermark."
                }),
                "width": ("INT", {
                    "default": 100,
                    "min": 1,
                    "tooltip": "The width of the watermark image. The height will be scaled automatically."
                }),
                "position_x": ("INT", {
                    "default": 10,
                    "tooltip": "The x-coordinate of the watermark's position."
                }),
                "position_y": ("INT", {
                    "default": 10,
                    "tooltip": "The y-coordinate of the watermark's position."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "add_img_watermark"
    CATEGORY = "🔥FFmpeg/Watermark"

    def add_img_watermark(self, video, watermark_image, width, position_x, position_y):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")
        if not os.path.exists(watermark_image):
            raise FileNotFoundError(f"Watermark image file not found: {watermark_image}")

        output_path = os.path.join(folder_paths.get_output_directory(), f"watermarked_{os.path.basename(video)}")

        command = [
            'ffmpeg', '-y', '-i', video, '-i', watermark_image,
            '-filter_complex', f"[1:v]scale={width}:-1[wm];[0:v][wm]overlay={position_x}:{position_y}",
            output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)