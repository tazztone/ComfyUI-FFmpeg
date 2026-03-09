import os
import subprocess
from comfy_api.latest import io

class StreamOutputV3(io.ComfyNode):
    """
    A V3 node to stream a video file to an RTSP/RTMP destination.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="StreamOutputV3",
            display_name="🔥Stream Output (V3)",
            category="🔥FFmpeg/Output",
            inputs=[
                io.String.Input("video", tooltip="The video file to stream."),
                io.String.Input("stream_url", default="rtmp://localhost/live/stream", tooltip="Target RTMP/RTSP URL."),
                io.Combo.Input("preset", ["ultrafast", "veryfast", "medium"], default="veryfast"),
            ],
            outputs=[io.String.Output(tooltip="Status message.")],
        )

    @classmethod
    def execute(cls, video, stream_url, preset) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        # Basic streaming command
        # -re reads input at native frame rate
        cmd = [
            "ffmpeg", "-re", "-i", video,
            "-c:v", "libx264", "-preset", preset, "-tune", "zerolatency",
            "-c:a", "aac", "-f", "flv", stream_url
        ]

        try:
            # We don't want to block indefinitely for streaming usually, 
            # but ComfyUI execution is blocking. For now we run to completion.
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return io.NodeOutput(f"Streaming to {stream_url} completed.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg streaming failed: {e.stderr}")
