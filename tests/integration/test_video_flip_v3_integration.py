import os
import pytest
import asyncio
from unittest.mock import MagicMock, patch

# Import the V3 node
# Note: We rely on the internal class, bypassing the decorator if necessary for raw logic testing,
# but testing the decorated method is better.
# However, the decorator requires 'comfy.nodes.package' which might be mocked in conftest.
from nodes.videoFlip_v3 import VideoFlipV3

# Define path to videos relative to this test file
VIDEO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../videos"))
TEST_VIDEO_PATH = os.path.join(VIDEO_DIR, "test_flip_v3.mp4")


@pytest.fixture(scope="module")
def create_test_video():
    """Create a dummy video file for testing."""
    import subprocess

    os.makedirs(VIDEO_DIR, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "testsrc=size=1280x720:rate=30",
        "-t",
        "1",
        TEST_VIDEO_PATH,
    ]
    subprocess.run(command, check=True)
    yield
    if os.path.exists(TEST_VIDEO_PATH):
        os.remove(TEST_VIDEO_PATH)


@pytest.mark.integration
def test_videoflip_v3_execution(create_test_video):
    """Test the execution of VideoFlipV3."""
    # node = VideoFlipV3() # It's a classmethod, don't need instance really, or can call on class

    # We need to mock folder_paths.get_output_directory since it's used in the node
    # conftest.py should have already mocked 'folder_paths', but let's double check usage.
    # The integration test environment might need the mock to return a valid temp dir.

    # In conftest, we mocked folder_paths.get_output_directory to return 'tmp_output'

    output_filename = "flipped_v3_test.mp4"

    # Call the synchronous execute method
    # It returns io.NodeOutput which is a tuple subclass (via conftest mock)
    # The real V3 implementation returns io.NodeOutput which holds the value.
    # In conftest: class MockNodeOutput(tuple): ...
    # So output_path should be result[0]

    result = VideoFlipV3.execute(
        video=TEST_VIDEO_PATH, flip_type="horizontal", filename=output_filename
    )

    # result is a MockNodeOutput which is a tuple.
    output_path = result[0]

    assert os.path.exists(output_path)
    assert output_filename in output_path

    # Optional: Verify output with ffprobe?
    # For now, existence is enough proof of ffmpeg execution.
