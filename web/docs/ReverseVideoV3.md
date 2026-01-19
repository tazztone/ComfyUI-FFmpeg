# Reverse Video (V3)

The **Reverse Video (V3)** node plays the video backwards.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **reverse_audio** | `BOOLEAN` | Whether to reverse the audio track as well. | `True` |
| **filename** | `STRING` | The name of the output video file. | `reversed_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the reversed video file. |

## Usage notes

- This process requires re-encoding and buffering the entire video in memory (RAM), so it can be slow and memory-intensive for long or high-resolution videos.
