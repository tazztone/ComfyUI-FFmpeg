# Add Audio (V3)

The **Add Audio (V3)** node allows you to add an audio track to a video file, replacing any existing audio.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **audio** | `AUDIO` | The audio data to add (e.g., from `Load Audio` or `Extract Audio`). | - |
| **filename** | `STRING` | The name of the output video file. | `video_with_audio.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the processed video file. |

## Usage notes

- The audio is re-encoded to AAC.
- The video stream is copied (no re-encoding) for speed.
- The duration of the output is clamped to the shortest input (video or audio) using the `-shortest` flag.
