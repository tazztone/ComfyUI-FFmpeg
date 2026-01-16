import os
import subprocess
import folder_paths
from comfy_api.latest import io


class StitchVideosV3(io.ComfyNode):
    """
    A V3 node to stitch two videos together (horizontal/vertical).
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="StitchVideosV3",
            display_name="🔥Stitch Videos (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input(
                    "video1", default="video1.mp4", tooltip="The first video file."
                ),
                io.String.Input(
                    "video2", default="video2.mp4", tooltip="The second video file."
                ),
                io.Combo.Input(
                    "layout",
                    ["horizontal", "vertical"],
                    default="horizontal",
                    tooltip="Stitching layout.",
                ),
                io.Combo.Input(
                    "audio_source",
                    ["video1", "video2", "none"],
                    default="video1",
                    tooltip="Audio source.",
                ),
                io.String.Input(
                    "filename", default="stitched_video.mp4", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the stitched video file."),
            ],
        )

    @classmethod
    def execute(cls, video1, video2, layout, audio_source, filename) -> io.NodeOutput:
        if not os.path.exists(video1):
            raise FileNotFoundError(f"Video 1 not found: {video1}")
        if not os.path.exists(video2):
            raise FileNotFoundError(f"Video 2 not found: {video2}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        filter_complex = (
            f"[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[v]"
            if layout == "horizontal"
            else f"[0:v]pad=iw:ih*2[int];[int][1:v]overlay=0:H/2[v]"
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video1,
            "-i",
            video2,
            "-filter_complex",
            filter_complex,
        ]

        if audio_source != "none":
            audio_map = {"video1": "0:a", "video2": "1:a"}
            command.extend(["-map", "[v]", "-map", audio_map[audio_source]])
        else:
            command.extend(["-map", "[v]", "-an"])

        command.append(output_path)

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
