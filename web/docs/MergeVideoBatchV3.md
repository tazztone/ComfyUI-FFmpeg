# Merge Video Batch (V3)

The **Merge Video Batch (V3)** node takes a directory of video files and merges them into a single file.

## Inputs

| Input Name | Type | Description | Options | Default |
| :--- | :--- | :--- | :--- | :--- |
| **video_directory** | `STRING` | The absolute path to the directory containing `.mp4` files. | - | - |
| **resolution** | `COMBO` | The target output resolution. | `720p`, `1080p`, `4K` | `1080p` |
| **filename** | `STRING` | The name of the output video file. | - | `merged_video_batch.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the merged video file. |

## Usage notes

- Scans the directory for `.mp4` files.
- Files are sorted alphabetically before merging.
- All videos are standardized to the selected resolution.
