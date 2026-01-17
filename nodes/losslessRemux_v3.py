import os
import subprocess
import folder_paths
from comfy_api.latest import io


class RemuxVideoV3(io.ComfyNode):
    """
    A V3 node to change the container of a video file.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="RemuxVideoV3",
            display_name="🔥Remux Video (V3)",
            category="🔥FFmpeg/Advanced",
            inputs=[
                io.String.Input("video", tooltip="The video file to remux."),
                # Using io.Combo for container selection
                io.Combo.Input(
                    "container",
                    ["mp4", "mkv", "mov", "webm"],
                    tooltip="Target container format.",
                ),
                io.String.Input(
                    "filename", default="remuxed_video.mkv", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the remuxed video file."),
            ],
        )

    @classmethod
    def execute(cls, video, container, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        # Ensure filename has correct extension
        base, _ = os.path.splitext(filename)
        filename = f"{base}.{container}"

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        # FFmpeg infers format from extension, no need for -f
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
