import os
import subprocess
import folder_paths
from comfy_api.latest import io

try:
    from ..func import save_tensor_to_temp_file
except ImportError:
    from func import save_tensor_to_temp_file


class PictureInPictureV3(io.ComfyNode):
    """
    A V3 node to create a picture-in-picture video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="PictureInPictureV3",
            display_name="🔥Picture In Picture (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input(
                    "background_video",
                    default="background.mp4",
                    tooltip="Background video.",
                ),
                io.Combo.Input(
                    "position",
                    ["top_left", "top_right", "bottom_left", "bottom_right", "center"],
                    tooltip="Position.",
                ),
                io.Float.Input(
                    "scale",
                    default=0.5,
                    min=0.1,
                    max=1.0,
                    tooltip="Scale of foreground.",
                ),
                io.Combo.Input(
                    "audio_source",
                    ["background", "foreground", "none"],
                    default="background",
                    tooltip="Audio source.",
                ),
                io.String.Input(
                    "filename", default="pip_video.mp4", tooltip="Output filename."
                ),
                # Optional inputs
                io.String.Input(
                    "foreground_video", default="", tooltip="Foreground video path."
                ),
                io.Image.Input(
                    "foreground_image", tooltip="Foreground image tensor."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output video file."),
            ],
        )

    @classmethod
    def execute(cls, 
        background_video,
        position,
        scale,
        audio_source,
        filename,
        foreground_video="",
        foreground_image=None,
    ) -> io.NodeOutput:
        if not os.path.exists(background_video):
            raise FileNotFoundError(f"Background video not found: {background_video}")

        # Determine foreground source
        temp_files = []
        foreground_is_image = False

        # Check if foreground_image is provided (it might comes as a list/tensor wrapper in V3?
        # Assuming mapped to raw tensor or list of tensors. V1 passed list.
        # Io.Image.Input likely passes list of tensors?
        # But V1 logic assumes input is a list `foreground_image[0]`.
        # I'll check if it's not None.

        if foreground_image is not None:
            # Safe check if it's a list or tensor
            if isinstance(foreground_image, list) or (
                hasattr(foreground_image, "shape") and len(foreground_image.shape) == 4
            ):
                fg_img = (
                    foreground_image[0]
                    if isinstance(foreground_image, list)
                    else foreground_image
                )
                foreground_path = save_tensor_to_temp_file(fg_img, "fg")
                temp_files.append(foreground_path)
                foreground_is_image = True
            else:
                # Fallback/Error if format unexpected?
                # Assuming V3 handles passing it as is.
                # If io.Image.Input receives a wrapper object, I might need to unpack.
                # For now assuming standard behavior matching V1.
                raise ValueError(
                    f"Unexpected foreground_image format: {type(foreground_image)}"
                )

        elif foreground_video:
            if not os.path.exists(foreground_video):
                raise FileNotFoundError(
                    f"Foreground video not found: {foreground_video}"
                )
            foreground_path = foreground_video
        else:
            raise ValueError(
                "Either foreground_video or foreground_image must be provided"
            )

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        position_map = {
            "top_left": "10:10",
            "top_right": "W-w-10:10",
            "bottom_left": "10:H-h-10",
            "bottom_right": "W-w-10:H-h-10",
            "center": "(W-w)/2:(H-h)/2",
        }

        filter_complex = (
            f"[1:v]scale=iw*{scale}:-1[fg];[0:v][fg]overlay={position_map[position]}"
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            background_video,
            "-i",
            foreground_path,
            "-filter_complex",
            filter_complex,
        ]

        if foreground_is_image and audio_source == "foreground":
            print(
                "Warning: Foreground is an image, ignoring audio_source='foreground'."
            )
            audio_source = "none"

        if audio_source != "none":
            audio_map = {"background": "0:a", "foreground": "1:a"}
            command.extend(
                ["-map", "0:v", "-map", audio_map[audio_source], "-shortest"]
            )

        command.append(output_path)

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")
        finally:
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

        return io.NodeOutput(output_path)
