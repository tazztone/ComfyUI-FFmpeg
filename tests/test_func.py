import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock

# Mock the comfy and folder_paths modules
sys.modules['comfy'] = MagicMock()
sys.modules['comfy.model_management'] = MagicMock()
sys.modules['folder_paths'] = MagicMock()

from func import validate_time_format, set_file_name, generate_template_string, video_type, audio_type, clear_memory


def test_validate_time_format():
    assert validate_time_format("12:34:56") == True
    assert validate_time_format("01:02:03") == True
    assert validate_time_format("23:59:59") == True
    assert validate_time_format("00:00:00") == True
    assert validate_time_format("24:00:00") == False
    assert validate_time_format("12:60:00") == False
    assert validate_time_format("12:34:60") == False
    assert validate_time_format("12:34") == False
    assert validate_time_format("12:34:56:78") == False
    assert validate_time_format("abc") == False
    assert validate_time_format("") == False
    assert validate_time_format("1:2:3") == False

@patch('func.time')
def test_set_file_name(mock_time):
    mock_time.localtime.return_value = "localtime_return"
    mock_time.strftime.return_value = "20250101000000"

    video_path = "/path/to/video.mp4"
    new_filename = set_file_name(video_path)
    assert new_filename == "20250101000000.mp4"
    mock_time.localtime.assert_called_once()
    mock_time.strftime.assert_called_once_with("%Y%m%d%H%M%S", "localtime_return")

def test_generate_template_string():
    assert generate_template_string("frame123.jpg") == "frame%03d.jpg"
    assert generate_template_string("img_001.png") == "img_%03d.png"
    assert generate_template_string("image_1.tif") == "image_%01d.tif"
    assert generate_template_string("no_digits.jpg") == "no_digits.jpg"
    assert generate_template_string("file0000.exr") == "file%04d.exr"

def test_video_type():
    types = video_type()
    assert isinstance(types, tuple)
    assert len(types) > 0
    for t in types:
        assert t.startswith('.')
    assert '.mp4' in types
    assert '.avi' in types
    assert '.mov' in types

def test_audio_type():
    types = audio_type()
    assert isinstance(types, tuple)
    assert len(types) > 0
    for t in types:
        assert t.startswith('.')
    assert '.mp3' in types
    assert '.wav' in types
    assert '.aac' in types

@patch('func.gc')
@patch('func.unload_all_models')
@patch('func.soft_empty_cache')
def test_clear_memory(mock_soft_empty_cache, mock_unload_all_models, mock_gc):
    clear_memory()
    mock_gc.collect.assert_called_once()
    mock_unload_all_models.assert_called_once()
    mock_soft_empty_cache.assert_called_once()
