import os
import subprocess
import folder_paths
from comfy_api.latest import io


class VideoFlipV3(io.ComfyNode):
    """
    A V3 node to flip a video horizontally, vertically, or both.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="VideoFlipV3",
            display_name="🔥Flip Video (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input(
                    "video", default="video.mp4", tooltip="The video file to flip."
                ),
                io.Combo.Input(
                    "flip_type",
                    ["horizontal", "vertical", "both"],
                    default="horizontal",
                    tooltip="Direction to flip the video.",
                ),
                io.String.Input(
                    "filename",
                    default="flipped_video_v3.mp4",
                    tooltip="Output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the flipped video file."),
            ],
        )

    @classmethod
    def execute(cls, video, flip_type, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        flip_map = {
            "horizontal": "hflip",
            "vertical": "vflip",
            "both": "hflip,vflip",
        }

        command = ["ffmpeg", "-y", "-i", video, "-vf", flip_map[flip_type], output_path]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
