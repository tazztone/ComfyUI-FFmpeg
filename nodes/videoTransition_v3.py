import os
import subprocess
import folder_paths
from comfy_api.latest import io

# Assuming this util is available like in V1
from ..func import get_xfade_transitions


class VideoTransitionV3(io.ComfyNode):
    """
    A V3 node to create a transition between two videos.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="VideoTransitionV3",
            display_name="🔥Video Transition (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input("video1", tooltip="The first video file."),
                io.String.Input("video2", tooltip="The second video file.", optional=True),
                io.Combo.Input(
                    "transition",
                    get_xfade_transitions(),
                    default="fade",
                    tooltip="Transition effect.",
                ),
                io.Float.Input(
                    "duration",
                    default=1.0,
                    min=0.1,
                    max=10.0,
                    tooltip="Duration in seconds.",
                ),
                io.Float.Input(
                    "offset",
                    default=2.0,
                    min=0.0,
                    tooltip="Time offset in first video.",
                ),
                io.String.Input(
                    "filename",
                    default="transition_video.mp4",
                    tooltip="Output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output video file."),
            ],
        )

    @classmethod
    def execute(
        cls, video1, video2, transition, duration, offset, filename
    ) -> io.NodeOutput:
        if not os.path.exists(video1):
            raise FileNotFoundError(f"Video 1 not found: {video1}")
        
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        if not video2 or not os.path.exists(video2):
             # Fallback: Just copy video1 if video2 is missing
             print("Warning: Video 2 not found or not provided for transition. Returning Video 1.")
             command = ["ffmpeg", "-y", "-i", video1, "-c", "copy", output_path]
             subprocess.run(command, check=True)
             return io.NodeOutput(output_path)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video1,
            "-i",
            video2,
            "-filter_complex",
            f"[0:v][1:v]xfade=transition={transition}:duration={duration}:offset={offset}[v];"
            f"[0:a][1:a]acrossfade=d={duration}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            output_path,
        ]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
