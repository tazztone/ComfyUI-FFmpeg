# Split Video (V3)

The **Split Video (V3)** node divides a long video into multiple smaller segments of equal duration.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **segment_duration** | `INT` | The duration of each segment in seconds. | `10` |
| **output_prefix** | `STRING` | The prefix for the output filenames (e.g., `segment_` -> `segment_001.mp4`). | `segment_` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The **directory** containing the generated segment files. |

## Usage notes

- Matches the functionality of `ffmpeg -f segment`.
- Uses stream copying (`-c copy`) for speed.
- Useful for batch processing large videos (e.g., splitting a movie into scenes).
