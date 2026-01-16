<h1 align="center">ComfyUI-FFmpeg</h1>

<p align="center">
  <a href="https://github.com/MoonHugo/ComfyUI-FFmpeg/stargazers"><img src="https://img.shields.io/github/stars/MoonHugo/ComfyUI-FFmpeg?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/MoonHugo/ComfyUI-FFmpeg/network/members"><img src="https://img.shields.io/github/forks/MoonHugo/ComfyUI-FFmpeg?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/MoonHugo/ComfyUI-FFmpeg/issues"><img src="https://img.shields.io/github/issues/MoonHugo/ComfyUI-FFmpeg?style=flat-square" alt="Issues"></a>
</p>

## Introduction

**ComfyUI-FFmpeg** is a comprehensive extension for ComfyUI that integrates the power of **FFmpeg** directly into your workflows. It provides a suite of nodes for video editing, audio processing, watermarking, format conversion, and more—ranging from simple tasks to advanced stream manipulation.

Whether you need to stitch videos, extract frames, add subtitles, or perform complex filter operations, ComfyUI-FFmpeg offers a node for the job.

## Prerequisites

1.  **FFmpeg**: You must have FFmpeg installed on your system and added to your system's PATH.
    *   **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [BtbN](https://github.com/BtbN/FFmpeg-Builds/releases).
    *   **Linux**: `sudo apt install ffmpeg`
    *   **macOS**: `brew install ffmpeg`
2.  **ComfyUI**: A working installation of ComfyUI.

## Installation

### Method 1: ComfyUI Manager (Recommended)
1.  Open **ComfyUI Manager**.
2.  Search for `ComfyUI-FFmpeg`.
3.  Click **Install**.
4.  Restart ComfyUI.

### Method 2: Git Clone
1.  Navigate to your custom nodes directory:
    ```bash
    cd ComfyUI/custom_nodes/
    ```
2.  Clone the repository:
    ```bash
    git clone https://github.com/MoonHugo/ComfyUI-FFmpeg.git
    ```
3.  Install dependencies:
    ```bash
    cd ComfyUI-FFmpeg
    pip install -r requirements.txt
    ```
4.  Restart ComfyUI.

---

## Node Reference

### 🎞️ Video Editing & Manipulation

#### 🔥 Merge Videos
Merges two video files into a single video, handling resolution differences.
![](./assets/7.png)

#### 🔥 Merge Video Batch
Merges multiple short videos from a directory into a single long video. Requires same encoding/resolution.
![](./assets/11.png)

#### 🔥 Stitch Videos
Stitches two videos together spatially, either horizontally (side-by-side) or vertically.
![](./assets/8.png)

#### 🔥 Split Video
Cuts a video into multiple smaller segments of a specified duration.
![](./assets/9.png)

#### 🔥 Trim Video
Extracts a single segment from a video based on start/end times (`HH:MM:SS`).
![](./assets/10.png)

#### 🔥 Keyframe Trim
Cuts a video at the nearest keyframes to the specified times. Ensures fast, clean cuts without re-encoding.

#### 🔥 Lossless Cut
**Interactive Node**: Provides a UI timeline for precise, keyframe-accurate cutting with real-time preview.
*   **Features**: Visual timeline, play/pause controls, start/end point setting.

#### 🔥 Remux Video
Changes the container format (e.g., `.mp4` -> `.mkv`) without re-encoding streams. Instant conversion preserving 100% quality.

---

### 🎨 Video Effects & Transitions

#### 🔥 Picture In Picture
Overlays one video onto another with customizable position, scaling, and optional Chroma Key (Green Screen) removal.
![](./assets/13.png)

#### 🔥 Video Transition
Creates a transition effect (e.g., fade, wipe, slide) between two videos using FFmpeg's `xfade` filter.
![](./assets/14.png)

#### 🔥 Flip Video
Flips a video horizontally, vertically, or both.
![](./assets/5.png)

#### 🔥 Reverse Video
Reverses video playback. Can optionally reverse audio as well.
![](./assets/15.png)

#### 🔥 Apply Filtergraph
Applies a raw FFmpeg video filtergraph string for custom complex effects.

---

### 📝 Watermarking & Subtitles

#### 🔥 Add Text Watermark
Adds a text overlay to a video. Supports custom fonts (in `fonts/` folder), size, color, and positioning.
![](./assets/3.png)

#### 🔥 Add Image Watermark
Overlays an image watermark onto a video.
![](./assets/4.png)

#### 🔥 Handle Subtitles
Burns subtitles into a video, adds them as a stream, or extracts them from a file.

---

### 🎵 Audio Operations

#### 🔥 Add Audio
Adds or replaces an audio track in a video. Supports delay, looping, and mixing.
![](./assets/12.png)

#### 🔥 Extract Audio
Extracts the audio track from a video file to formats like `.mp3`, `.wav`, or `.aac`.
![](./assets/6.png)

#### 🔥 Apply Audio Filter
Applies a raw FFmpeg audio filtergraph to an audio stream.

---

### 🖼️ Frame & Image Processing

#### 🔥 Video to Frames
Extracts frames from a video into an `IMAGE` tensor for use with other ComfyUI nodes (e.g., IPAdapter, ControlNet).
![](./assets/1.png)

#### 🔥 Frames to Video
Converts a sequence of images (or an `IMAGE` tensor) into a video file.
![](./assets/2.png)

#### 🔥 Load Images from Directory
Loads all images from a folder as a batch tensor.

#### 🔥 Save Images
Saves a batch of images to a specified directory.

#### 🔥 Copy Images <!-- TODO: Redundant with Save Images, consider deprecating -->
Utility to copy image files to a destination.

---

### 🛠️ Advanced & Analysis

#### 🔥 Generic FFmpeg
**Advanced**: Executes arbitrary FFmpeg commands. Supports placeholders like `{media_in_1}` and `{output_file}`. Gives you full access to the FFmpeg CLI.

#### 🔥 Analyze Streams
Returns detailed JSON metadata about a file's video, audio, and subtitle streams (codec, bitrate, duration, etc.).

#### 🔥 Apply Stream Map
Manually maps input streams to output streams for precise control over track selection.

---

## Socials

-   **Bilibili:** [My Bilibili Homepage](https://space.bilibili.com/1303099255)

## Acknowledgments

Special thanks to the contributors of the [FFmpeg](https://github.com/FFmpeg/FFmpeg) project.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MoonHugo/ComfyUI-FFmpeg&type=Date)](https://star-history.com/#MoonHugo/ComfyUI-FFmpeg&Date)
