import os
import subprocess
import json
from comfy_api.latest import io


class AnalyzeStreamsV3(io.ComfyNode):
    """
    A V3 node to analyze the streams of a video file.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AnalyzeStreamsV3",
            display_name="🔥Analyze Streams (V3)",
            category="🔥FFmpeg/TestV3",
            inputs=[
                io.String.Input(
                    "video", default="video.mp4", tooltip="The video file to analyze."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="JSON string containing stream information."),
            ],
        )

    @classmethod
    def execute(cls, video) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        command = ["ffprobe", "-v", "error", "-show_streams", "-of", "json", video]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return io.NodeOutput(json.dumps(json.loads(result.stdout), indent=4))
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFprobe error: {e.stderr}")
