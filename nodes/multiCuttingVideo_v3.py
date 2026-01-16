import os
import subprocess
import folder_paths
from comfy_api.latest import io


class SplitVideoV3(io.ComfyNode):
    """
    A V3 node to cut a video into multiple segments.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="SplitVideoV3",
            display_name="🔥Split Video (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input(
                    "video", default="video.mp4", tooltip="The video file to split."
                ),
                io.Int.Input(
                    "segment_duration",
                    default=10,
                    min=1,
                    tooltip="Duration of each segment in seconds.",
                ),
                io.String.Input(
                    "output_prefix",
                    default="segment_",
                    tooltip="Prefix for output files.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The directory containing the segments."),
            ],
        )

    @classmethod
    def execute(cls, video, segment_duration, output_prefix) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_dir = folder_paths.get_output_directory()
        # Ensure output filename pattern is correct
        output_pattern = os.path.join(output_dir, f"{output_prefix}%03d.mp4")

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-c",
            "copy",
            "-map",
            "0",
            "-segment_time",
            str(segment_duration),
            "-f",
            "segment",
            output_pattern,
        ]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_dir)
