# Remux Video (V3)

The **Remux Video (V3)** node changes the container format of a video file (e.g., from `.mp4` to `.mkv`) without re-encoding the streams.

## Inputs

| Input Name | Type | Description | Options | Default |
| :--- | :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - | - |
| **container** | `COMBO` | The target container format. | `mp4`, `mkv`, `mov`, `webm` | `mp4` |
| **filename** | `STRING` | The base name of the output file. The extension is automatically adjusted. | - | `remuxed_video.mkv` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the remuxed video file. |

## Usage notes

- **Lossless**: Does not degrade quality because it copies the bitstreams directly.
- **Fast**: Much faster than conversion nodes that re-encode.
- Useful for fixing compatibility issues with players or editors that prefer specific containers.
