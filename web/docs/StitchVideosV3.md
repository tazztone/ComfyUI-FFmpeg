# Stitch Videos (V3)

The **Stitch Videos (V3)** node combines two videos spatially, placing them either side-by-side or stacking them vertically.

## Inputs

| Input Name | Type | Description | Options | Default |
| :--- | :--- | :--- | :--- | :--- |
| **video1** | `STRING` | The first video file (Left or Top). | - | - |
| **video2** | `STRING` | The second video file (Right or Bottom). | - | - |
| **layout** | `COMBO` | The layout configuration. | `horizontal`, `vertical` | `horizontal` |
| **audio_source** | `COMBO` | Which video's audio to use for the output. | `video1`, `video2`, `none` | `video1` |
| **filename** | `STRING` | The name of the output video file. | - | `stitched_video.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the stitched video file. |

## Usage notes

- **Horizontal**: `video1` is on the left, `video2` is on the right.
- **Vertical**: `video1` is on the top, `video2` is on the bottom.
- The node pads the canvas to fit both videos.
