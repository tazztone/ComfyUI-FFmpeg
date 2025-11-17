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
