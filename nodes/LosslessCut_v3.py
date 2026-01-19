import os
import subprocess
from datetime import datetime
import folder_paths
from comfy_api.latest import io


class LosslessCutV3(io.ComfyNode):
    """
    A V3 node to cut a video at the nearest keyframes, with an interactive UI.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="LosslessCutV3",
            display_name="🔥Lossless Cut (V3)",
            category="🔥FFmpeg/Editing",
            description="Interactive video cutter that cuts at keyframes for lossless output.",
            is_output_node=True,
            inputs=[
                io.String.Input("video", tooltip="Path to the input video file."),
                io.Float.Input(
                    "in_point",
                    default=0.0,
                    min=0.0,
                    step=0.01,
                    tooltip="Start time in seconds.",
                ),
                io.Float.Input(
                    "out_point",
                    default=-1.0,
                    min=-1.0,
                    step=0.01,
                    tooltip="End time in seconds (-1 = end of video).",
                ),
            ],
            outputs=[
                io.String.Output(
                    display_name="file_path",
                    tooltip="Path to the cut video file.",
                ),
            ],
            hidden=[io.Hidden.unique_id],
        )

    @classmethod
    def execute(
        cls,
        video,
        in_point,
        out_point,
    ) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        # Handle default out_point (-1 means end of video)
        if out_point <= 0:
            # We need to find the duration to know where the end is
            # Run ffprobe
            cmd = [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=duration",
                "-of",
                "csv=p=0",
                video,
            ]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                duration = float(result.stdout.strip())
                out_point = duration
            except Exception as e:
                # Fallback if ffprobe fails or duration missing: use a very large number
                # FFmpeg is smart enough to stop at EOF usually, but -to requires a timestamp.
                # If we don't know duration, we can omit -to ... but our logic below uses it.
                print(
                    f"[LosslessCut] Could not determine duration: {e}. using end of file logic."
                )
                out_point = None  # Special marker

        # Swap if in/out are reversed (sanity check)
        if out_point is not None and in_point > out_point:
            in_point, out_point = out_point, in_point

        filename = f"lossless_cut_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-ss",
            str(in_point),
        ]

        if out_point is not None:
            command.extend(["-to", str(out_point)])

        command.extend(
            [
                "-c",
                "copy",
                "-avoid_negative_ts",
                "make_zero",  # Good practice for cutting
                output_path,
            ]
        )

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg cut failed: {result.stderr}")

        return io.NodeOutput(output_path)
