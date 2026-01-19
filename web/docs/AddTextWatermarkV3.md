# Add Text Watermark (V3)

The **Add Text Watermark (V3)** node overlays a text string onto a video file at a specified position, using customizable fonts and colors.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **text** | `STRING` | The text content of the watermark. | `ComfyUI` |
| **font_size** | `INT` | The size of the watermark text. | `48` |
| **font_color** | `STRING` | The color of the text (e.g., `white`, `black`, `red`, `#FF0000`). | `white` |
| **position_x** | `INT` | The X-coordinte (horizontal) for the text overlay. | `10` |
| **position_y** | `INT` | The Y-coordinate (vertical) for the text overlay. | `10` |
| **font_file** | `COMBO` | The font file to use. Place custom `.ttf` files in the `fonts/` directory. | `default` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the processed video file with the watermark. |

## Font Management

- The node includes a standard set of fonts.
- To add custom fonts, place `.ttf` files in the `fonts/` directory at the root of the **ComfyUI-FFmpeg** package.
- You must restart ComfyUI for new fonts to appear in the `font_file` dropdown.
