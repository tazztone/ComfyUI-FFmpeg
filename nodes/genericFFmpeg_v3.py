import os
import subprocess
import shlex
import folder_paths
from comfy_api.latest import io


class GenericFFmpegV3(io.ComfyNode):
    """
    A generic V3 node to execute custom FFmpeg commands.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="GenericFFmpegV3",
            display_name="🔥Generic FFmpeg (V3)",
            category="🔥FFmpeg/Advanced",
            inputs=[
                io.String.Input("video", tooltip="The input video file."),
                io.String.Input(
                    "ffmpeg_command",
                    default="-vf hflip",
                    multiline=True,
                    tooltip="The FFmpeg command arguments.",
                ),
                io.String.Input(
                    "filename",
                    default="generic_output.mp4",
                    tooltip="The output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output video file."),
            ],
        )

    @classmethod
    def execute(cls, video, ffmpeg_command, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        # Securely construct command
        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            *shlex.split(ffmpeg_command),
            output_path,
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return io.NodeOutput(output_path)
