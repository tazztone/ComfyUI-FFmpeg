# Merge Videos (V3)

The **Merge Videos (V3)** node concatenates two video files into a single continuous video.

## Inputs

| Input Name | Type | Description | Options | Default |
| :--- | :--- | :--- | :--- | :--- |
| **video1** | `STRING` | The absolute path to the first video file. | - | - |
| **video2** | `STRING` | The absolute path to the second video file. | - | - |
| **resolution** | `COMBO` | The target output resolution. Both inputs are scaled to fit. | `720p`, `1080p`, `4K` | `1080p` |
| **filename** | `STRING` | The name of the output video file. | - | `merged_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the merged video file. |

## Usage notes

- Both input videos are resized to match the selected resolution (letterboxed if aspect ratio differs).
- Videos are played sequentially (video 1, then video 2).
- Audio is also concatenated.
