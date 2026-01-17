import os
import subprocess
import folder_paths
from comfy_api.latest import io


class ReverseVideoV3(io.ComfyNode):
    """
    A V3 node to reverse a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ReverseVideoV3",
            display_name="🔥Reverse Video (V3)",
            category="🔥FFmpeg/IO",
            inputs=[
                io.String.Input("video", tooltip="The video file to reverse."),
                io.Boolean.Input(
                    "reverse_audio", default=True, tooltip="Reverse audio as well."
                ),
                io.String.Input(
                    "filename", default="reversed_video.mp4", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the reversed video file."),
            ],
        )

    @classmethod
    def execute(cls, video, reverse_audio, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ["ffmpeg", "-y", "-i", video, "-vf", "reverse"]
        if reverse_audio:
            command.extend(["-af", "areverse"])

        command.append(output_path)

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
