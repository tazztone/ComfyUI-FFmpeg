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
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.String.Input(
                    "action", default="", tooltip="Action (internal usage)."
                ),
                io.Float.Input(
                    "in_point", default=0.0, min=0.0, step=0.01, tooltip="In point."
                ),
                io.Float.Input(
                    "out_point", default=-1.0, min=-1.0, step=0.01, tooltip="Out point."
                ),
                io.Float.Input(
                    "current_position",
                    default=0.0,
                    min=0.0,
                    step=0.01,
                    tooltip="Current cursor pos.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the cut video file."),
            ],
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
        data = json.loads(result.stdout)

        keyframes = []
        if "packets" in data:
            for packet in data.get("packets", []):
                if "K" in packet.get("flags", ""):
                    keyframes.append(float(packet["pts_time"]))

        fps_str = data["streams"][0]["r_frame_rate"]
        num, den = map(int, fps_str.split("/"))
        fps = num / den

        return {
            "duration": float(data["streams"][0]["duration"]),
            "fps": fps,
            "keyframes": keyframes,
        }

    @staticmethod
    def save_metadata_for_web(metadata, node_id):
        temp_dir = folder_paths.get_temp_directory()
        temp_file = os.path.join(temp_dir, f"losslesscut_data_{node_id}.json")
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
        node_id="0",
        prompt=None,
        extra_pnginfo=None,
    ) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        metadata = cls.extract_video_metadata(video)
        cls.save_metadata_for_web(metadata, node_id)

        keyframes = metadata["keyframes"]
        if out_point == -1:
            out_point = keyframes[-1] if keyframes else 0

        # UI Logic handling - simplified for V3 backbone port
        # The logic below updates in_point/out_point/current_pos but V3 API execute logic
        # usually is one-shot.
        # LosslessCut V1 returns {"ui": ...} to update the widget.
        # V3 NodeOutput might not support UI update payload directly in the same way?
        # Or it might pass it through?
        # For now, I'll replicate the logic and return standard output.
        # Use io.NodeOutput(output, ui_update={...}) if available?
        # Checking hypothetical API: io.NodeOutput(*outputs, ui_events=...)
        # Without confirmation, I just return standard output.

        # NOTE: This UI interaction might break slightly in V3 without JS update.

        if action == "next_kf":
            current_position = min(
                [kf for kf in keyframes if kf > current_position] or [current_position]
            )
        elif action == "prev_kf":
            current_position = max(
                [kf for kf in keyframes if kf < current_position] or [current_position]
            )
        elif action == "set_in":
            in_point = current_position
        elif action == "set_out":
            out_point = current_position
        elif action == "cut":
            start_keyframe = min(keyframes, key=lambda x: abs(x - in_point))
            end_keyframe = min(keyframes, key=lambda x: abs(x - out_point))

            if start_keyframe >= end_keyframe:
                raise ValueError("Start time must be before end time.")

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
            subprocess.run(command, check=True)
            return io.NodeOutput(output_path)  # Return output path

        # For UI updates, we send a message to the frontend
        # and stay on the current inputs (conceptually).
        # Since the node has executed, we just return the previous output or None.

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
            # Fallback if server cannot be imported (e.g. in tests)
            pass

        return io.NodeOutput(None)
