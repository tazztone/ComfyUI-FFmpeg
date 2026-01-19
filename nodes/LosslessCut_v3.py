import os
import subprocess
import json
import tempfile
import numpy as np
import torch
from PIL import Image
from datetime import datetime
import folder_paths
from comfy_api.latest import io
from . import smartcut


class LosslessCutV3(io.ComfyNode):
    """
    A V3 node to cut a video at the nearest keyframes, with an interactive UI.
    Supports stream selection, metadata control, screenshot export, and multiple segments.
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
                io.Float.Input(
                    "in_point",
                    default=0.0,
                    min=0.0,
                    step=0.01,
                    tooltip="Start time in seconds (used if segments is empty).",
                ),
                io.Float.Input(
                    "out_point",
                    default=-1.0,
                    min=-1.0,
                    step=0.01,
                    tooltip="End time in seconds (-1 = end of video, used if segments is empty).",
                ),
                io.Boolean.Input(
                    "export_individual_clips",
                    default=True,
                    tooltip="If true, export each segment as individual clip. If false, merge all segments into one.",
                ),
                # Output Format
                io.Combo.Input(
                    "output_format",
                    options=["mp4", "mkv", "mov", "webm"],
                    default="mp4",
                    tooltip="Output container format.",
                ),
                # Stream Selection
                io.Boolean.Input(
                    "include_video",
                    default=True,
                    tooltip="Include video stream in output.",
                ),
                io.Boolean.Input(
                    "include_audio",
                    default=True,
                    tooltip="Include audio stream(s) in output.",
                ),
                io.Int.Input(
                    "audio_track_index",
                    default=-1,
                    min=-1,
                    max=10,
                    tooltip="Audio track index to include (-1 = all tracks).",
                ),
                io.Boolean.Input(
                    "include_subtitles",
                    default=False,
                    tooltip="Include subtitle stream(s) in output.",
                ),
                # Metadata Preservation
                io.Combo.Input(
                    "preserve_metadata",
                    options=["all", "none", "chapters_only"],
                    default="all",
                    tooltip="Control metadata preservation in output.",
                ),
                # UI-managed inputs (synced from JavaScript)
                io.String.Input(
                    "segments",
                    default="",
                    multiline=True,
                    tooltip="JSON array of segments (managed by UI).",
                ),
                io.Boolean.Input(
                    "export_screenshot",
                    default=False,
                    tooltip="Export a screenshot (triggered by UI button).",
                ),
                io.Float.Input(
                    "screenshot_time",
                    default=0.0,
                    min=0.0,
                    step=0.01,
                    tooltip="Time in seconds to capture screenshot (set by UI).",
                ),
                io.Boolean.Input(
                    "smart_cut",
                    default=False,
                    tooltip="Enable smart cut (auto-enabled when keyframe lock is off).",
                ),
            ],
            outputs=[
                io.String.Output(
                    display_name="file_path",
                    tooltip="Path to the cut video file (or comma-separated paths if multiple).",
                ),
                io.Image.Output(
                    display_name="screenshot",
                    tooltip="Screenshot image (if captured via 📷 button).",
                ),
            ],
            hidden=[io.Hidden.unique_id],
        )

    @classmethod
    def _build_common_args(
        cls,
        include_video,
        include_audio,
        audio_track_index,
        include_subtitles,
        preserve_metadata,
    ):
        """Build common FFmpeg arguments for stream mapping and metadata."""
        map_args = []
        if include_video:
            map_args.extend(["-map", "0:v:0?"])
        if include_audio:
            if audio_track_index >= 0:
                map_args.extend(["-map", f"0:a:{audio_track_index}?"])
            else:
                map_args.extend(["-map", "0:a?"])
        if include_subtitles:
            map_args.extend(["-map", "0:s?"])

        if not map_args:
            map_args = ["-map", "0"]

        metadata_args = []
        if preserve_metadata == "all":
            metadata_args = ["-map_metadata", "0"]
        elif preserve_metadata == "none":
            metadata_args = ["-map_metadata", "-1"]
        elif preserve_metadata == "chapters_only":
            metadata_args = ["-map_metadata", "-1", "-map_chapters", "0"]

        return map_args, metadata_args

    @classmethod
    def _cut_segment(
        cls,
        video,
        in_point,
        out_point,
        output_path,
        map_args,
        metadata_args,
    ):
        """Cut a single segment from the video."""
        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-ss",
            str(in_point),
        ]

        if out_point is not None:
            command.extend(["-to", str(out_point)])

        command.extend(map_args)
        command.extend(metadata_args)
        command.extend(
            [
                "-c",
                "copy",
                "-avoid_negative_ts",
                "make_zero",
                output_path,
            ]
        )

        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg cut failed: {result.stderr}")

        return output_path

    @classmethod
    def _merge_segments(cls, segment_files, output_path):
        """Merge multiple segment files using FFmpeg concat demuxer."""
        # Create concat file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as concat_file:
            for f in segment_files:
                concat_file.write(f"file '{f}'\n")
            concat_path = concat_file.name

        try:
            command = [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                concat_path,
                "-c",
                "copy",
                output_path,
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg merge failed: {result.stderr}")
        finally:
            # Cleanup concat file
            os.unlink(concat_path)

        return output_path

    @classmethod
    def execute(
        cls,
        video,
        in_point,
        out_point,
        export_individual_clips=True,
        output_format="mp4",
        include_video=True,
        include_audio=True,
        audio_track_index=-1,
        include_subtitles=False,
        preserve_metadata="all",
        segments="",
        export_screenshot=False,
        screenshot_time=0.0,
        smart_cut=False,
    ) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_dir = folder_paths.get_output_directory()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        screenshot_tensor = None

        # Export screenshot if requested (screenshot-only mode)
        if export_screenshot:
            screenshot_path = os.path.join(output_dir, f"screenshot_{timestamp}.jpg")
            screenshot_cmd = [
                "ffmpeg",
                "-y",
                "-ss",
                str(screenshot_time),
                "-i",
                video,
                "-vframes",
                "1",
                "-q:v",
                "2",
                screenshot_path,
            ]
            result = subprocess.run(screenshot_cmd, capture_output=True, text=True)
            if result.returncode == 0 and os.path.exists(screenshot_path):
                # Load image and convert to torch tensor for ComfyUI
                try:
                    img = Image.open(screenshot_path).convert("RGB")
                    img_array = np.array(img).astype(np.float32) / 255.0
                    # Convert to torch tensor with batch dimension [B, H, W, C]
                    screenshot_tensor = torch.from_numpy(img_array).unsqueeze(0)
                    print(f"[LosslessCut] Screenshot saved: {screenshot_path}")
                except Exception as e:
                    print(f"[LosslessCut] Failed to load screenshot as tensor: {e}")
            else:
                print(f"[LosslessCut] Screenshot export failed: {result.stderr}")

            # Return early - screenshot only, no video cut
            return io.NodeOutput("", screenshot_tensor)

        # Parse segments JSON or fall back to in_point/out_point
        segment_list = []
        if segments and segments.strip():
            try:
                segment_list = json.loads(segments)
                if not isinstance(segment_list, list):
                    segment_list = []
            except json.JSONDecodeError:
                print(f"[LosslessCut] Invalid segments JSON, using in_point/out_point")
                segment_list = []

        # If no valid segments, use single in_point/out_point
        if not segment_list:
            # Handle default out_point (-1 means end of video)
            if out_point <= 0:
                cmd = [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=duration",
                    "-of",
                    "csv=p=0",
                    video,
                ]
                try:
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, check=True
                    )
                    duration = float(result.stdout.strip())
                    out_point = duration
                except Exception as e:
                    print(
                        f"[LosslessCut] Could not determine duration: {e}. using end of file logic."
                    )
                    out_point = None

            # Swap if in/out are reversed
            if out_point is not None and in_point > out_point:
                in_point, out_point = out_point, in_point

            segment_list = [{"in": in_point, "out": out_point}]

        # Build common args
        map_args, metadata_args = cls._build_common_args(
            include_video,
            include_audio,
            audio_track_index,
            include_subtitles,
            preserve_metadata,
        )

        # Cut each segment
        segment_files = []
        for i, seg in enumerate(segment_list):
            seg_in = float(seg.get("in", 0))
            seg_out = seg.get("out")
            if seg_out is not None:
                seg_out = float(seg_out)

            seg_filename = f"lossless_cut_{timestamp}_seg{i:03d}.{output_format}"
            seg_path = os.path.join(output_dir, seg_filename)

            if smart_cut and seg_out is not None:
                # Use smart cut for frame-accurate cutting
                try:
                    smartcut.smart_cut(video, seg_in, seg_out, seg_path)
                    print(f"[LosslessCut] Smart cut segment {i} completed")
                except Exception as e:
                    print(
                        f"[LosslessCut] Smart cut failed, falling back to lossless: {e}"
                    )
                    cls._cut_segment(
                        video, seg_in, seg_out, seg_path, map_args, metadata_args
                    )
            else:
                cls._cut_segment(
                    video, seg_in, seg_out, seg_path, map_args, metadata_args
                )

            segment_files.append(seg_path)

        # Merge or return individual files
        # Note: export_individual_clips=True means DON'T merge, so invert
        merge_segments = not export_individual_clips
        if len(segment_files) == 1:
            output_path = segment_files[0]
        elif merge_segments:
            final_filename = f"lossless_cut_{timestamp}_merged.{output_format}"
            final_path = os.path.join(output_dir, final_filename)
            cls._merge_segments(segment_files, final_path)

            # Clean up individual segment files
            for f in segment_files:
                try:
                    os.unlink(f)
                except Exception:
                    pass

            output_path = final_path
        else:
            # Return comma-separated list of paths
            output_path = ",".join(segment_files)

        # No screenshot in video cut mode
        return io.NodeOutput(output_path, None)
