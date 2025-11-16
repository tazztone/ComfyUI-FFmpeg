import sys
import unittest
from unittest.mock import MagicMock

# Mock the comfy module before importing func
sys.modules['comfy'] = MagicMock()
sys.modules['comfy.model_management'] = MagicMock()

import os
import shutil
from func import *

class TestFunc(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_temp'
        os.makedirs(self.test_dir, exist_ok=True)
        self.video_with_audio = 'tests/videos/video_with_audio.mp4'
        self.video_without_audio = 'tests/videos/video_without_audio.mp4'
        self.test_image = 'tests/videos/test_image.jpg'

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        # Reset mocks
        sys.modules['comfy.model_management'].reset_mock()

    def test_get_xfade_transitions(self):
        transitions = get_xfade_transitions()
        self.assertIsInstance(transitions, list)
        self.assertGreater(len(transitions), 0)

    def test_copy_image(self):
        dest_path = copy_image(self.test_image, self.test_dir)
        self.assertTrue(os.path.exists(dest_path))

    def test_copy_images_to_directory(self):
        image_paths = [self.test_image] * 3
        dest_paths = copy_images_to_directory(image_paths, self.test_dir)
        self.assertEqual(len(dest_paths), 3)
        for path in dest_paths:
            self.assertTrue(os.path.exists(path))

    def test_get_image_paths_from_directory(self):
        shutil.copy(self.test_image, self.test_dir)
        image_paths = get_image_paths_from_directory(self.test_dir, 0, 1)
        self.assertEqual(len(image_paths), 1)

    def test_generate_template_string(self):
        template = generate_template_string('frame_001.png')
        self.assertEqual(template, 'frame_%03d.png')

    def test_get_video_info(self):
        video_info = getVideoInfo(self.video_with_audio)
        self.assertIn('fps', video_info)
        self.assertIn('width', video_info)
        self.assertIn('height', video_info)
        self.assertIn('duration', video_info)

    def test_get_image_size(self):
        width, height = get_image_size(self.test_image)
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

    def test_has_audio(self):
        self.assertTrue(has_audio(self.video_with_audio))
        self.assertFalse(has_audio(self.video_without_audio))

    def test_set_file_name(self):
        new_name = set_file_name('test.mp4')
        self.assertNotEqual(new_name, 'test.mp4')

    def test_validate_time_format(self):
        self.assertTrue(validate_time_format('12:34:56'))
        self.assertFalse(validate_time_format('12:34'))

    def test_get_video_files(self):
        shutil.copy(self.video_with_audio, self.test_dir)
        video_files = get_video_files(self.test_dir)
        self.assertEqual(len(video_files), 1)

    def test_clear_memory(self):
        clear_memory()
        sys.modules['comfy.model_management'].unload_all_models.assert_called_once()
        sys.modules['comfy.model_management'].soft_empty_cache.assert_called_once()

if __name__ == '__main__':
    unittest.main()
