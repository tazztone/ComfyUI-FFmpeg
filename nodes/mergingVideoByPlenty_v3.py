import os
import subprocess
import folder_paths
from comfy_api.latest import io


class MergeVideoBatchV3(io.ComfyNode):
    """
    A V3 node to merge multiple video files from a directory.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="MergeVideoBatchV3",
            display_name="🔥Merge Video Batch (V3)",
            category="🔥FFmpeg/Editing",
            inputs=[
                io.String.Input(
                    "video_directory",
                    tooltip="Directory containing video files.",
                ),
                io.Combo.Input(
                    "resolution",
                    ["720p", "1080p", "4K"],
                    default="1080p",
                    tooltip="Output resolution.",
                ),
                io.String.Input(
                    "filename",
                    default="merged_video_batch.mp4",
                    tooltip="Output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the merged video file."),
            ],
        )

    @classmethod
    def execute(cls, video_directory, resolution, filename) -> io.NodeOutput:
        if not os.path.isdir(video_directory):
            raise FileNotFoundError(f"Video directory not found: {video_directory}")

        videos = sorted(
            [
                os.path.join(video_directory, f)
                for f in os.listdir(video_directory)
                if f.endswith(".mp4")
            ]
        )
        if not videos:
            raise ValueError("No MP4 videos found in the directory.")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        resolution_map = {
            "720p": "1280:720",
            "1080p": "1920:1080",
            "4K": "3840:2160",
        }

        inputs = [item for video in videos for item in ["-i", video]]
        filter_complex = "".join(
            [
                f"[{i}:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}];"
                for i in range(len(videos))
            ]
        )
        filter_complex += (
            "".join([f"[v{i}][{i}:a?]" for i in range(len(videos))])
            + f"concat=n={len(videos)}:v=1:a=1[v][a]"
        )

        command = [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",
            "-map",
            "[a]",
            output_path,
        ]

        subprocess.run(command, check=True)
        return io.NodeOutput(output_path)
