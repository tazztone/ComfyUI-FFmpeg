# Trim Video (V3)

The **Trim Video (V3)** node cuts a single segment from a video file based on start and end timestamps.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **start_time** | `STRING` | The start time of the clip (HH:MM:SS or HH:MM:SS.mmm). | `00:00:00` |
| **end_time** | `STRING` | The end time of the clip (HH:MM:SS or HH:MM:SS.mmm). | `00:00:10` |
| **filename** | `STRING` | The name of the output video file. | `trimmed_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the trimmed video file. |

## Usage notes

- This node uses stream copying (`-c copy`), so it is very fast and lossless.
- **Accuracy**: Cuts may not be frame-perfect because they must snap to the nearest keyframe before the start time. For precision cuts at keyframes, use **Keyframe Trim (V3)**.
