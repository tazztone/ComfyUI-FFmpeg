# Apply Filtergraph (V3)

The **Apply Filtergraph (V3)** node allows advanced users to apply raw, complex FFmpeg video filters.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **filtergraph** | `STRING` | The FFmpeg filter string options. | `vf hflip` |
| **filename** | `STRING` | The name of the output video file. | `filtered_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the processed video file. |

## Usage notes

- This node injects arguments directly into the FFmpeg command line.
- Do NOT include `-vf` or `-filter_complex` in the string; just the filter chain itself (e.g., `scale=1280:-1,format=yuv420p` or `-vf hflip`).
- **Warning**: Incorrect syntax will cause the FFmpeg process to fail. Use `shlex` splitting internally for safety.
