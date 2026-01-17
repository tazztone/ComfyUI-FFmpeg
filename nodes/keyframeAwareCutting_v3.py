import os
import subprocess
import json
from datetime import datetime, timedelta
import folder_paths
from comfy_api.latest import io


class KeyframeTrimV3(io.ComfyNode):
    """
    A V3 node to cut a video at the nearest keyframes.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="KeyframeTrimV3",
            display_name="🔥Keyframe Trim (V3)",
            category="🔥FFmpeg/Advanced",
            inputs=[
                io.String.Input("video", tooltip="The video file."),
                io.String.Input(
                    "start_time", default="00:00:00", tooltip="Start time (HH:MM:SS)."
                ),
                io.String.Input(
                    "end_time", default="00:00:10", tooltip="End time (HH:MM:SS)."
                ),
                io.String.Input(
                    "filename",
                    default="keyframe_trimmed_video.mp4",
                    tooltip="Output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the trimmed video file."),
            ],
        )

    @staticmethod
    def _get_keyframes(video):
        command = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "frame=pkt_pts_time,pts_time,best_effort_timestamp_time,pict_type",
            "-of",
            "json",
            video,
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        frames = json.loads(result.stdout)["frames"]
        keyframes = []
        for f in frames:
            if f.get("pict_type") == "I":
                time_val = (
                    f.get("pkt_pts_time")
                    or f.get("pts_time")
                    or f.get("best_effort_timestamp_time")
                )
                if time_val:
                    keyframes.append(float(time_val))
        return keyframes

    @staticmethod
    def _find_nearest_keyframe(time_sec, keyframes):
        return min(keyframes, key=lambda x: abs(x - time_sec))

    @classmethod
    def execute(cls, video, start_time, end_time, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        def parse_time(t_str):
            try:
                return datetime.strptime(t_str, "%H:%M:%S")
            except ValueError:
                return datetime.strptime(t_str, "%H:%M:%S.%f")

        t_start = parse_time(start_time)
        start_sec = timedelta(
            hours=t_start.hour,
            minutes=t_start.minute,
            seconds=t_start.second,
            microseconds=t_start.microsecond,
        ).total_seconds()

        t_end = parse_time(end_time)
        end_sec = timedelta(
            hours=t_end.hour,
            minutes=t_end.minute,
            seconds=t_end.second,
            microseconds=t_end.microsecond,
        ).total_seconds()

        keyframes = cls._get_keyframes(video)
        start_keyframe = cls._find_nearest_keyframe(start_sec, keyframes)
        end_keyframe = cls._find_nearest_keyframe(end_sec, keyframes)

        if start_keyframe >= end_keyframe:
            raise ValueError("Start time must be before end time.")

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
        return io.NodeOutput(output_path)
