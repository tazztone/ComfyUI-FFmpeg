# Generic FFmpeg (V3)

The **Generic FFmpeg (V3)** node executes a raw, custom FFmpeg command on an input video.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **ffmpeg_command** | `STRING` | The arguments to pass to FFmpeg (inserted after input, before output). | `-vf hflip` |
| **filename** | `STRING` | The name of the output video file. | `generic_output.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the processed video file. |

## Usage notes

- This node constructs the command: `ffmpeg -y -i [video] [ffmpeg_command] [output_path]`.
- Use this for any FFmpeg functionality not covered by dedicated nodes.
- **Power User Tool**: Requires knowledge of FFmpeg syntax.
