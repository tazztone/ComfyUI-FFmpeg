# Video Flip (V3)

The **Video Flip (V3)** node allows you to flip or mirror a video file either horizontally, vertically, or both. This is useful for correcting orientation issues or creating artistic effects.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **flip_type** | `COMBO` | The direction to flip the video. Options: `horizontal`, `vertical`, `both`. | `horizontal` |
| **filename** | `STRING` | The name of the output video file. | `flipped_video_v3.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the processed (flipped) video file. |

## Usage notes

- This node re-encodes the video stream to apply the flip effect.
- Audio tracks are preserved (copied) without modification.
