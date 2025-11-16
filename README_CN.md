<h1 align="center">ComfyUI-FFmpeg</h1>

<p align="center">
    <br> <font size=5>中文 | <a href="README.md">English</a></font>
</p>

## 介绍

**ComfyUI-FFmpeg** 是 ComfyUI 的一个强大扩展，它将常用的 FFmpeg 功能封装成直观的节点。这使您可以直接在 ComfyUI 工作流中执行各种视频处理任务，从而简化您的创作流程。

## 先决条件

在使用此扩展之前，您必须在系统上安装 **FFmpeg**，并能从命令行访问。有关安装说明，请参阅官方 FFmpeg 文档或社区指南。

## 安装

您可以使用以下方法之一安装 ComfyUI-FFmpeg：

### 方法一：Git 克隆

1.  导航到 ComfyUI 安装目录下的 `custom_nodes` 目录：
    ```sh
    cd ComfyUI/custom_nodes/
    ```
2.  克隆存储库：
    ```sh
    git clone https://github.com/MoonHugo/ComfyUI-FFmpeg.git
    ```
3.  安装所需的依赖项：
    ```sh
    cd ComfyUI-FFmpeg
    pip install -r requirements.txt
    ```
4.  重启 ComfyUI。

### 方法二：手动下载

1.  下载源代码的 ZIP 存档。
2.  将 ZIP 文件的内容解压到 `ComfyUI/custom_nodes/` 目录中。
3.  重启 ComfyUI。

### 方法三：ComfyUI-Manager

1.  打开 ComfyUI-Manager。
2.  搜索“ComfyUI-FFmpeg”并安装。
3.  重启 ComfyUI。

## 节点参考

本节详细介绍了 ComfyUI-FFmpeg 中可用的每个节点。

---

### 🔥 Video2Frames

从视频中提取帧并将其保存为单个图像。

![](./assets/1.png)

**参数：**

*   `video_path`: 输入视频的文件路径（例如 `C:\Users\Desktop\video.mp4`）。
*   `output_path`: 保存提取帧的目录（例如 `C:\Users\Desktop\output`）。
*   `frames_max_width`: 输出帧的最大宽度。如果设置为 `0`，则保持原始宽度。如果指定宽度小于原始宽度，则在保持宽高比的同时缩小帧。

---

### 🔥 Frames2Video

将一系列图像转换为视频文件。

![](./assets/2.png)

**参数：**

*   `frame_path`: 包含输入图像帧的目录（例如 `C:\Users\Desktop\output`）。
*   `fps`: 输出视频的帧率。默认为 `30`。
*   `video_name`: 输出视频文件的名称（例如 `my_video.mp4`）。
*   `output_path`: 保存输出视频的目录（例如 `C:\Users\Desktop\output`）。
*   `audio_path`: （可选）要包含在视频中的音频文件的文件路径（例如 `C:\Users\Desktop\audio.mp3`）。

---

### 🔥 AddTextWatermark

向视频添加文本水印。

![](./assets/3.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存带水印视频的目录。
*   `font_file`: 水印文本的字体文件。请将字体文件放在 `ComfyUI-FFmpeg/fonts` 目录中。
*   `font_size`: 水印文本的字体大小。
*   `font_color`: 水印文本的颜色（例如 `#FFFFFF` 或 `white`）。
*   `position_x`: 水印位置的 x 坐标。
*   `position_y`: 水印位置的 y 坐标。

---

### 🔥 AddImgWatermark

向视频添加图像水印。

![](./assets/4.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存带水印视频的目录。
*   `watermark_image`: 水印图像的文件路径。
*   `watermark_img_width`: 水印图像的宽度。
*   `position_x`: 水印位置的 x 坐标。
*   `position_y`: 水印位置的 y 坐标。

---

### 🔥 VideoFlip

水平、垂直或同时翻转视频。

![](./assets/5.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存翻转视频的目录。
*   `flip_type`: 应用的翻转类型（`horizontal`、`vertical` 或 `both`）。

---

### 🔥 ExtractAudio

从视频文件中提取音轨。

![](./assets/6.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存提取音频的目录。
*   `audio_format`: 输出音频文件的所需格式（例如 `.mp3`、`.wav`、`.aac`）。

---

### 🔥 MergingVideoByTwo

将两个视频文件合并为一个视频。

![](./assets/7.png)

**参数：**

*   `video1_path`: 第一个视频的文件路径。
*   `video2_path`: 第二个视频的文件路径。
*   `device`: 使用的处理设备（`CPU` 或 `GPU`）。
*   `resolution_reference`: 指定使用哪个视频（`video1` 或 `video2`）作为输出分辨率的参考。
*   `output_path`: 保存合并视频的目录。

---

### 🔥 MergingVideoByPlenty

将多个具有相同编码、分辨率和帧率的短视频合并为一个长视频。

![](./assets/11.png)

**参数：**

*   `video_path`: 包含要合并的视频文件的目录。
*   `output_path`: 保存合并视频的目录。

---

### 🔥 StitchingVideo

将两个视频水平或垂直拼接在一起。

![](./assets/8.png)

**参数：**

*   `video1_path`: 第一个视频的文件路径。
*   `video2_path`: 第二个视频的文件路径。
*   `device`: 使用的处理设备（`CPU` 或 `GPU`）。
*   `use_audio`: 指定在拼接输出中使用哪个视频的音频（`video1` 或 `video2`）。
*   `stitching_type`: 拼接方向（`horizontal` 或 `vertical`）。
*   `output_path`: 保存拼接视频的目录。
*   `scale_and_crop`: 是否缩放和裁剪输出以匹配 `video1` 的尺寸。

---

### 🔥 MultiCuttingVideo

将视频剪切成多个指定时长的片段。

![](./assets/9.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存视频片段的目录。
*   `segment_time`: 每个片段的时长（以秒为单位）。请注意，剪切是在最近的关键帧处进行的，因此实际片段时长可能略有不同。

---

### 🔥 SingleCuttingVideo

根据指定的开始和结束时间从视频中提取单个片段。

![](./assets/10.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存提取片段的目录。
*   `start_time`: 片段的开始时间，格式为 `HH:MM:SS`。
*   `end_time`: 片段的结束时间，格式为 `HH:MM:SS`。

---

### 🔥 AddAudio

向视频添加音轨。

![](./assets/12.png)

###### 参数说明
**video_path**: 视频路径，比如：`C:\Users\Desktop\111.mp4`<br>
**output_path**: 视频保存路径，比如：`C:\Users\Desktop\output`<br>
**audio**: 来自上游节点的音频数据（VHS、TTS、RVC等）。<br>
**audio_file_path**: 音频文件路径（仅当未连接音频输入时使用）。<br>
**audio_codec**: 音频编解码器（copy = 无损（如果兼容））。<br>
**audio_bitrate**: 音频比特率（例如，128k, 192k, 320k）。<br>
**filename_prefix**: 输出文件名的前缀（可选）。<br>
**delay_play**: 音频延迟播放时间，单位为秒，默认值为0。<br>

---

### 🔥 PipVideo

通过在一个视频上叠加另一个视频来创建画中画（PiP）效果。

![](./assets/13.png)

**参数：**

*   `video1_path`: 背景视频的文件路径。
*   `video2_path`: 前景视频的文件路径。
*   `device`: 使用的处理设备（`CPU` 或 `GPU`）。
*   `use_audio`: 指定在输出中使用哪个视频的音频（`video1` 或 `video2`）。
*   `use_duration`: 指定使用哪个视频的时长作为输出的时长（`video1` 或 `video2`）。
*   `align_type`: 前景视频的位置（`top-left`、`top-right`、`bottom-left`、`bottom-right` 或 `center`）。
*   `pip_fg_zoom`: 前景视频的缩放因子。值越大，前景越小。
*   `output_path`: 保存画中画视频的目录。
*   `scale_and_crop`: 缩放和裁剪比例。
*   `fps`: 输出视频的帧率。
*   `is_chromakey`: 是否对前景视频应用绿幕（色度键）效果。

---

### 🔥 VideoTransition

在两个视频之间添加过渡效果。

![](./assets/14.png)

**参数：**

*   `video1_path`: 第一个视频的文件路径。
*   `video2_path`: 第二个视频的文件路径。
*   `reference_video`: 指定使用哪个视频作为输出分辨率和帧率的参考。
*   `device`: 使用的处理设备（`CPU` 或 `GPU`）。
*   `transition`: 过渡效果的名称。要查看可用过渡的列表，请运行 `ffmpeg -hide_banner -h filter=xfade`。
*   `transition_duration`: 过渡的持续时间（以秒为单位）。
*   `offset`: 第一个视频中过渡的开始时间。
*   `output_path`: 保存输出视频的目录。

---

### 🔥 VideoPlayback

倒放视频。

![](./assets/15.png)

**参数：**

*   `video_path`: 输入视频的文件路径。
*   `output_path`: 保存倒放视频的目录。
*   `reverse_audio`: 是否也倒放音频。

---

### 🔥 Filtergraph

对视频应用原始 FFmpeg 滤镜图。

**参数：**

*   `video`: 输入视频的文件路径。
*   `filtergraph`: FFmpeg 滤镜图字符串。
*   `output_path`: 保存处理后视频的目录。
*   `output_ext`: 输出视频的文件扩展名。

---

### 🔥 StreamMapping

对视频应用流映射。

**参数：**

*   `video`: 输入视频的文件路径。
*   `maps`: FFmpeg 流映射字符串。
*   `output_path`: 保存处理后视频的目录。
*   `output_ext`: 输出视频的文件扩展名。

---

### 🔥 Subtitle

处理字幕的节点。

**参数：**

*   `video`: 输入视频的文件路径。
*   `subtitle_file`: 字幕文件的文件路径。
*   `action`: 要执行的字幕操作（`burn`、`add` 或 `extract`）。
*   `output_path`: 保存处理后视频的目录。
*   `output_ext`: 输出视频的文件扩展名。

---

### 🔥 AudioFilter

对音频流应用原始 FFmpeg 音频滤镜图。

**参数：**

*   `audio`: 输入音频的文件路径。
*   `filtergraph`: FFmpeg 音频滤镜图字符串。
*   `output_path`: 保存处理后音频的目录。
*   `output_ext`: 输出音频的文件扩展名。

---

## 社交媒体

-   **Bilibili:** [我的 Bilibili 主页](https://space.bilibili.com/1303099255)

## 致谢

特别感谢 [FFmpeg](https://github.com/FFmpeg/FFmpeg) 存储库的贡献者。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MoonHugo/ComfyUI-FFmpeg&type=Date)](https://star-history.com/#MoonHugo/ComfyUI-FFmpeg&Date)
