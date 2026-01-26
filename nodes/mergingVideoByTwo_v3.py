import os
import subprocess
import folder_paths
from comfy_api.latest import io


class MergeVideosV3(io.ComfyNode):
    """
    A V3 node to merge two video files.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="MergeVideosV3",
            display_name="🔥Merge Videos (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input("video1", tooltip="The first video file."),
                io.String.Input("video2", tooltip="The second video file.", optional=True),
                io.Combo.Input(
                    "resolution",
                    ["720p", "1080p", "4K"],
                    default="1080p",
                    tooltip="Output resolution.",
                ),
                io.String.Input(
                    "filename", default="merged_video.mp4", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the merged video file."),
            ],
        )

    @classmethod
    def execute(cls, video1, video2, resolution, filename) -> io.NodeOutput:
        if not os.path.exists(video1):
            raise FileNotFoundError(f"Video 1 not found: {video1}")
        
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        if not video2 or not os.path.exists(video2):
             # Fallback: Just copy video1
             print("Warning: Video 2 not found or not provided for merging. Returning Video 1.")
             command = ["ffmpeg", "-y", "-i", video1, "-c", "copy", output_path]
             subprocess.run(command, check=True)
             return io.NodeOutput(output_path)

        resolution_map = {
            "720p": "1280:720",
            "1080p": "1920:1080",
            "4K": "3840:2160",
        }

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video1,
            "-i",
            video2,
            "-filter_complex",
            f"[0:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v0];"
            f"[1:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];"
            f"[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            output_path,
        ]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
