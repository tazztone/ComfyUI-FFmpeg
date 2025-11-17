import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nodes.losslesscut import LosslessCutLogic

test_video_path = "/tmp/test_video.mp4"

@pytest.fixture
def logic_instance():
    """Provides a LosslessCutLogic instance with mocked keyframes."""
    logic = LosslessCutLogic()

    def mock_get_keyframes(video_path):
        keyframes = [0.0, 1.5, 3.0, 4.5, 6.0]
        logic.keyframes = keyframes
        return keyframes

    with patch.object(logic, 'get_keyframes', side_effect=mock_get_keyframes):
        yield logic

def test_initial_state(logic_instance):
    """Test the initial state when a new video is loaded."""
    in_point, out_point, current_position, _ = logic_instance.process_event(test_video_path, "", -1.0, -1.0, -1.0, None)
    assert in_point == 0.0
    assert out_point == 6.0
    assert current_position == 0.0

def test_keyframe_navigation(logic_instance):
    """Test next and previous keyframe navigation."""
    in_point, out_point, current_position, video_path_ = logic_instance.process_event(test_video_path, "", -1.0, -1.0, -1.0, None)

    _, _, current_position, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "next_kf")
    assert current_position == 1.5

    _, _, current_position, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "next_kf")
    assert current_position == 3.0

    _, _, current_position, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "prev_kf")
    assert current_position == 1.5

def test_set_points(logic_instance):
    """Test setting in and out points."""
    in_point, out_point, current_position, video_path_ = logic_instance.process_event(test_video_path, "", -1.0, -1.0, -1.0, None)

    current_position = 1.5
    in_point, out_point, current_position, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "set_in")
    assert in_point == 1.5

    current_position = 4.5
    in_point, out_point, current_position, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "set_out")
    assert out_point == 4.5

def test_invalid_point_setting(logic_instance):
    """Test invalid in/out point settings."""
    logic_instance.process_event(test_video_path, "", -1.0, -1.0, -1.0, None)
    in_point, out_point, current_position, video_path_ = 1.5, 4.5, 1.5, test_video_path

    current_position = 5.0
    new_in_point, _, _, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "set_in")
    assert new_in_point == in_point

    current_position = 1.0
    _, new_out_point, _, _ = logic_instance.process_event(test_video_path, video_path_, in_point, out_point, current_position, "set_out")
    assert new_out_point == out_point
