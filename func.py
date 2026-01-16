import numpy as np
from PIL import Image
import torch
import subprocess
import json
import re
import os
import gc
import shutil
import time
import glob
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from comfy.model_management import unload_all_models, soft_empty_cache

_xfade_transitions_cache = None


def get_xfade_transitions():
    """Retrieves a list of available FFmpeg xfade transitions.

    This function executes the `ffmpeg -h filter=xfade` command to get a list
    of supported cross-fade transitions. It then parses the output to extract
    the transition names.

    Returns:
        list: A sorted list of available xfade transition names. If FFmpeg is
              not found or an error occurs, it returns an empty list.
    """
    global _xfade_transitions_cache
    if _xfade_transitions_cache is not None:
        return _xfade_transitions_cache
    try:
        # 执行命令：ffmpeg -hide_banner -h filter=xfade 查看可用的转场效果，执行ffmpeg命令获取xfade过滤器帮助信息
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-h", "filter=xfade"],
            capture_output=True,
            text=True,
            check=True,
        )

        # 命令输出在stderr中
        output = result.stdout if result.stdout else result.stderr
        # 使用正则表达式匹配所有transition行
        pattern = r"^\s*(\w+)\s+-?\d+\b"
        data = output.split("\n")
        if len(data) == 0:
            transitions = [
                "fade",
                "wipeleft",
                "wiperight",
                "wipeup",
                "wipedown",
                "slideleft",
                "slideright",
                "slideup",
                "slidedown",
                "circlecrop",
                "rectcrop",
                "distance",
                "fadeblack",
                "fadewhite",
                "radial",
                "smoothleft",
                "smoothright",
                "smoothup",
                "smoothdown",
                "circleopen",
                "circleclose",
                "vertopen",
                "vertclose",
                "horzopen",
                "horzclose",
                "dissolve",
                "pixelize",
                "diagtl",
                "diagtr",
                "diagbl",
                "diagbr",
                "hlslice",
                "hrslice",
                "vuslice",
                "vdslice",
                "hblur",
                "fadegrays",
                "wipetl",
                "wipetr",
                "wipebl",
                "wipebr",
                "squeezeh",
                "squeezev",
                "zoomin",
                "fadefast",
                "fadeslow",
                "hlwind",
                "hrwind",
                "vuwind",
                "vdwind",
                "coverleft",
                "coverright",
                "coverup",
                "coverdown",
                "revealleft",
                "revealright",
                "revealup",
                "revealdown",
            ]  # 如果没有找到任何transition，使用默认的
        else:
            transitions = []
            for line in data:
                match = re.search(pattern, line)
                if match and match.group(1) != "none" and match.group(1) != "custom":
                    transitions.append(match.group(1))

        _xfade_transitions_cache = sorted(transitions)
        return _xfade_transitions_cache

    except subprocess.CalledProcessError as e:
        logging.error(f"执行ffmpeg命令出错: {e}")
        logging.error(f"错误输出: {e.stderr}")
        return []
    except FileNotFoundError:
        logging.error("错误: 找不到ffmpeg程序，请确保ffmpeg已安装并添加到系统PATH")
        return []


def copy_image(image_path, destination_directory):
    """Copies a single image to a destination directory.

    Args:
        image_path (str): The path to the image file.
        destination_directory (str): The directory to copy the image to.

    Returns:
        str: The path to the copied image, or None if an error occurred.
    """
    try:
        # 获取图片文件名
        image_name = os.path.basename(image_path)
        # 构建目标路径
        destination_path = os.path.join(destination_directory, image_name)
        # 检查目标路径是否已有相同文件，避免重复复制
        if not os.path.exists(destination_path):
            shutil.copy(image_path, destination_path)
        return destination_path
    except Exception as e:
        logging.error(f"Error copying image {image_path}: {e}")
        return None


def copy_images_to_directory(image_paths, destination_directory):
    """Copies a list of images to a destination directory in parallel.

    Args:
        image_paths (list): A list of paths to the image files.
        destination_directory (str): The directory to copy the images to.

    Returns:
        list: A list of paths to the copied images.
    """
    # 如果目标目录不存在，创建它
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # 使用字典来保持原始索引与路径的对应关系
    index_to_path = {i: image_path for i, image_path in enumerate(image_paths)}
    copied_paths = [None] * len(image_paths)

    # 使用多线程并行复制图片
    with ThreadPoolExecutor() as executor:
        # 提交所有任务
        futures = {
            executor.submit(copy_image, image_path, destination_directory): i
            for i, image_path in index_to_path.items()
        }

        # 等待所有任务完成并按顺序存储结果
        for future in as_completed(futures):
            index = futures[future]
            result = future.result()
            if result is not None:
                copied_paths[index] = result

    # 返回按原始顺序排列的新路径
    return [path for path in copied_paths if path is not None]


def get_image_paths_from_directory(directory, start_index, length):
    """Gets a specified number of image paths from a directory.

    Args:
        directory (str): The directory to get the image paths from.
        start_index (int): The starting index of the images to get.
        length (int): The number of images to get.

    Returns:
        list: A list of image paths.
    """
    image_extensions = get_image_extensions()

    # 创建排序后的文件生成器，直接在生成器中过滤
    def image_generator():
        for filename in sorted(os.listdir(directory)):
            if os.path.splitext(filename)[1].lower() in image_extensions:
                yield os.path.join(directory, filename)

    # 使用islice获取所需的图像路径
    selected_images = islice(image_generator(), start_index, start_index + length)

    return list(selected_images)


def generate_template_string(filename):
    """Generates a template string for FFmpeg based on a filename.

    This function takes a filename and replaces the first sequence of digits
    with a C-style format specifier (e.g., `%03d`).

    Args:
        filename (str): The filename to generate the template string from.

    Returns:
        str: The generated template string.
    """
    match = re.search(r"\d+", filename)
    return (
        re.sub(r"\d+", lambda x: f"%0{len(x.group())}d", filename)
        if match
        else filename
    )


def tensor2pil(image):
    """Converts a tensor to a PIL image.

    Args:
        image (torch.Tensor): The tensor to convert.

    Returns:
        PIL.Image.Image: The converted PIL image.
    """
    return Image.fromarray(
        np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
    )


def pil2tensor(image):
    """Converts a PIL image to a tensor.

    Args:
        image (PIL.Image.Image): The PIL image to convert.

    Returns:
        torch.Tensor: The converted tensor.
    """
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


def getVideoInfo(video_path):
    """Gets information about a video file.

    This function uses `ffprobe` to get the video's FPS, width, height, and
    duration.

    Args:
        video_path (str): The path to the video file.

    Returns:
        dict: A dictionary containing the video's information, or an empty
              dictionary if an error occurred.
    """
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=avg_frame_rate,duration,width,height",
        "-of",
        "json",
        video_path,
    ]
    # 运行ffprobe命令
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # 将输出转化为字符串
    output = result.stdout.decode("utf-8").strip()

    if not output:
        logging.error(f"FFprobe returned empty output for file: {video_path}")
        return {}

    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing FFprobe output: {e}\nOutput was: {output}")
        return {}
    # 查找视频流信息
    if "streams" in data and len(data["streams"]) > 0:
        stream = data["streams"][0]  # 获取第一个视频流
        fps = stream.get("avg_frame_rate")
        if fps is not None:
            # 帧率可能是一个分数形式的字符串，例如 "30/1" 或 "20.233000"
            if "/" in fps:
                num, denom = map(int, fps.split("/"))
                fps = num / denom
            else:
                fps = float(fps)  # 直接转换为浮点数
            width = int(stream.get("width"))
            height = int(stream.get("height"))
            duration = float(stream.get("duration"))
            return_data = {
                "fps": fps,
                "width": width,
                "height": height,
                "duration": duration,
            }
    else:
        return_data = {}
    return return_data


def get_image_size(image_path):
    """Gets the size of an image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        tuple: A tuple containing the width and height of the image.
    """
    # 打开图像文件
    with Image.open(image_path) as img:
        # 获取图像的宽度和高度
        width, height = img.size
        return width, height


def has_audio(video_path):
    """Checks if a video file has an audio stream.

    Args:
        video_path (str): The path to the video file.

    Returns:
        bool: True if the video has an audio stream, False otherwise.
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_path,
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip() == "audio"


def set_file_name(video_path):
    """Generates a new filename based on the current timestamp.

    Args:
        video_path (str): The original path of the video file.

    Returns:
        str: The new filename.
    """
    file_name = os.path.basename(video_path)
    file_extension = os.path.splitext(file_name)[1]
    # 文件名根据年月日时分秒来命名
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_extension
    return file_name


def get_image_extensions():
    """Returns a set of supported image file extensions.

    Returns:
        set: A set of image file extensions.
    """
    return {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def video_type():
    """Returns a tuple of supported video file extensions.

    Returns:
        tuple: A tuple of video file extensions.
    """
    return (".mp4", ".avi", ".mov", ".mkv", ".rmvb", ".wmv", ".flv", ".webm")


def audio_type():
    """Returns a tuple of supported audio file extensions.

    Returns:
        tuple: A tuple of audio file extensions.
    """
    return (
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".m4a",
        ".wma",
        ".ogg",
        ".amr",
        ".ape",
        ".ac3",
        ".aiff",
        ".opus",
        ".m4b",
        ".caf",
        ".dts",
    )


def validate_time_format(time_str):
    """Validates a time string in HH:MM:SS format.

    Args:
        time_str (str): The time string to validate.

    Returns:
        bool: True if the time string is valid, False otherwise.
    """
    pattern = r"^([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$"
    return bool(re.match(pattern, time_str))


def get_video_files(directory):
    """Gets all video files from a directory.

    Args:
        directory (str): The directory to get the video files from.

    Returns:
        list: A sorted list of video file paths.
    """

    # TODO: Centralize extension definitions with video_type() and audio_type() to avoid inconsistency
    # video_extensions = ["*.mp4", "*.avi", "*.mov", "*.mkv", "*.rmvb", "*.wmv", "*.flv"]
    video_extensions = [f"*{ext}" for ext in video_type()]
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(directory, ext)))
    # 排序文件名
    video_files.sort()
    return video_files


def save_image(image, path):
    """Saves an image to a specified path.

    Args:
        image (torch.Tensor): The image tensor to save.
        path (str): The path to save the image to.
    """
    tensor2pil(image).save(path)


def clear_memory():
    """Clears the GPU memory."""
    gc.collect()
    unload_all_models()
    soft_empty_cache()


def save_tensor_to_temp_file(image_tensor, prefix="temp_image", extension=".png"):
    """Saves a ComfyUI IMAGE tensor to a temporary file.

    Args:
        image_tensor: ComfyUI IMAGE tensor (single image)
        prefix: Filename prefix
        extension: File extension (.png, .jpg, etc.)

    Returns:
        str: Path to the temporary file
    """
    import tempfile

    temp_dir = tempfile.gettempdir()
    timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    temp_path = os.path.join(temp_dir, f"{prefix}_{timestamp}{extension}")
    tensor2pil(image_tensor).save(temp_path)
    return temp_path


def validate_file_exists(file_path, file_type="file"):
    """Validates that a file exists and raises appropriate error.

    Args:
        file_path: Path to validate
        file_type: Description of file type for error message

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_type.capitalize()} file not found: {file_path}")
    return True


def get_output_path(filename, prefix="", suffix=""):
    """Generates a standardized output path in ComfyUI's output directory.

    Args:
        filename: Base filename
        prefix: Optional prefix to add
        suffix: Optional suffix to add (before extension)

    Returns:
        str: Full output path
    """
    import folder_paths

    base, ext = os.path.splitext(filename)
    new_filename = f"{prefix}{base}{suffix}{ext}" if prefix or suffix else filename
    return os.path.join(folder_paths.get_output_directory(), new_filename)
