# Extract Audio (V3)

The **Extract Audio (V3)** node extracts the audio track from a video file.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **video** | `STRING` | The absolute path to the input video file. | - |
| **filename** | `STRING` | The name of the output audio file. | `extracted_audio.wav` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **audio** | `AUDIO` | The extracted audio data (waveform), compatible with other audio nodes. |
| **output** | `STRING` | The absolute path to the extracted audio file. |

## Usage notes

- The extracted audio is converted to PCM WAV format (44.1kHz, Stereo).
