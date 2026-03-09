import os
import subprocess
import folder_paths
from comfy_api.latest import io

class FrameInterpolateV3(io.ComfyNode):
    """
    A V3 node to perform frame interpolation using FFmpeg's minterpolate filter.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="FrameInterpolateV3",
            display_name="🔥Frame Interpolate (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Int.Input("fps", default=60, min=1, tooltip="Target frame rate."),
                io.Combo.Input("mi_mode", ["mci", "blend", "dup"], default="mci", tooltip="Motion interpolation mode."),
                io.Combo.Input("mc_mode", ["obmc", "aobmc"], default="obmc", tooltip="Motion compensation mode."),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, fps, mi_mode, mc_mode) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        base, ext = os.path.splitext(os.path.basename(video))
        output_filename = f"{base}_interpolated_{fps}fps{ext}"
        output_path = os.path.join(folder_paths.get_output_directory(), output_filename)

        filter_str = f"minterpolate=fps={fps}:mi_mode={mi_mode}:mc_mode={mc_mode}"

        cmd = [
            "ffmpeg", "-y",
            "-i", video,
            "-vf", filter_str,
            "-c:a", "copy",
            output_path
        ]

        try:
            # This can take a long time
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return io.NodeOutput(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg frame interpolation failed: {e.stderr}")
