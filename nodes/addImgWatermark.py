import os
import subprocess
try:
    from ..func import validate_file_exists, save_tensor_to_temp_file, get_output_path
except ImportError:
    from func import validate_file_exists, save_tensor_to_temp_file, get_output_path

class AddImgWatermark:
    """
    A node to add an image watermark to a video.
    This node overlays an image onto a video at a specified position and size.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video": ("STRING", {
                    "default": "sample.mp4",
                    "tooltip": "The video file to add the watermark to."
                }),
                "width": ("INT", {
                    "default": 100,
                    "min": 1,
                    "tooltip": "The width of the watermark image. The height will be scaled automatically."
                }),
                "position_x": ("INT", {"default": 10}),
                "position_y": ("INT", {"default": 10}),
            },
            "optional": {
                "watermark_image_tensor": ("IMAGE", {
                    "tooltip": "Watermark image from ComfyUI nodes (takes priority over path)."
                }),
                "watermark_image": ("STRING", {
                    "default": "logo.png",
                    "tooltip": "Path to watermark image file (used if tensor not provided)."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "add_img_watermark"
    CATEGORY = "🔥FFmpeg/Watermark"

    def add_img_watermark(self, video, width, position_x, position_y,
                           watermark_image_tensor=None, watermark_image=""):

        # Validate video input
        validate_file_exists(video, "Video")

        # Handle watermark source priority: tensor > path
        if watermark_image_tensor is not None:
            # Convert tensor to temp file
            watermark_path = save_tensor_to_temp_file(watermark_image_tensor[0], "watermark")
        elif watermark_image:
            validate_file_exists(watermark_image, "Watermark image")
            watermark_path = watermark_image
        else:
            raise ValueError("Either watermark_image_tensor or watermark_image (path) must be provided")

        # Generate output path
        output_path = get_output_path(os.path.basename(video), prefix="watermarked_")

        # Build FFmpeg command
        command = [
            'ffmpeg', '-y', '-i', video, '-i', watermark_path,
            '-filter_complex',
            f"[1:v]scale={width}:-1[wm];[0:v][wm]overlay={position_x}:{position_y}",
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")
        finally:
            # Clean up temp file if created
            if watermark_image_tensor is not None and os.path.exists(watermark_path):
                os.remove(watermark_path)

        return (output_path,)
