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
                io.String.Input("video1", tooltip="The first video file."),
                io.String.Input("video2", tooltip="The second video file.", optional=True),
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
        
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        if not video2 or not os.path.exists(video2):
             # Fallback: Just copy video1
             print("Warning: Video 2 not found or not provided for stitching. Returning Video 1.")
             command = ["ffmpeg", "-y", "-i", video1, "-c", "copy", output_path]
             subprocess.run(command, check=True)
             return io.NodeOutput(output_path)

        filter_complex = (
            "[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[v]"
            if layout == "horizontal"
            else "[0:v]pad=iw:ih*2[int];[int][1:v]overlay=0:H/2[v]"
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
