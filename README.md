<h1 align="center">ComfyUI-FFmpeg</h1>

<p align="center">
    <br> <font size=5>English | <a href="README_CN.md">中文</a></font>
</p>

## Introduction

**ComfyUI-FFmpeg** is a powerful extension for ComfyUI that wraps frequently used FFmpeg functionalities into intuitive nodes. This allows you to perform a wide range of video processing tasks directly within your ComfyUI workflow, streamlining your creative process.

## Prerequisites

Before using this extension, you must have **FFmpeg** installed on your system and accessible from the command line. For installation instructions, please refer to the official FFmpeg documentation or community guides.

## Installation

You can install ComfyUI-FFmpeg using one of the following methods:

### Method 1: Git Clone

1.  Navigate to the `custom_nodes` directory within your ComfyUI installation:
    ```sh
    cd ComfyUI/custom_nodes/
    ```
2.  Clone the repository:
    ```sh
    git clone https://github.com/MoonHugo/ComfyUI-FFmpeg.git
    ```
3.  Install the required dependencies:
    ```sh
    cd ComfyUI-FFmpeg
    pip install -r requirements.txt
    ```
4.  Restart ComfyUI.

### Method 2: Manual Download

1.  Download the source code as a ZIP archive.
2.  Extract the contents of the ZIP file into the `ComfyUI/custom_nodes/` directory.
3.  Restart ComfyUI.

### Method 3: ComfyUI-Manager

1.  Open the ComfyUI-Manager.
2.  Search for "ComfyUI-FFmpeg" and install it.
3.  Restart ComfyUI.

## Node Reference

This section provides a detailed overview of each node available in ComfyUI-FFmpeg.

---

### 🔥 Video2Frames

Extracts frames from a video and saves them as individual images.

![](./assets/1.png)

**Parameters:**

*   `video_path`: The file path to the input video (e.g., `C:\Users\Desktop\video.mp4`).
*   `output_path`: The directory where the extracted frames will be saved (e.g., `C:\Users\Desktop\output`).
*   `frames_max_width`: The maximum width for the output frames. If set to `0`, the original width is maintained. If the specified width is smaller than the original, the frames will be scaled down while preserving the aspect ratio.

---

### 🔥 Frames2Video

Converts a sequence of images into a video file.

![](./assets/2.png)

**Parameters:**

*   `frame_path`: The directory containing the input image frames (e.g., `C:\Users\Desktop\output`).
*   `fps`: The frame rate of the output video. Default is `30`.
*   `video_name`: The name of the output video file (e.g., `my_video.mp4`).
*   `output_path`: The directory where the output video will be saved (e.g., `C:\Users\Desktop\output`).
*   `audio_path`: (Optional) The file path to an audio file to be included in the video (e.g., `C:\Users\Desktop\audio.mp3`).

---

### 🔥 AddTextWatermark

Adds a text watermark to a video.

![](./assets/3.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the watermarked video.
*   `font_file`: The font file for the watermark text. Place your font files in the `ComfyUI-FFmpeg/fonts` directory.
*   `font_size`: The font size of the watermark text.
*   `font_color`: The color of the watermark text (e.g., `#FFFFFF` or `white`).
*   `position_x`: The x-coordinate for the watermark's position.
*   `position_y`: The y-coordinate for the watermark's position.

---

### 🔥 AddImgWatermark

Adds an image watermark to a video.

![](./assets/4.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the watermarked video.
*   `watermark_image`: The file path to the watermark image.
*   `watermark_img_width`: The width of the watermark image.
*   `position_x`: The x-coordinate for the watermark's position.
*   `position_y`: The y-coordinate for the watermark's position.

---

### 🔥 VideoFlip

Flips a video horizontally, vertically, or both.

![](./assets/5.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the flipped video.
*   `flip_type`: The type of flip to apply (`horizontal`, `vertical`, or `both`).

---

### 🔥 ExtractAudio

Extracts the audio track from a video file.

![](./assets/6.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the extracted audio.
*   `audio_format`: The desired format for the output audio file (e.g., `.mp3`, `.wav`, `.aac`).

---

### 🔥 MergingVideoByTwo

Merges two video files into a single video.

![](./assets/7.png)

**Parameters:**

*   `video1_path`: The file path to the first video.
*   `video2_path`: The file path to the second video.
*   `device`: The processing device to use (`CPU` or `GPU`).
*   `resolution_reference`: Specifies which video (`video1` or `video2`) to use as a reference for the output resolution.
*   `output_path`: The directory to save the merged video.

---

### 🔥 MergingVideoByPlenty

Merges multiple short videos with the same encoding, resolution, and frame rate into a single long video.

![](./assets/11.png)

**Parameters:**

*   `video_path`: The directory containing the video files to be merged.
*   `output_path`: The directory to save the merged video.

---

### 🔥 StitchingVideo

Stitches two videos together, either horizontally or vertically.

![](./assets/8.png)

**Parameters:**

*   `video1_path`: The file path to the first video.
*   `video2_path`: The file path to the second video.
*   `device`: The processing device to use (`CPU` or `GPU`).
*   `use_audio`: Specifies which video's audio to use in the stitched output (`video1` or `video2`).
*   `stitching_type`: The stitching orientation (`horizontal` or `vertical`).
*   `output_path`: The directory to save the stitched video.
*   `scale_and_crop`: Whether to scale and crop the output to match the dimensions of `video1`.

---

### 🔥 MultiCuttingVideo

Cuts a video into multiple segments of a specified duration.

![](./assets/9.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the video segments.
*   `segment_time`: The duration of each segment in seconds. Note that cuts are made at the nearest keyframe, so the actual segment duration may vary slightly.

---

### 🔥 SingleCuttingVideo

Extracts a single segment from a video based on a specified start and end time.

![](./assets/10.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the extracted segment.
*   `start_time`: The start time of the segment in `HH:MM:SS` format.
*   `end_time`: The end time of the segment in `HH:MM:SS` format.

---

### 🔥 AddAudio

Adds an audio track to a video.

![](./assets/12.png)

**Parameter Description**
- **video_path**: Local video path, e.g.:`C:\Users\Desktop\111.mp4`
- **output_path**: Video save path, e.g.:`C:\Users\Desktop\output`
- **audio**: Processed audio from upstream nodes (VHS, TTS, RVC, etc.)
- **audio_file_path**: Path to audio file (used only if audio input not connected)
- **audio_codec**: Audio codec (copy = lossless if compatible)
- **audio_bitrate**: Audio bitrate (e.g., 128k, 192k, 320k)
- **filename_prefix**: Prefix for output filename (optional)
- **delay_play**: The audio delay playback time is measured in seconds, with a default value of 0

---

### 🔥 PipVideo

Creates a picture-in-picture (PiP) effect by overlaying one video on top of another.

![](./assets/13.png)

**Parameters:**

*   `video1_path`: The file path to the background video.
*   `video2_path`: The file path to the foreground video.
*   `device`: The processing device to use (`CPU` or `GPU`).
*   `use_audio`: Specifies which video's audio to use in the output (`video1` or `video2`).
*   `use_duration`: Specifies which video's duration to use for the output (`video1` or `video2`).
*   `align_type`: The position of the foreground video (`top-left`, `top-right`, `bottom-left`, `bottom-right`, or `center`).
*   `pip_fg_zoom`: The scaling factor for the foreground video. A larger value results in a smaller foreground.
*   `output_path`: The directory to save the PiP video.
*   `scale_and_crop`: The scaling and cropping ratio.
*   `fps`: The frame rate of the output video.
*   `is_chromakey`: Whether to apply a green screen (chroma key) effect to the foreground video.

---

### 🔥 VideoTransition

Adds a transition effect between two videos.

![](./assets/14.png)

**Parameters:**

*   `video1_path`: The file path to the first video.
*   `video2_path`: The file path to the second video.
*   `reference_video`: Specifies which video to use as a reference for the output resolution and frame rate.
*   `device`: The processing device to use (`CPU` or `GPU`).
*   `transition`: The name of the transition effect. To see a list of available transitions, run `ffmpeg -hide_banner -h filter=xfade`.
*   `transition_duration`: The duration of the transition in seconds.
*   `offset`: The start time of the transition in the first video.
*   `output_path`: The directory to save the output video.

---

### 🔥 VideoPlayback

Reverses the playback of a video.

![](./assets/15.png)

**Parameters:**

*   `video_path`: The file path to the input video.
*   `output_path`: The directory to save the reversed video.
*   `reverse_audio`: Whether to reverse the audio as well.

---

### 🔥 Load Images from Directory

Loads all images from a directory and returns them as an IMAGE tensor.

**Parameters:**

*   `directory`: The directory containing the images to load.

---

### 🔥 Copy Images

Copies a list of images to a specified directory.

**Parameters:**

*   `images`: The images to copy.
*   `directory`: The destination directory for the copied images.

---

### 🔥 Save Images

Saves a batch of images to a specified directory.

**Parameters:**

*   `images`: The images to save.
*   `directory`: The directory where images will be saved.
*   `filename_prefix`: Prefix for the output filename.

---

### 🔥 Apply Filtergraph

Apply a raw FFmpeg filtergraph to a video.

**Parameters:**

*   `video`: The file path to the input video.
*   `filtergraph`: The FFmpeg filtergraph string.
*   `output_path`: The directory to save the processed video.
*   `output_ext`: The file extension for the output video.

---

### 🔥 Apply Stream Map

Apply stream mapping to a video.

**Parameters:**

*   `video`: The file path to the input video.
*   `maps`: The FFmpeg stream mapping string.
*   `output_path`: The directory to save the processed video.
*   `output_ext`: The file extension for the output video.

---

### 🔥 Handle Subtitles

A node to handle subtitles.

**Parameters:**

*   `video`: The file path to the input video.
*   `subtitle_file`: The file path to the subtitle file.
*   `action`: The subtitle action to perform (`burn`, `add`, or `extract`).
*   `output_path`: The directory to save the processed video.
*   `output_ext`: The file extension for the output video.

---

### 🔥 Apply Audio Filter

Apply a raw FFmpeg audio filtergraph to an audio stream.

**Parameters:**

*   `audio`: The file path to the input audio.
*   `filtergraph`: The FFmpeg audio filtergraph string.
*   `output_path`: The directory to save the processed audio.
*   `output_ext`: The file extension for the output audio.

---

### 🔥 Analyze Streams

Analyzes the streams of a video file and returns detailed information about video, audio, and subtitle streams.

**Parameters:**

*   `video`: The file path to the input video.

**Returns:**
*   JSON string containing detailed stream information including codec, resolution, bitrate, duration, and more.

---

### 🔥 Keyframe Trim

Cuts a video at the nearest keyframes to the specified start and end times for precise editing.

**Parameters:**

*   `video`: The file path to the input video.
*   `start_time`: The start time in `HH:MM:SS` format.
*   `end_time`: The end time in `HH:MM:SS` format.
*   `filename`: The output filename for the trimmed video.

---

### 🔥 Remux Video

Changes the container of a video file without re-encoding (lossless operation).

**Parameters:**

*   `video`: The file path to the input video.
*   `container`: The target container format (`mp4`, `mkv`, `mov`, `webm`).
*   `filename`: The output filename for the remuxed video.

---

### 🔥 Generic FFmpeg

Executes custom FFmpeg commands for advanced users who need full control over FFmpeg parameters.

**Parameters:**

*   `video`: The file path to the input video.
*   `ffmpeg_command`: Custom FFmpeg command string (without the base `ffmpeg -i video` part).
*   `filename`: The output filename.

**Note:** This node provides maximum flexibility for advanced users but requires knowledge of FFmpeg syntax.

---

### 🔥 Lossless Cut

An interactive node for precise video cutting at keyframes with real-time preview and controls.

**Parameters:**

*   `video`: The file path to the input video.
*   `action`: The action to perform (`cut`, `preview`, or `reset`).
*   `in_point`: The start time in seconds.
*   `out_point`: The end time in seconds (`-1` means end of video).
*   `current_position`: Current playback position in seconds.

**Features:**
- Interactive timeline controls
- Real-time frame preview
- Keyframe-accurate cutting
- Visual feedback during editing

---

## Socials

-   **Bilibili:** [My Bilibili Homepage](https://space.bilibili.com/1303099255)

## Acknowledgments

A special thanks to the contributors of the [FFmpeg](https://github.com/FFmpeg/FFmpeg) repository.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MoonHugo/ComfyUI-FFmpeg&type=Date)](https://star-history.com/#MoonHugo/ComfyUI-FFmpeg&Date)
