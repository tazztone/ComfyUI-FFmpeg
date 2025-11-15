# ComfyUI-FFmpeg Project Index

This document provides a brief overview of the ComfyUI-FFmpeg project structure, outlining the purpose of key files and directories to facilitate navigation and development.

ComfyUI-FFmpeg is a custom node extension for ComfyUI that integrates FFmpeg functionalities, allowing users to perform various video and audio processing tasks directly within the ComfyUI interface. The project is designed to be modular, with each node corresponding to a specific FFmpeg command or a set of related commands.

## File Index

### `nodes_map.py`
This file serves as the central registry for all custom nodes in the project. It imports the node classes from the individual files in the `nodes/` directory and maps them to their respective display names in the ComfyUI interface. This is the primary file that ComfyUI interacts with to discover and load the custom nodes.

### `nodes/`
This directory contains the source code for each individual custom node. Each file in this directory corresponds to a single node and contains the node's class definition, input parameters, and the `execute` method that is called when the node is run. These node files import and utilize the core functionalities defined in `func.py`.

### `func.py`
This file contains the core logic and wrapper functions for interacting with FFmpeg. It includes functions for video processing, such as encoding, decoding, and filtering, as well as utility functions for file handling and validation. The nodes in the `nodes/` directory call these functions to perform their operations.

### `__init__.py`
This file indicates that the directory is a Python package, allowing for the modular import of the node classes in `nodes_map.py`.

### `requirements.txt`
This file lists the Python dependencies required for the project to run correctly.
