# Add Image Watermark (V3)

The **Add Image Watermark (V3)** node overlays an image (logo) onto a video at a specific pixel coordinate.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | `sample.mp4` |
| **width** | `INT` | The display width of the watermark in pixels (height is auto-scaled). | `100` |
| **position_x** | `INT` | X coordinate from the top-left. | `10` |
| **position_y** | `INT` | Y coordinate from the top-left. | `10` |
| **watermark_image_tensor** | `IMAGE` | (Optional) Watermark image input from another node. | - |
| **watermark_image** | `STRING` | (Optional) Absolute path to a watermark image file. | `logo.png` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the watermarked video file. |

## Usage notes

- You must provide either `watermark_image_tensor` OR `watermark_image`.
- The watermark supports transparency (alpha channel).
