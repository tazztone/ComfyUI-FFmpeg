import os
import subprocess
import re
import tempfile
from comfy_api.latest import io

class SceneDetectV3(io.ComfyNode):
    """
    A V3 node to detect scene cuts in a video.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="SceneDetectV3",
            display_name="🔥Scene Detect (V3)",
            category="🔥FFmpeg/Analysis",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Float.Input("threshold", default=0.4, min=0.0, max=1.0, tooltip="Scene detection threshold (0.0 to 1.0)."),
            ],
            outputs=[
                io.String.Output(tooltip="List of scene cut timestamps (comma separated)."),
                io.String.Output(tooltip="List of scene cut frame indices (comma separated)."),
            ],
        )

    @classmethod
    def execute(cls, video, threshold) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        temp_dir = tempfile.mkdtemp()
        meta_tmp = os.path.join(temp_dir, "metadata.txt")

        # FFmpeg command to detect scenes and output metadata to a file
        cmd = [
            "ffmpeg", "-i", video,
            "-vf", f"select=gt(scene\\,{threshold}),metadata=print:file={meta_tmp}",
            "-f", "null", "-"
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
           
            if not os.path.exists(meta_tmp):
                return io.NodeOutput("", "")

            with open(meta_tmp, "r") as f:
                output = f.read()
          
            # Parse output for pts_time and frame indices
            # Example output:
            # [Parsed_metadata_1 @ 0x...] pts:1500 pts_time:1.5
            # [Parsed_metadata_1 @ 0x...] frame:37 pts:1500 pts_time:1.5
          
            timestamps = []
            indices = []
          
            for line in output.split("\n"):
                # Look for pts_time
                time_match = re.search(r"pts_time:([\d\.]+)", line)
                if time_match:
                    timestamps.append(time_match.group(1))
              
                # Look for frame index
                index_match = re.search(r"frame:(\d+)", line)
                if index_match:
                    indices.append(index_match.group(1))
          
            # Deduplicate and sort (ffmpeg might print multiple lines for same event)
            timestamps = sorted(list(set(timestamps)), key=float)
            indices = sorted(list(set(indices)), key=int)
          
            return io.NodeOutput(",".join(timestamps), ",".join(indices))
          
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg scene detection failed: {e.stderr}")
