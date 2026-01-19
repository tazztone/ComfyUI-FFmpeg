# Handle Subtitles (V3)

The **Handle Subtitles (V3)** node provides tools for managing subtitles: burning them into the video frames, adding them as a soft track, or extracting them.

## Inputs

| Input Name | Type | Description | Options | Default |
| :--- | :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - | - |
| **subtitle_file** | `STRING` | Path to the subtitle file (`.srt`, `.ass`, etc). | - | `subtitle.srt` |
| **action** | `COMBO` | The operation to perform. | `burn`, `add`, `extract` | - |
| **filename** | `STRING` | The name of the output file. | - | `video_with_subs.mp4` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **output** | `STRING` | The absolute path to the result file (video or subtitle). |

## Usage notes

- **Burn**: Hardcodes the text onto the video pixels (requres re-encoding).
- **Add**: Muxes the subtitle stream into the container (copy codec for video usually, `mov_text` for subs in MP4).
- **Extract**: Saves the first subtitle track of the video to the specified filename.
