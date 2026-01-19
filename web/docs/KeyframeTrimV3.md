# Keyframe Trim (V3)

The **Keyframe Trim (V3)** node cuts a video segment specifically at keyframe boundaries.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **start_time** | `STRING` | Approximate start time (HH:MM:SS). The node will snap to the nearest keyframe. | `00:00:00` |
| **end_time** | `STRING` | Approximate end time (HH:MM:SS). The node will snap to the nearest keyframe. | `00:00:10` |
| **filename** | `STRING` | The name of the output video file. | `keyframe_trimmed_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the trimmed video file. |

## Usage notes

- **Precision**: Analyzes the video bitstream to find exact keyframe timestamps (`I-frames`).
- **Lossless**: Uses stream copying (`-c copy`), ensuring no quality loss.
- Ideal for making clean cuts that don't produce visual glitches or "smearing" at the start of playback.
