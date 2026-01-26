import os
import subprocess
import folder_paths
from comfy_api.latest import io


class HandleSubtitlesV3(io.ComfyNode):
    """
    A V3 node to handle subtitles (burn, add, extract).
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="HandleSubtitlesV3",
            display_name="🔥Handle Subtitles (V3)",
            category="🔥FFmpeg/Advanced",
            inputs=[
                io.String.Input("video", tooltip="Input video."),
                io.String.Input(
                    "subtitle_file", default="subtitle.srt", tooltip="Subtitle file.", optional=True
                ),
                io.Combo.Input(
                    "action", ["burn", "add", "extract"], tooltip="Action to perform."
                ),
                io.String.Input(
                    "filename",
                    default="video_with_subs.mp4",
                    tooltip="Output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output file."),
            ],
        )

    @classmethod
    def execute(cls, video, subtitle_file, action, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")
        if action != "extract":
            if not subtitle_file or not os.path.exists(subtitle_file):
                 # Fallback: Just copy video if subtitle file is missing for burn/add
                 print(f"Warning: Subtitle file not found or not provided for action '{action}'. Returning original video.")
                 output_path = os.path.join(folder_paths.get_output_directory(), filename)
                 command = ["ffmpeg", "-y", "-i", video, "-c", "copy", output_path]
                 subprocess.run(command, check=True)
                 return io.NodeOutput(output_path)

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        if action == "burn":
            command = [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-vf",
                f"subtitles={subtitle_file}",
                output_path,
            ]
        elif action == "add":
            command = [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-i",
                subtitle_file,
                "-c",
                "copy",
                "-c:s",
                "mov_text",
                output_path,
            ]
        elif action == "extract":
            command = ["ffmpeg", "-y", "-i", video, "-map", "0:s:0", output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            # Re-raise with stderr for visibility
            raise Exception(f"FFmpeg error: {e.stderr}")

        return io.NodeOutput(output_path)
