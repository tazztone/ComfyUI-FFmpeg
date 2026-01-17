import os
import subprocess
import folder_paths
from comfy_api.latest import io

# Setup fonts path similar to V1
current_path = os.path.abspath(__file__)
# Assuming this file is in 'nodes', so parent is root
font_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.normpath(__file__))), "fonts"
)
# Register fonts folder if not present? V1 does it.
if "fonts" not in folder_paths.folder_names_and_paths:
    folder_paths.folder_names_and_paths["fonts"] = ([font_dir], {".ttf"})
elif font_dir not in folder_paths.folder_names_and_paths["fonts"][0]:
    # Append if existing but missing this dir (unlikely but safe)
    folder_paths.folder_names_and_paths["fonts"][0].append(font_dir)


class AddTextWatermarkV3(io.ComfyNode):
    """
    A V3 node to add a text watermark to a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        # Dynamic font list
        fonts = ["default"] + folder_paths.get_filename_list("fonts")

        return io.Schema(
            node_id="AddTextWatermarkV3",
            display_name="🔥Add Text Watermark (V3)",
            category="🔥FFmpeg/Watermark",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.String.Input("text", default="ComfyUI", tooltip="Watermark text."),
                io.Int.Input("font_size", default=48, min=1, tooltip="Font size."),
                io.String.Input("font_color", default="white", tooltip="Font color."),
                io.Int.Input("position_x", default=10, tooltip="X position."),
                io.Int.Input("position_y", default=10, tooltip="Y position."),
                io.Combo.Input(
                    "font_file", fonts, default="default", tooltip="Font file."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the watermarked video file."),
            ],
        )

    @classmethod
    def execute(
        cls, video, text, font_size, font_color, position_x, position_y, font_file
    ) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(
            folder_paths.get_output_directory(),
            f"watermarked_{os.path.basename(video)}",
        )

        font_path = "default"
        if font_file != "default":
            font_path = os.path.join(font_dir, font_file)

        text_escaped = text.replace(":", "\\:").replace("'", "")
        font_arg = f":fontfile='{font_path}'" if font_file != "default" else ""

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-vf",
            f"drawtext=text='{text_escaped}'{font_arg}:fontsize={font_size}:fontcolor={font_color}:x={position_x}:y={position_y}",
            output_path,
        ]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
