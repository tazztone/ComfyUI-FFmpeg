# Load Images from Directory (V3)

The **Load Images from Directory (V3)** node reads all supported images from a specified folder and converts them into a batch tensor.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **directory** | `STRING` | The absolute path to the directory containing images. | - |

## Outputs

| Output Name | Type | Description |
| :--- | :--- | :--- |
| **images** | `IMAGE` | The loaded images as a batch tensor. |

## Usage notes

- Supports `.png`, `.jpg`, `.jpeg`.
- Images are sorted alphabetically by filename.
- All images should ideally be the same dimension, though ComfyUI handles some variation (padding/cropping logic pending).
