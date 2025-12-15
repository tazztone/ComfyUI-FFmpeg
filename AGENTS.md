# Agent Instructions for ComfyUI-FFmpeg

This document provides comprehensive guidelines for agents and developers working on the **ComfyUI-FFmpeg** repository.

## Project Overview

**ComfyUI-FFmpeg** is a suite of custom nodes for ComfyUI that wraps FFmpeg functionalities. It allows users to perform video and audio processing tasks (editing, transcoding, watermarking, analysis, etc.) directly within ComfyUI workflows.

## Code Structure

*   **`nodes/`**: Contains the Python source code for individual nodes. Each file typically corresponds to one node class.
*   **`func.py`**: A shared utility module containing core FFmpeg wrapper logic, file handling helpers, and validation functions.
*   **`nodes_map.py`**: The registry file that imports node classes and defines `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`.
*   **`web/`**: Contains frontend assets.
    *   **`web/js/`**: JavaScript files for custom node UIs (e.g., hidden widgets, interactive canvases).
*   **`fonts/`**: Directory for font files used by nodes like `AddTextWatermark`.
*   **`tests/`**: Unit tests using `pytest`.
*   **`.github/workflows/`**: CI/CD workflows, including Comfy Registry publishing.
*   **`pyproject.toml`**: Project metadata and dependencies for Comfy Registry.

## Development Guidelines

### Adding New Nodes
1.  **Create Node File**: Add a new Python file in `nodes/`.
2.  **Register Node**: Import the class in `nodes_map.py` and add it to `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`.
3.  **Naming Convention**: Use descriptive names. Prefix display names with `🔥` (e.g., `🔥FFmpeg/MyNode`).
4.  **Backward Compatibility**: Prefer modifying existing classes over creating new ones. If a new node is necessary, ensure it doesn't break existing workflows.

### Frontend Development
*   Place JavaScript logic in `web/js/`.
*   To serve these assets, the Python node class must define `WEB_DIRECTORY` (usually pointing to `./web` relative to the node or the root).
*   Use `app.registerExtension` to integrate with the ComfyUI frontend.

### Testing
*   **Framework**: Use `pytest`.
*   **Running Tests**: `pytest tests/test_nodes.py` (from root).
*   **Mocking**: Mock ComfyUI-specific modules (`folder_paths`, `torch`) in unit tests using `unittest.mock` or `sys.modules` manipulation to run tests in isolation.
*   **Environment**: `pip install -r requirements-test.txt`.

### Dependencies
*   **Core**: `numpy`, `Pillow`, `torch`, `torchaudio` are assumed to be present in the ComfyUI environment.
*   **FFmpeg**: The system must have `ffmpeg` installed and in the PATH.
*   **Policy**: Do **not** add new dependencies to `requirements.txt` unless explicitly instructed.

### Coding Style
*   **Docstrings**: Use Google Style Python Docstrings for all classes and functions.
*   **Imports**: For shared modules like `func`, use a `try-except ImportError` block to support both package execution and standalone testing:
    ```python
    try:
        from ..func import my_helper
    except ImportError:
        from func import my_helper
    ```

### FFmpeg Best Practices
*   **Helper Functions**: Use `func.py` for common tasks (e.g., `save_tensor_to_temp_file`, `get_output_path`).
*   **Security**: Always use `shlex.split()` when parsing user-provided command strings to prevent injection vulnerabilities.
*   **In-Memory Data**: For `IMAGE` or `AUDIO` tensors, save them to a temporary file, run the FFmpeg command, and then delete the temp file.

## Publishing to Comfy Registry

This repository is configured to publish nodes to the Comfy Registry.

### Setup
1.  Ensure you have a Publisher ID and API Key from [Comfy Registry](https://registry.comfy.org/).
2.  The GitHub Action `.github/workflows/publish_action.yml` handles automated publishing.
3.  **IMPORTANT:** You must set the `REGISTRY_ACCESS_TOKEN` secret in your GitHub repository settings with your API Key.

### Publishing a New Version
1.  Update the `version` field in `pyproject.toml` (e.g., `1.0.0` -> `1.0.1`).
2.  Push the change to the `main` branch.
3.  The GitHub Action will automatically detect the change and publish.

## Environment Setup

Run `./environment_setup.sh` to install FFmpeg and Python dependencies.

## Key Patterns & Best Practices

*   **`INPUT_TYPES` Caching**: Avoid expensive operations inside `INPUT_TYPES` as it is called frequently. Cache results where possible.
*   **Hidden Widgets**: For interactive nodes, use hidden inputs to pass state from the frontend (JS) to the backend (Python).
*   **`RETURN_NAMES`**: Always define `RETURN_NAMES` in your node class to provide clear output labels in the UI.
*   **Frontend Data Exchange**: For large data (e.g., metadata), save a JSON file to the temp directory in Python and fetch it in JS via `/output/...`. Use a timestamp query param to bypass caching.
