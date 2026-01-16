import sys
import os
import pytest
import torch
import shutil
import subprocess

# Note: conftest.py handles basic folder_paths mocking

from nodes.addImgWatermark import AddImgWatermark
from nodes.pipVideo import PictureInPicture
from nodes.mergingVideoByTwo import MergeVideos
from nodes.stitchingVideo import StitchVideos
from nodes.frames2video import Frames2Video
from nodes.addTextWatermark import AddTextWatermark

# Setup paths
VIDEO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../videos"))
TEST_VIDEO_PATH = os.path.join(VIDEO_DIR, "test_general.mp4")


@pytest.fixture(scope="module")
def setup_environment():
    # Create test video with audio
    os.makedirs(VIDEO_DIR, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=320x240:rate=30",
        "-f",
        "lavfi",
        "-i",
        "sine=frequency=1000:duration=1",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-t",
        "1",
        TEST_VIDEO_PATH,
    ]
    subprocess.run(command, check=True)
    yield
    # Cleanup
    if os.path.exists(TEST_VIDEO_PATH):
        os.remove(TEST_VIDEO_PATH)


@pytest.mark.integration
def test_add_img_watermark(setup_environment):
    node = AddImgWatermark()

    # Create a dummy image tensor (1, H, W, C)
    image_tensor = torch.zeros((1, 100, 100, 3), dtype=torch.float32)

    # Test with tensor
    result = node.add_img_watermark(
        video=TEST_VIDEO_PATH,
        width=50,
        position_x=10,
        position_y=10,
        watermark_image_tensor=image_tensor,
    )
    assert os.path.exists(result[0])

    # Test with path (backward compatibility)
    # Create dummy image file
    img_path = os.path.join(VIDEO_DIR, "watermark.png")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=red:s=100x100",
            "-frames:v",
            "1",
            img_path,
        ],
        check=True,
    )

    result_path = node.add_img_watermark(
        video=TEST_VIDEO_PATH,
        width=50,
        position_x=20,
        position_y=20,
        watermark_image=img_path,
    )
    assert os.path.exists(result_path[0])
    os.remove(img_path)


@pytest.mark.integration
def test_add_text_watermark(setup_environment):
    node = AddTextWatermark()
    # Note: depends on fonts usually, defaulting to a system font or provided default might fail if not found
    # But let's assume 'default' or similar works or the node handles it.
    try:
        result = node.add_text_watermark(
            video=TEST_VIDEO_PATH,
            text="Test Watermark",
            font_size=24,
            font_color="white",
            position_x=10,
            position_y=10,
            font_file="default",
        )
        assert os.path.exists(result[0])
    except Exception as e:
        # If font missing, we might skip or fail.
        # Just re-raising for now to see failure if it happens.
        raise e


@pytest.mark.integration
def test_pip_video(setup_environment):
    node = PictureInPicture()

    # Create a dummy foreground image tensor
    image_tensor = torch.zeros((1, 100, 100, 3), dtype=torch.float32)

    # Test with image foreground
    result = node.create_pip_video(
        background_video=TEST_VIDEO_PATH,
        position="top_left",
        scale=0.5,
        audio_source="background",
        filename="pip_test.mp4",
        foreground_image=image_tensor,
    )
    assert os.path.exists(result[0])


@pytest.mark.integration
def test_merge_videos(setup_environment):
    node = MergeVideos()
    # Merge same video twice
    result = node.merge_videos(
        TEST_VIDEO_PATH, TEST_VIDEO_PATH, "720p", "merge_test.mp4"
    )
    assert os.path.exists(result[0])


@pytest.mark.integration
def test_stitch_videos(setup_environment):
    node = StitchVideos()
    result = node.stitch_videos(
        TEST_VIDEO_PATH, TEST_VIDEO_PATH, "horizontal", "video1", "stitch_test.mp4"
    )
    assert os.path.exists(result[0])


@pytest.mark.integration
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
        filename="frames_test.mp4",
    )
    assert os.path.exists(result[0])
