import os
import subprocess
import folder_paths
from comfy_api.latest import io


class TrimVideoV3(io.ComfyNode):
    """
    A V3 node to cut a single segment from a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="TrimVideoV3",
            display_name="🔥Trim Video (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input("video", tooltip="The video file to trim."),
                io.String.Input(
                    "start_time", default="00:00:00", tooltip="Start time (HH:MM:SS)."
                ),
                io.String.Input(
                    "end_time", default="00:00:10", tooltip="End time (HH:MM:SS)."
                ),
                io.String.Input(
                    "filename", default="trimmed_video.mp4", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the trimmed video file."),
            ],
        )

    @classmethod
    def execute(cls, video, start_time, end_time, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-ss",
            start_time,
            "-to",
            end_time,
            "-c",
            "copy",
            output_path,
        ]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
