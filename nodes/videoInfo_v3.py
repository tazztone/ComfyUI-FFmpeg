import os
import subprocess
import json
from comfy_api.latest import io

class VideoInfoV3(io.ComfyNode):
    """
    A V3 node to expose video metadata (fps, frame count, duration, size) as outputs.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="VideoInfoV3",
            display_name="🔥Video Info (V3)",
            category="🔥FFmpeg/Metadata",
            inputs=[
                io.String.Input("video", tooltip="The video file to analyze."),
            ],
            outputs=[
                io.Float.Output(tooltip="Frames per second."),
                io.Int.Output(tooltip="Total frame count."),
                io.Float.Output(tooltip="Duration in seconds."),
                io.Int.Output(tooltip="Width in pixels."),
                io.Int.Output(tooltip="Height in pixels."),
            ],
        )

    @classmethod
    def execute(cls, video) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        command = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration",
            "-of", "json",
            video
        ]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            data = json.loads(result.stdout)
           
            if "streams" not in data or not data["streams"]:
                raise RuntimeError(f"No video streams found in {video}")
               
            stream = data["streams"][0]

            # Parse FPS
            fps_str = stream.get("r_frame_rate", "0/1")
            if "/" in fps_str:
                num, den = map(int, fps_str.split("/"))
                fps = num / den if den != 0 else 0.0
            else:
                fps = float(fps_str)

            frame_count = int(stream.get("nb_frames", 0))
            duration = float(stream.get("duration", 0.0))
            width = int(stream.get("width", 0))
            height = int(stream.get("height", 0))

            return io.NodeOutput(fps, frame_count, duration, width, height)
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFprobe error: {e.stderr}")
        except Exception as e:
            raise Exception(f"Error parsing video info: {str(e)}")
