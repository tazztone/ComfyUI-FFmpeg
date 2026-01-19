# Frames to Video (V3)

The **Frames to Video (V3)** node compiles a batch of images into a video file using high-efficiency codecs.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **images** | `IMAGE` | The batch of images to encode. | - |
| **fps** | `INT` | Frame rate of the output video. | `24` |
| **codec** | `COMBO` | The video codec to use (CPU or NVIDIA GPU). | `h264_cpu` |
| **crf** | `INT` | Quality factor (0-51). Lower is better quality. | `23` |
| **preset** | `COMBO` | Encoding speed/compression efficiency trade-off. | `medium` |
| **filename** | `STRING` | The name of the output video file. | `output.mp4` |
| **audio** | `AUDIO` | (Optional) Audio track to mux with the video. | - |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the generated video file. |

## Usage notes

- **Codecs**:
  - `h264_cpu` / `h265_cpu`: Software encoding (high compatibility / efficiency).
  - `h264_nvidia` / `h265_nvidia`: Hardware encoding (fast, requires NVIDIA GPU).
