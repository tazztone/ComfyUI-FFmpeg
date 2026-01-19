# Lossless Cut (V3)
This node allows you to perform lossless video cutting using FFmpeg, preserving the original quality by cutting at keyframes.

## Features
*   **Lossless**: No re-encoding, so there is no quality loss and the process is extremely fast.
*   **Interactive UI**: Use the timeline to set IN and OUT points visually.
*   **Keyframe Snapping**: Automatically snaps cuts to the nearest keyframes to ensure valid video files.

## Parameters
*   **video**: The input video file path.
*   **action**: (Internal) Used by the UI to trigger actions like "next_kf" or "cut".
*   **in_point**: The start time of the cut (in seconds).
*   **out_point**: The end time of the cut (in seconds). Set to -1 to go to the end.
*   **current_position**: The current playback head position (in seconds).

## Outputs
*   **string**: The absolute file path to the cut video.
