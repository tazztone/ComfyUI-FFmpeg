# Agent Instructions for ComfyUI-FFmpeg

This document provides comprehensive guidelines for agents and developers working on the **ComfyUI-FFmpeg** repository.

## Project Overview

**ComfyUI-FFmpeg** is a suite of custom nodes for ComfyUI that wraps FFmpeg functionalities. It allows users to perform video and audio processing tasks (editing, transcoding, watermarking, analysis, etc.) directly within ComfyUI workflows.

## Architecture & Data Flow

ComfyUI operates on a **Client-Server model**:
*   **Server (Python):** Handles the heavy lifting—loading models, processing tensors (images/latents), and executing algorithms.
*   **Client (JavaScript):** Handles the UI, graph connections, and widgets in the browser.

In **ComfyUI-FFmpeg**, this communication often involves:
*   **Python (Backend)**: Running FFmpeg processes, handling video files, and processing `IMAGE`/`AUDIO` tensors.
*   **JavaScript (Frontend)**: Managing specialized widgets (like the timeline in `LosslessCut`), passing configuration to the backend, and displaying metadata.

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

### Backend Development (Python)

#### Node Schema
While ComfyUI is migrating to a V3-style Modern Schema (classes inheriting from `comfy_api.latest.io.ComfyNode`), this repository currently uses the **V1 (Standard/Legacy) Schema**.
*   **`INPUT_TYPES`**: Defines input widgets and slots.
*   **`RETURN_TYPES` & `RETURN_NAMES`**: Defines output slots and labels.
*   **`FUNCTION`**: The entry point method.
*   **`CATEGORY`**: Grouping in the node menu.

#### Critical Data Types
*   **`IMAGE`**: Shape `[Batch, Height, Width, Channels]` (usually RGB). Values are floats `0.0` to `1.0`.
*   **`AUDIO`**: ComfyUI audio tensor format (shape `[Batch, Channels, Samples]`).
*   **`STRING`**: File paths or raw text.

> **Tip:** When processing tensors, check dimensions carefully. You often need to `unsqueeze` to match shapes or normalize `0-255` integers to `0.0-1.0` floats.

#### Advanced Execution Features
*   **Lazy Evaluation:** Add `{"lazy": True}` to `INPUT_TYPES` and implement `check_lazy_status` if you want to skip execution based on downstream needs.
*   **`IS_CHANGED`**: Return a unique value (like a hash or timestamp) to force the node to re-execute even if inputs haven't changed.
*   **`VALIDATE_INPUTS`**: Implement this static method to check data validity before the graph starts running.

### Adding New Nodes
1.  **Create Node File**: Add a new Python file in `nodes/`.
2.  **Register Node**: Import the class in `nodes_map.py` and add it to `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`.
3.  **Naming Convention**: Use descriptive names. Prefix display names with `🔥` (e.g., `🔥Add Text Watermark`).
4.  **Backward Compatibility**: Prefer modifying existing classes over creating new ones. If a new node is necessary, ensure it doesn't break existing workflows.

### Frontend Development
*   **Architecture**:
    *   Place JavaScript logic in `web/js/`.
    *   To serve these assets, the Python node class must define `WEB_DIRECTORY` (usually pointing to `./web` relative to the node or the root).
    *   Use `app.registerExtension` to integrate with the ComfyUI frontend.
*   **Modern Frontend APIs**:
    *   **Context Menus**: Use `getCanvasMenuItems` and `getNodeMenuItems` in your extension object. Avoid monkey-patching prototypes directly.
    *   **Settings**: Register settings via `app.registerExtension({ settings: [...] })` to make them appear in the main ComfyUI settings dialog.
*   **State Management**:
    *   **Hidden Widgets**: Use hidden inputs in `INPUT_TYPES` to pass state from the frontend (JS) to the backend (Python).
    *   **Execution Flow**: Button clicks in JS set an 'action' widget's value and call `app.queuePrompt()`. The Python node processes this and returns updated state in a `ui` dictionary (e.g., `{"ui": {"widget_name": [value]}}`). The JS `onExecuted` function then updates the hidden widgets for the next run.
*   **Data Exchange**:
    *   For large data (e.g., video metadata), the Python node should save a JSON file to the ComfyUI temporary directory.
    *   The JS frontend fetches this file asynchronously via `/output/filename.json?t=${Date.now()}` (using a timestamp to bypass caching).

### Testing
*   **Guide**: See `docs/TESTING.md` for full instructions.
*   **Infrastructure**:
    *   `tests/unit/`: Unit tests (no server needed).
    *   `tests/integration/`: Integration tests (require FFmpeg).
    *   `tests/run_tests.py`: **Wrapper script to run tests**.
*   **Running Tests**: `python tests/run_tests.py` (from package root) or `python -m pytest .` (from `tests/` directory).
*   **Mocking**: Centralized in `tests/conftest.py`.
*   **Environment**: `pip install -r requirements.txt`.

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

### Documentation & Polish
*   **Node Documentation**: Place markdown files in `web/docs/NameOfNode.md`. This content appears when users blindly click "Node Info".
*   **i18n (Localization)**: Support multiple languages (e.g., `zh`, `en`) by creating `locales/` folders if strictly necessary, mapping node names and inputs to translated strings.
*   **Workflow Templates**: Add example workflows (`.json`) and thumbnails to an `example_workflows` directory to help users get started quickly.

### FFmpeg Best Practices
*   **Helper Functions**: Use `func.py` for common tasks (e.g., `save_tensor_to_temp_file`, `get_output_path`).
*   **Security**: Always use `shlex.split()` when parsing user-provided command strings to prevent injection vulnerabilities.
*   **In-Memory Data**: For `IMAGE` or `AUDIO` tensors, save them to a temporary file, run the FFmpeg command, and then delete the temp file.
*   **GenericFFmpeg Placeholders**: When using generic command execution, support placeholders like `{media_in_1}` and `{output_file}` to allow flexible command construction.

### Troubleshooting Tips
*   **Visual Debugging**: Use `PromptServer.instance.send_sync("message_id", data)` in Python and listen via `api.addEventListener` in JS to send debug data to the browser console.
*   **Frontend Issues**: Check the browser developer console (F12) for JS errors.
*   **Binary Search**: If the suite crashes ComfyUI, disable half the nodes in `nodes_map.py` to isolate the culprit.

## Publishing to Comfy Registry

This repository is configured to publish nodes to the Comfy Registry.

### Setup
1.  Ensure you have a Publisher ID (`tazztone`) and API Key from [Comfy Registry](https://registry.comfy.org/).
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
*   **`RETURN_NAMES`**: Always define `RETURN_NAMES` in your node class to provide clear output labels in the UI.
*   **Optional Inputs**: To create a connectable input socket (optional input), omit the `default` value in `INPUT_TYPES`. Providing a `default` value creates a widget instead.

---

# ComfyUI-FFmpeg Project Index

This document provides a brief overview of the ComfyUI-FFmpeg project structure, outlining the purpose of key files and directories to facilitate navigation and development.

## File Index

### Registry & Core
*   **`nodes_map.py`**: The central registry. Imports node classes and maps them to display names.
*   **`func.py`**: Core utility module containing FFmpeg wrappers and file handling logic.
*   **`__init__.py`**: Package initialization.

### Audio Nodes
*   **`nodes/addAudio.py`**: Adds an audio track to a video. Supports various codecs and delay.
*   **`nodes/addAudioLegacy.py`**: Legacy version of the audio-adding node.
*   **`nodes/extractAudio.py`**: Extracts audio tracks from video files.
*   **`nodes/audioFilter.py`**: Applies raw FFmpeg audio filtergraphs.

### Video Editing (Cut/Merge)
*   **`nodes/mergingVideoByTwo.py`**: Merges two video files, handling resolution differences.
*   **`nodes/mergingVideoByPlenty.py`**: Merges a directory of videos into one.
*   **`nodes/stitchingVideo.py`**: Stitches two videos spatially (side-by-side or stacked).
*   **`nodes/multiCuttingVideo.py`**: Cuts video into multiple segments.
*   **`nodes/singleCuttingVideo.py`**: Extracts a single clip based on start/end times.
*   **`nodes/keyframeAwareCutting.py`**: Precision cutting at keyframes to avoid re-encoding artifacts.
*   **`nodes/losslessRemux.py`**: Changes container format (e.g., mp4 to mkv) without re-encoding.
*   **`nodes/LosslessCut.py`**: Interactive node for precise cutting with a UI timeline.

### Video Effects & Transforms
*   **`nodes/addImgWatermark.py`**: Overlays an image watermark.
*   **`nodes/addTextWatermark.py`**: Overlays a text watermark using custom fonts.
*   **`nodes/videoFlip.py`**: Flips video horizontally or vertically.
*   **`nodes/videoPlayback.py`**: Reverses video and/or audio playback.
*   **`nodes/pipVideo.py`**: Picture-in-Picture effect with positioning and scaling.
*   **`nodes/videoTransition.py`**: Applies transition effects (xfade) between two videos.
*   **`nodes/filtergraph.py`**: Applies raw FFmpeg video filtergraphs.
*   **`nodes/subtitle.py`**: Burns, adds, or extracts subtitles.

### Frame Processing
*   **`nodes/frames2video.py`**: Converts a sequence of image frames to a video.
*   **`nodes/video2frames.py`**: Extracts frames from a video to an image tensor.

### Utilities & Advanced
*   **`nodes/genericFFmpeg.py`**: Executes custom user-defined FFmpeg commands.
*   **`nodes/streamAnalysis.py`**: Returns JSON metadata about media streams.
*   **`nodes/streamMapping.py`**: Manually maps specific streams from input to output.
*   **`nodes/loadImageFromDir.py`**: Scans a directory for images.
*   **`nodes/imageCopy.py`**: Copies images to a destination.
*   **`nodes/imagesSave.py`**: Saves an image batch to disk.

## Project Roadmap & TODOs

### 🧹 Cleanup & Bloat Removal
*   **[DONE] Legacy Nodes**: Deprecate and remove `nodes/addAudioLegacy.py` (`AddAudioFile`). Use `nodes/addAudio.py` instead.
*   **[DONE] Redundancy**: `nodes/imageCopy.py` (`CopyImages`) appears to be a subset of `nodes/imagesSave.py` (`SaveImages`). Consolidate or remove `CopyImages`.
*   **Feature Creep Policy**: Avoid adding generic file manipulation nodes unless they are strictly required for FFmpeg workflows (e.g., handling specific tensor formats).

### 🛠️ Reliability & Quality
*   **`func.py`**:
    *   Remove `print()` statements in production code. Use proper logging.
    *   Improve error handling in `getVideoInfo` (JSON parsing).
    *   Centralize file extension definitions.
*   **Testing**: Investigate and fix `test_keyframe_aware_cutting` failure mentioned in Testing section.
*   **Security**: Ensure all new nodes using `subprocess` utilize `shlex.split()` or list-based arguments.
