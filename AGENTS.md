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


---

# ComfyUI-FFmpeg Project Index

This document provides a brief overview of the ComfyUI-FFmpeg project structure, outlining the purpose of key files and directories to facilitate navigation and development.

ComfyUI-FFmpeg is a custom node extension for ComfyUI that integrates FFmpeg functionalities, allowing users to perform various video and audio processing tasks directly within the ComfyUI interface. The project is designed to be modular, with each node corresponding to a specific FFmpeg command or a set of related commands.

## File Index

### `nodes_map.py`
This file serves as the central registry for all custom nodes in the project. It imports the node classes from the individual files in the `nodes/` directory and maps them to their respective display names in the ComfyUI interface. the primary file that ComfyUI interacts with to discover and load the custom nodes.

### `nodes/`
This directory contains the source code for each individual custom node. Each file in this directory corresponds to a single node and contains the node's class definition, input parameters, and the `execute` method that is called when the node is run. These node files import and utilize the core functionalities defined in `func.py`.

### `func.py`
This file contains the core logic and wrapper functions for interacting with FFmpeg. It includes functions for video processing, such as encoding, decoding, and filtering, as well as utility functions for file handling and validation. The nodes in the `nodes/` directory call these functions to perform their operations.

### `__init__.py`
This file indicates that the directory is a Python package, allowing for the modular import of the node classes in `nodes_map.py`.

### `requirements.txt`
This file lists the Python dependencies required for the project to run correctly.

### `nodes/addAudio.py`
adds an audio track to a video file. It can accept audio data from other nodes or a separate audio file. It supports various audio codecs and bitrates, and it can perform a lossless remux if the formats are compatible.

### `nodes/addAudioLegacy.py`
an older version of the audio-adding node. It takes a video and an audio file (or a video with audio) and combines them.

### `nodes/addImgWatermark.py`
overlays an image watermark onto a video at a specified position and size.

### `nodes/addTextWatermark.py`
adds a text watermark to a video. You can customize the font, size, color, and position of the text.

### `nodes/extractAudio.py`
extracts the audio track from a video file and can save it as a separate audio file (`.wav`, `.mp3`, or `.flac`) or pass the audio data to other nodes.

### `nodes/frames2video.py`
creates a video from a sequence of images (frames). It can also add an audio track to the generated video.

### `nodes/imageCopy.py`
an auxiliary tool that copies a list of images to a specified directory.

### `nodes/imagePath2Tensor.py`
This auxiliary node takes a list of image file paths, loads the images, and converts them into a single image tensor for processing in ComfyUI.

### `nodes/imagesSave.py`
This auxiliary node saves a batch of images from a tensor to a specified directory.

### `nodes/loadImageFromDir.py`
This auxiliary node scans a directory for images and returns a list of their file paths.

### `nodes/mergingVideoByPlenty.py`
merges multiple video files from a single directory into one video file.

### `nodes/mergingVideoByTwo.py`
merges two video files. It can handle differences in resolution and audio streams between the two videos.

### `nodes/multiCuttingVideo.py`
cuts a video into multiple smaller segments of a specified duration.

### `nodes/pipVideo.py`
creates a picture-in-picture (PiP) effect by overlaying one video on top of another. It includes options for positioning, scaling, audio selection, and even chroma keying (green screen removal).

### `nodes/singleCuttingVideo.py`
extracts a single clip from a video based on a specified start and end time.

### `nodes/stitchingVideo.py`
stitches two videos together either horizontally (side-by-side) or vertically (one on top of the other).

### `nodes/video2frames.py`
extracts all the frames from a video file, returning them as an image tensor. It can also save the frames to disk as individual image files.

### `nodes/videoFlip.py`
flips a video horizontally, vertically, or both.

### `nodes/videoPlayback.py`
reverses a video, creating a playback effect. It can also reverse the audio track.

### `nodes/videoTransition.py`
creates a transition effect between two videos using FFmpeg's `xfade` filter.

### `nodes/audioFilter.py`
applies a raw FFmpeg audio filtergraph to an audio stream.

### `nodes/filtergraph.py`
applies a raw FFmpeg filtergraph to a video.

### `nodes/genericFFmpeg.py`
a generic node to execute custom FFmpeg commands using a placeholder system. It supports IMAGE and AUDIO data types.

### `nodes/keyframeAwareCutting.py`
cuts a video at the nearest keyframes to the specified start and end times to ensure clean cuts without re-encoding.

### `nodes/losslessRemux.py`
changes the container of a video or audio file (e.g., from `.mp4` to `.mkv`) without re-encoding the streams, making the process fast and preserving quality.

### `nodes/streamAnalysis.py`
analyzes a media file and outputs its stream information in JSON format, which is useful for debugging and advanced stream manipulation.

### `nodes/streamMapping.py`
allows for manual mapping of streams from an input file to the output file, giving precise control over which video, audio, and subtitle tracks are included.

### `nodes/subtitle.py`
provides subtitle handling functionalities, allowing you to burn subtitles into a video, add them as a separate stream, or extract them from a video.
