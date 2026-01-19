# Save Images (V3)

The **Save Images (V3)** node saves a batch of images to disk as individual PNG files.

## Inputs

| Input Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **images** | `IMAGE` | The batch of images to save. | - |
| **directory** | `STRING` | The sub-directory within the output folder. | `saved_images` |
| **filename_prefix** | `STRING` | Prefix for the filenames. | `image` |

## Outputs

The node does not return any values.

## Usage notes

- Files are saved as `{directory}/{filename_prefix}_{index}.png`.
- Primarily used for debugging or extracting frames for external processing.
