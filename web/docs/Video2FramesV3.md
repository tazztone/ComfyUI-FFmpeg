# Video to Frames (V3)

The **Video to Frames (V3)** node extracts frames from a video and returns them as an image batch.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **max_width** | `INT` | Resize frames to this max width (preserving aspect ratio). 0 = Original. | `0` |
| **save_frames** | `BOOLEAN` | Whether to save the extracted frames to disk as PNGs. | `False` |
| **output_dir** | `STRING` | Sub-directory in the output folder to save frames (if enabled). | `frames` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **images** | `IMAGE` | The batch of extracted frames (IMAGE tensor). |
| **count** | `INT` | The total number of frames extracted. |

## Usage notes

- **Memory Warning**: Extracting all frames from a long video can easily consume all available system RAM. Use short clips or downscale (`max_width`) for testing.
