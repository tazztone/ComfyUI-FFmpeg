# Apply Audio Filter (V3)

The **Apply Audio Filter (V3)** node applies a raw FFmpeg audio filtergraph to an audio stream.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **audio** | `AUDIO` | The input audio data. | - |
| **filtergraph** | `STRING` | The FFmpeg audio filter string (e.g., `loudnorm`, `volume=0.5`). | `loudnorm` |
| **filename** | `STRING` | The name of the output audio file. | `filtered_audio.wav` |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **audio** | `AUDIO` | The processed audio data. |
| **output** | `STRING` | The absolute path to the processed audio file. |

## Usage notes

- This node gives you access to the full power of FFmpeg's audio filters (`-af`).
- Common filters:
  - `loudnorm`: EBU R128 loudness normalization.
  - `volume=0.5`: Reduce volume by 50%.
  - `aecho=0.8:0.9:1000:0.3`: Add echo effect.
