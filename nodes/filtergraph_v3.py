import os
import subprocess
import shlex
import folder_paths
from comfy_api.latest import io


class ApplyFiltergraphV3(io.ComfyNode):
    """
    A V3 node to apply a raw FFmpeg filtergraph to a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ApplyFiltergraphV3",
            display_name="🔥Apply Filtergraph (V3)",
            category="🔥FFmpeg/Advanced",
            inputs=[
                io.String.Input("video", default="video.mp4", tooltip="Video file."),
                io.String.Input(
                    "filtergraph",
                    default="vf hflip",
                    multiline=True,
                    tooltip="FFmpeg filtergraph.",
                ),
                io.String.Input(
                    "filename", default="filtered_video.mp4", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the filtered video file."),
            ],
        )

    @classmethod
    def execute(cls, video, filtergraph, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ["ffmpeg", "-y", "-i", video, *shlex.split(filtergraph), output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return io.NodeOutput(output_path)
