import os
import subprocess
import folder_paths
from comfy_api.latest import io

try:
    from ..func import save_tensor_to_temp_file
except ImportError:
    from func import save_tensor_to_temp_file


class AddImgWatermarkV3(io.ComfyNode):
    """
    A V3 node to add an image watermark to a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AddImgWatermarkV3",
            display_name="🔥Add Image Watermark (V3)",
            category="🔥FFmpeg/Watermark",
            inputs=[
                io.String.Input("video", default="sample.mp4", tooltip="Video file."),
                io.Int.Input("width", default=100, min=1, tooltip="Watermark width."),
                io.Int.Input("position_x", default=10, tooltip="X position."),
                io.Int.Input("position_y", default=10, tooltip="Y position."),
                # Optional inputs
                io.Image.Input(
                    "watermark_image_tensor", tooltip="Watermark tensor.", optional=True
                ),
                io.String.Input(
                    "watermark_image",
                    default="logo.png",
                    tooltip="Watermark image path.",
                    optional=True,
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the watermarked video file."),
            ],
        )

    @classmethod
    def execute(cls, 
        video,
        width,
        position_x,
        position_y,
        watermark_image_tensor=None,
        watermark_image="",
    ) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        watermark_path = ""
        temp_file_created = False

        if watermark_image_tensor is not None:
            # Similar handling as PiP
            fg_img = (
                watermark_image_tensor[0]
                if isinstance(watermark_image_tensor, list)
                else watermark_image_tensor
            )
            watermark_path = save_tensor_to_temp_file(fg_img, "watermark")
            temp_file_created = True
        elif watermark_image:
            if not os.path.exists(watermark_image):
                raise FileNotFoundError(f"Watermark image not found: {watermark_image}")
            watermark_path = watermark_image
        else:
             # Just copy the video to the output path if no watermark is provided
             # But we should probably rename it to "watermarked_..." still?
             # Or just return a copy.
             output_path = os.path.join(
                folder_paths.get_output_directory(),
                f"watermarked_{os.path.basename(video)}",
             )
             command = [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-c",
                "copy",
                output_path,
             ]
             subprocess.run(command, check=True)
             return io.NodeOutput(output_path)

        output_path = os.path.join(
            folder_paths.get_output_directory(),
            f"watermarked_{os.path.basename(video)}",
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-i",
            watermark_path,
            "-filter_complex",
            f"[1:v]scale={width}:-1[wm];[0:v][wm]overlay={position_x}:{position_y}",
            output_path,
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")
        finally:
            if temp_file_created and os.path.exists(watermark_path):
                os.remove(watermark_path)

        return io.NodeOutput(output_path)
