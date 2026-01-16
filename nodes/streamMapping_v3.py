import os
import subprocess
import shlex
import folder_paths
from comfy_api.latest import io


class ApplyStreamMapV3(io.ComfyNode):
    """
    A V3 node to apply stream mapping to a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ApplyStreamMapV3",
            display_name="🔥Apply Stream Map (V3)",
            category="🔥FFmpeg/Advanced",
            inputs=[
                io.String.Input("video", default="video.mp4", tooltip="Input video."),
                io.String.Input(
                    "stream_map",
                    default="-map 0:v -map 0:a:0?",
                    multiline=True,
                    tooltip="Stream mapping arguments.",
                ),
                io.String.Input(
                    "filename", default="mapped_video.mp4", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the mapped video file."),
            ],
        )

    @classmethod
    def execute(cls, video, stream_map, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            *shlex.split(stream_map),
            "-c",
            "copy",
            output_path,
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return io.NodeOutput(output_path)
