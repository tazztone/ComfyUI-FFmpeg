import os
import subprocess
import json
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
                io.String.Input(
                    "action",
                    default="",
                    tooltip="Internal action (set by UI buttons).",
                ),
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
                io.Float.Input(
                    "current_position",
                    default=0.0,
                    min=0.0,
                    step=0.01,
                    tooltip="Current playhead position (set by UI).",
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

    @staticmethod
    def extract_video_metadata(video_path):
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=duration,r_frame_rate",
            "-show_entries",
            "packet=pts_time,flags",
            "-of",
            "json",
            video_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffprobe failed: {result.stderr}")
        data = json.loads(result.stdout)

        keyframes = []
        if "packets" in data:
            for packet in data.get("packets", []):
                if "K" in packet.get("flags", ""):
                    keyframes.append(float(packet["pts_time"]))

        if not data.get("streams"):
            raise RuntimeError("No video stream found in file.")

        fps_str = data["streams"][0]["r_frame_rate"]
        num, den = map(int, fps_str.split("/"))
        fps = num / den

        return {
            "duration": float(data["streams"][0].get("duration", 0)),
            "fps": fps,
            "keyframes": keyframes,
        }

    @staticmethod
    def save_metadata_for_web(metadata, node_id):
        output_dir = folder_paths.get_output_directory()
        temp_file = os.path.join(output_dir, f"losslesscut_data_{node_id}.json")
        with open(temp_file, "w") as f:
            json.dump(metadata, f, indent=2)

    @classmethod
    def execute(
        cls,
        video,
        action,
        in_point,
        out_point,
        current_position,
    ) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        node_id = cls.hidden.unique_id

        # Debug logging to console
        print(
            f"[LosslessCut] Execute: node_id={node_id}, action='{action}', in={in_point:.2f}, out={out_point:.2f}, pos={current_position:.2f}"
        )

        metadata = cls.extract_video_metadata(video)
        cls.save_metadata_for_web(metadata, node_id)

        keyframes = metadata["keyframes"]
        duration = metadata["duration"]

        # Handle default out_point (-1 means end of video)
        if out_point < 0:
            out_point = duration

        # Sync UI logic for "interactive" usage
        if action == "next_kf":
            next_kfs = [kf for kf in keyframes if kf > current_position]
            current_position = min(next_kfs) if next_kfs else current_position
        elif action == "prev_kf":
            prev_kfs = [kf for kf in keyframes if kf < current_position]
            current_position = max(prev_kfs) if prev_kfs else current_position
        elif action == "set_in":
            in_point = current_position
        elif action == "set_out":
            out_point = current_position
        elif action == "cut":
            # Swap if in/out are reversed
            if in_point > out_point:
                in_point, out_point = out_point, in_point

            # Find nearest keyframes
            start_keyframe = (
                min(keyframes, key=lambda x: abs(x - in_point))
                if keyframes
                else in_point
            )
            end_keyframe = (
                min(keyframes, key=lambda x: abs(x - out_point))
                if keyframes
                else out_point
            )

            # Swap if keyframes are reversed
            if start_keyframe > end_keyframe:
                start_keyframe, end_keyframe = end_keyframe, start_keyframe

            if start_keyframe == end_keyframe:
                raise ValueError(
                    f"IN and OUT points are the same keyframe ({start_keyframe:.2f}s). "
                    "Select a wider range."
                )

            filename = f"lossless_cut_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            output_path = os.path.join(folder_paths.get_output_directory(), filename)

            command = [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-ss",
                str(start_keyframe),
                "-to",
                str(end_keyframe),
                "-c",
                "copy",
                output_path,
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg cut failed: {result.stderr}")

            return io.NodeOutput(output_path)

        # Notify frontend of updated state
        try:
            from server import PromptServer

            PromptServer.instance.send_sync(
                "comfyui-ffmpeg-losslesscut-update",
                {
                    "node_id": node_id,
                    "in_point": in_point,
                    "out_point": out_point,
                    "current_position": current_position,
                },
            )
        except ImportError:
            pass

        return io.NodeOutput(None)
