# Picture In Picture (V3)

The **Picture In Picture (V3)** node overlays a foreground video or image onto a background video.

## Inputs

| Input Name | Type | Description | Options | Default |
| :--- | :--- | :--- | :--- | :--- |
| **background_video** | `STRING` | The absolute path to the background video file. | - | - |
| **position** | `COMBO` | The corner to place the foreground overlay. | `top_left`, `top_right`, `bottom_left`, `bottom_right`, `center` | - |
| **scale** | `FLOAT` | The size of the foreground relative to the background (0.1 to 1.0). | - | `0.5` |
| **audio_source** | `COMBO` | Audio track to use. | `background`, `foreground`, `none` | `background` |
| **filename** | `STRING` | The name of the output video file. | - | `pip_video.mp4` |
| **foreground_video** | `STRING` | (Optional) Path to foreground video. | - | - |
| **foreground_image** | `IMAGE` | (Optional) Foreground image tensor. | - | - |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the composed video file. |

## Usage notes

- You must provide either `foreground_video` OR `foreground_image`.
- If using an image, `audio_source` set to `foreground` will be ignored.
