# Analyze Streams (V3)

The **Analyze Streams (V3)** node probes a video file and returns detailed technical information about its streams (video, audio, subtitles).

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the video file to analyze. | - |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **info** | `STRING` | A JSON-formatted string containing the probe data. |

## Usage notes

- Uses `ffprobe -show_streams`.
- Useful for debugging or inspecting codec details, resolution, bitrate, etc.
- You can pipe the output to a text display node to read it in ComfyUI.
