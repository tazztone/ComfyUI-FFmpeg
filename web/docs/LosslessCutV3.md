# Lossless Cut (V3)
This node provides an advanced interactive interface for cutting videos. It supports lossless cutting (keyframe-aligned) and smart cutting (frame-accurate with partial re-encoding), along with multiple segments and stream selection.

## Features
*   **Interactive UI**: Timeline with zoom, playback, and segment management.
*   **Multi-Segment Editing**: Define multiple cut zones, delete with a click, and export as separate clips or a single merged file.
*   **Smart Cut**: Frame-accurate cutting that re-encodes only the boundaries (GOP) while copying the rest losslessly.
*   **Stream Selection**: Choose which video, audio, and subtitle tracks to keep.
*   **Screenshot Export**: Capture high-quality frames directly from the timeline to ComfyUI Image outputs.

## Parameters
*   **video**: The input video file path.
*   **export_individual_clips**: If true, exports each segment as a separate file. If false, merges them into one.
*   **output_format**: Container format for the output (mp4, mkv, mov, webm).
*   **Stream Selection**:
    *   `include_video`, `include_audio`, `include_subtitles`: Toggle streams.
    *   `audio_track_index`: Select specific audio track (-1 for all).
*   **preserve_metadata**: Control metadata copying (all, none, chapters_only).

## UI Controls
*   **IN/OUT**: Set start and end points for segments.
*   **CUT**: Execute the cut operation.
*   **📷**: Export the current frame as an image (outputs to `screenshot` socket).
*   **🔒 KF / 🧠 SC**: Toggle between Keyframe Lock (Lossless) and Smart Cut (Frame-Accurate).

## Outputs
*   **file_path**: The absolute file path(s) to the cut video(s).
*   **screenshot**: ComfyUI IMAGE tensor of the captured screenshot.
