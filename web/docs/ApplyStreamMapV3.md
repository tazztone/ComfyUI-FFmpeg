# Apply Stream Map (V3)

The **Apply Stream Map (V3)** node allows you to selectively copy or re-order streams using FFmpeg's `-map` option.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **stream_map** | `STRING` | The mapping arguments (e.g., `-map 0:v -map 0:a:0`). | `-map 0:v -map 0:a:0?` |
| **filename** | `STRING` | The name of the output video file. | `mapped_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the processed video file. |

## Usage notes

- Uses stream copying (`-c copy`), so no re-encoding occurs.
- **Syntax**: `0:v` selects the video stream from the first input. `0:a:0` selects the first audio stream. `?` makes the selection optional (avoids error if missing).
- Useful for removing specific tracks or extracting a specific audio stream.
