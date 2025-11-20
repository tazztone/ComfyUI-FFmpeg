import sys
import os
import pytest
from unittest.mock import MagicMock
import torch
import shutil
import subprocess

# Mock folder_paths
mock_folder_paths = MagicMock()
sys.modules['folder_paths'] = mock_folder_paths

# Setup output directory mock
temp_output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(temp_output_dir, exist_ok=True)
mock_folder_paths.get_output_directory.return_value = temp_output_dir

# Mock comfy
sys.modules['comfy'] = MagicMock()
sys.modules['comfy.model_management'] = MagicMock()

# Add repo root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nodes.addImgWatermark import AddImgWatermark
from nodes.pipVideo import PictureInPicture
from nodes.mergingVideoByTwo import MergeVideos
from nodes.stitchingVideo import StitchVideos
from nodes.frames2video import Frames2Video
from nodes.addTextWatermark import AddTextWatermark

test_video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'videos', 'test.mp4'))

@pytest.fixture(scope="module")
def setup_environment():
    # Create test video
    os.makedirs(os.path.dirname(test_video_path), exist_ok=True)
    command = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=size=320x240:rate=30',
        '-f', 'lavfi', '-i', 'sine=frequency=1000:duration=1',
        '-c:v', 'libx264', '-c:a', 'aac',
        '-t', '1', test_video_path
    ]
    subprocess.run(command, check=True)
    yield
    # Cleanup
    if os.path.exists(test_video_path):
        os.remove(test_video_path)
    if os.path.exists(temp_output_dir):
        shutil.rmtree(temp_output_dir)

def test_add_img_watermark(setup_environment):
    node = AddImgWatermark()

    # Create a dummy image tensor (1, H, W, C)
    # ComfyUI image tensors are usually (B, H, W, C)
    image_tensor = torch.zeros((1, 100, 100, 3), dtype=torch.float32)

    # Test with tensor
    result = node.add_img_watermark(
        video=test_video_path,
        width=50,
        position_x=10,
        position_y=10,
        watermark_image_tensor=image_tensor
    )
    assert os.path.exists(result[0])

    # Test with path (backward compatibility)
    # Create dummy image file
    img_path = os.path.join(os.path.dirname(test_video_path), 'watermark.png')
    subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=red:s=100x100', '-frames:v', '1', img_path], check=True)

    result_path = node.add_img_watermark(
        video=test_video_path,
        width=50,
        position_x=20,
        position_y=20,
        watermark_image=img_path
    )
    assert os.path.exists(result_path[0])
    os.remove(img_path)

def test_add_text_watermark(setup_environment):
    node = AddTextWatermark()
    result = node.add_text_watermark(
        video=test_video_path,
        text="Test Watermark",
        font_size=24,
        font_color="white",
        position_x=10,
        position_y=10,
        font_file="default"
    )
    assert os.path.exists(result[0])

def test_pip_video(setup_environment):
    node = PictureInPicture()

    # Create a dummy foreground image tensor
    image_tensor = torch.zeros((1, 100, 100, 3), dtype=torch.float32)

    # Test with image foreground
    result = node.create_pip_video(
        background_video=test_video_path,
        position="top_left",
        scale=0.5,
        audio_source="background",
        filename="pip_test.mp4",
        foreground_image=image_tensor
    )
    assert os.path.exists(result[0])

def test_merge_videos(setup_environment):
    node = MergeVideos()
    # Merge same video twice
    result = node.merge_videos(test_video_path, test_video_path, "720p", "merge_test.mp4")
    assert os.path.exists(result[0])

def test_stitch_videos(setup_environment):
    node = StitchVideos()
    result = node.stitch_videos(test_video_path, test_video_path, "horizontal", "video1", "stitch_test.mp4")
    assert os.path.exists(result[0])

def test_frames2video(setup_environment):
    node = Frames2Video()
    # Create dummy frames
    images = torch.rand((5, 64, 64, 3), dtype=torch.float32)
    result = node.frames_to_video(
        images=images,
        fps=24,
        codec="h264_cpu",
        crf=23,
        preset="ultrafast",
        filename="frames_test.mp4"
    )
    assert os.path.exists(result[0])
