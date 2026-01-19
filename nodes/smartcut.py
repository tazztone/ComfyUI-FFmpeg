"""
Smart Cut helper module for frame-accurate video cutting.

Smart Cut re-encodes only the GOP boundaries to achieve frame-perfect cuts,
while copying the rest of the video stream losslessly.
"""

import os
import subprocess
import tempfile
from typing import List, Tuple, Optional


def get_keyframe_timestamps(video_path: str) -> List[float]:
    """
    Get all keyframe timestamps from a video file using ffprobe.

    Args:
        video_path: Path to the video file.

    Returns:
        List of keyframe timestamps in seconds, sorted.
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "packet=pts_time,flags",
        "-of",
        "csv=p=0",
        video_path,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        keyframes = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 2 and "K" in parts[1]:  # K flag indicates keyframe
                try:
                    keyframes.append(float(parts[0]))
                except ValueError:
                    continue
        return sorted(keyframes)
    except subprocess.CalledProcessError as e:
        print(f"[SmartCut] Failed to get keyframes: {e.stderr}")
        return []


def find_gop_boundaries(
    keyframes: List[float],
    in_point: float,
    out_point: float,
) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    Find the GOP boundaries around the cut points.

    Returns:
        Tuple of (prev_keyframe_before_in, next_keyframe_after_in,
                  prev_keyframe_before_out, next_keyframe_after_out)
    """
    if not keyframes:
        return None, None, None, None

    # Find keyframes around in_point
    prev_kf_in = None
    next_kf_in = None
    for kf in keyframes:
        if kf <= in_point:
            prev_kf_in = kf
        if kf > in_point and next_kf_in is None:
            next_kf_in = kf

    # Find keyframes around out_point
    prev_kf_out = None
    next_kf_out = None
    for kf in keyframes:
        if kf <= out_point:
            prev_kf_out = kf
        if kf > out_point and next_kf_out is None:
            next_kf_out = kf

    return prev_kf_in, next_kf_in, prev_kf_out, next_kf_out


def smart_cut(
    video_path: str,
    in_point: float,
    out_point: float,
    output_path: str,
    video_codec: str = "libx264",
    audio_codec: str = "aac",
    crf: int = 18,
) -> str:
    """
    Perform a smart cut that re-encodes only the GOP boundaries.

    This achieves frame-accurate cutting by:
    1. Re-encoding the intro section (from prev keyframe to in_point)
    2. Copying the middle section losslessly (from in_point's next keyframe to out_point's prev keyframe)
    3. Re-encoding the outro section (from out_point's prev keyframe to out_point)
    4. Concatenating all parts

    Args:
        video_path: Input video path.
        in_point: Start time in seconds.
        out_point: End time in seconds.
        output_path: Output video path.
        video_codec: Codec for re-encoded sections (default: libx264).
        audio_codec: Audio codec for re-encoded sections (default: aac).
        crf: Quality setting for re-encoding (default: 18, lower = better).

    Returns:
        Path to the output file.
    """
    keyframes = get_keyframe_timestamps(video_path)

    if not keyframes:
        # Fallback to simple cut if no keyframes found
        print("[SmartCut] No keyframes found, falling back to simple cut")
        return simple_cut(video_path, in_point, out_point, output_path)

    prev_kf_in, next_kf_in, prev_kf_out, next_kf_out = find_gop_boundaries(
        keyframes, in_point, out_point
    )

    # Check if cut points are already on keyframes
    tolerance = 0.01  # 10ms tolerance
    in_on_keyframe = any(abs(kf - in_point) < tolerance for kf in keyframes)
    out_on_keyframe = any(abs(kf - out_point) < tolerance for kf in keyframes)

    if in_on_keyframe and out_on_keyframe:
        # Perfect keyframe alignment, no re-encoding needed
        print("[SmartCut] Cut points align with keyframes, using simple cut")
        return simple_cut(video_path, in_point, out_point, output_path)

    # Create temporary directory for segment files
    with tempfile.TemporaryDirectory() as temp_dir:
        segments = []

        # Section 1: Intro (re-encode from prev_kf_in to in_point, then from in_point to next_kf_in)
        if not in_on_keyframe and prev_kf_in is not None and next_kf_in is not None:
            intro_path = os.path.join(temp_dir, "intro.mp4")
            # Re-encode from prev_kf_in, starting output from in_point
            reencode_section(
                video_path,
                prev_kf_in,  # Seek to prev keyframe for decoding
                next_kf_in,  # End at next keyframe
                in_point,  # Trim output to start from in_point
                next_kf_in,  # Trim output to end at next keyframe
                intro_path,
                video_codec,
                audio_codec,
                crf,
            )
            if os.path.exists(intro_path) and os.path.getsize(intro_path) > 0:
                segments.append(intro_path)

            # Middle section starts from next_kf_in
            middle_start = next_kf_in
        else:
            middle_start = in_point

        # Section 2: Middle (lossless copy)
        if not out_on_keyframe and prev_kf_out is not None:
            middle_end = prev_kf_out
        else:
            middle_end = out_point

        if middle_end > middle_start:
            middle_path = os.path.join(temp_dir, "middle.mp4")
            simple_cut(video_path, middle_start, middle_end, middle_path)
            if os.path.exists(middle_path) and os.path.getsize(middle_path) > 0:
                segments.append(middle_path)

        # Section 3: Outro (re-encode from prev_kf_out to out_point)
        if not out_on_keyframe and prev_kf_out is not None and prev_kf_out < out_point:
            outro_path = os.path.join(temp_dir, "outro.mp4")
            reencode_section(
                video_path,
                prev_kf_out,  # Seek to prev keyframe for decoding
                out_point + 1,  # Some buffer
                prev_kf_out,  # Trim output from prev keyframe
                out_point,  # Trim output to end at out_point
                outro_path,
                video_codec,
                audio_codec,
                crf,
            )
            if os.path.exists(outro_path) and os.path.getsize(outro_path) > 0:
                segments.append(outro_path)

        if not segments:
            print("[SmartCut] No segments created, falling back to simple cut")
            return simple_cut(video_path, in_point, out_point, output_path)

        if len(segments) == 1:
            # Only one segment, just copy it
            import shutil

            shutil.copy2(segments[0], output_path)
        else:
            # Concatenate segments
            concat_segments(segments, output_path)

    return output_path


def reencode_section(
    video_path: str,
    decode_start: float,
    decode_end: float,
    output_start: float,
    output_end: float,
    output_path: str,
    video_codec: str,
    audio_codec: str,
    crf: int,
):
    """Re-encode a section of video with precise trimming."""
    # Calculate the offset within the decoded section
    trim_start = output_start - decode_start
    duration = output_end - output_start

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(decode_start),
        "-i",
        video_path,
        "-ss",
        str(trim_start),
        "-t",
        str(duration),
        "-c:v",
        video_codec,
        "-crf",
        str(crf),
        "-preset",
        "fast",
        "-c:a",
        audio_codec,
        "-b:a",
        "192k",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[SmartCut] Re-encode failed: {result.stderr}")


def simple_cut(
    video_path: str,
    in_point: float,
    out_point: float,
    output_path: str,
) -> str:
    """Perform a simple lossless cut (keyframe-aligned)."""
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-ss",
        str(in_point),
        "-to",
        str(out_point),
        "-c",
        "copy",
        "-avoid_negative_ts",
        "make_zero",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg cut failed: {result.stderr}")

    return output_path


def concat_segments(segment_files: List[str], output_path: str):
    """Concatenate segment files using FFmpeg concat demuxer."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for seg in segment_files:
            f.write(f"file '{seg}'\n")
        concat_path = f.name

    try:
        cmd = [
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
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg concat failed: {result.stderr}")
    finally:
        os.unlink(concat_path)
