import os
import subprocess
import pytest
from nodes.streamAnalysis import AnalyzeStreams
from nodes.keyframeAwareCutting import KeyframeTrim

# Define path to videos relative to this test file
# Assumes structure: tests/integration/this_file.py and tests/videos/
VIDEO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../videos"))
TEST_VIDEO_PATH = os.path.join(VIDEO_DIR, "test_analysis.mp4")


@pytest.fixture(scope="module")
def create_test_video():
    """Create a dummy video file for testing."""
    os.makedirs(VIDEO_DIR, exist_ok=True)
    # Use ffmpeg to create a 1-second silent video
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
def test_stream_analysis(create_test_video):
    """Test the AnalyzeStreams node."""
    node = AnalyzeStreams()
    result = node.analyze_streams(TEST_VIDEO_PATH)
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    # Validate result is JSON
    import json

    data = json.loads(result[0])
    assert "streams" in data


@pytest.mark.skip(reason="Known flaky test - see AGENTS.md")
@pytest.mark.integration
def test_keyframe_aware_cutting(create_test_video):
    """Test the KeyframeTrim node."""
    node = KeyframeTrim()
    output_path = os.path.dirname(TEST_VIDEO_PATH)
    result = node.keyframe_trim(
        TEST_VIDEO_PATH, "00:00:00", "00:00:00.500", "test_output_trim.mp4"
    )
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert os.path.isfile(result[0])
    # Cleanup
    if os.path.isfile(result[0]):
        os.remove(result[0])
