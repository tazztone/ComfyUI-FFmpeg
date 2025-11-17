import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import subprocess
import pytest
from unittest.mock import patch, MagicMock

# Mock the comfy and folder_paths modules
sys.modules['comfy'] = MagicMock()
sys.modules['comfy.model_management'] = MagicMock()
sys.modules['folder_paths'] = MagicMock()

from nodes.streamAnalysis import AnalyzeStreams
from nodes.keyframeAwareCutting import KeyframeTrim

# Mock video path for testing
test_video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'videos', 'test.mp4'))

@pytest.fixture(scope="module")
def create_test_video():
    """Create a dummy video file for testing."""
    os.makedirs(os.path.dirname(test_video_path), exist_ok=True)
    # Use ffmpeg to create a 1-second silent video
    command = [
        'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=size=1280x720:rate=30',
        '-t', '1', test_video_path
    ]
    subprocess.run(command, check=True)
    yield
    os.remove(test_video_path)

def test_stream_analysis(create_test_video):
    """Test the AnalyzeStreams node."""
    node = AnalyzeStreams()
    result = node.analyze_streams(test_video_path)
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    # You can add more assertions here to validate the content of the stream info

def test_keyframe_aware_cutting(create_test_video):
    """Test the KeyframeTrim node."""
    node = KeyframeTrim()
    output_path = os.path.dirname(test_video_path)
    result = node.keyframe_trim(test_video_path, "00:00:00", "00:00:01", "test_output.mp4")
    assert isinstance(result, tuple)
    assert isinstance(result[0], str)
    assert os.path.isfile(result[0])
    os.remove(result[0])
