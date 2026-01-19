# Video Transition (V3)

The **Video Transition (V3)** node creates a smooth visual transition between two videos using FFmpeg's XFade filter.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video1** | `STRING` | The first video file (outgoing). | - |
| **video2** | `STRING` | The second video file (incoming). | - |
| **transition** | `COMBO` | The transition effect type (e.g., `fade`, `wipeleft`, `circleopen`). | `fade` |
| **duration** | `FLOAT` | Length of the transition in seconds. | `1.0` |
| **offset** | `FLOAT` | The timestamp in Video 1 where the transition begins. | `2.0` |
| **filename** | `STRING` | The name of the output video file. | `transition_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the output video file. |

## Usage notes

- **Validation**: Ensure `offset` + `duration` does not exceed the length of Video 1.
- Audio is cross-faded (`acrossfade`) concurrently with the video transition.
