import os
import shutil
import tempfile
import unittest
import sys
from unittest.mock import MagicMock

# --- MOCKING SETUP ---
# Mock ComfyUI modules BEFORE they are imported by func
sys.modules["comfy"] = MagicMock()
sys.modules["comfy.model_management"] = MagicMock()
sys.modules["folder_paths"] = MagicMock()

# Import the functions to test
from func import get_video_files, get_audio_files, get_image_paths_from_directory

class TestFileHelpers(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_video_files_case_insensitive(self):
        # Create files with different cases
        open(os.path.join(self.test_dir, "video1.mp4"), 'a').close()
        open(os.path.join(self.test_dir, "VIDEO2.MP4"), 'a').close()
        open(os.path.join(self.test_dir, "video3.mkv"), 'a').close()
        open(os.path.join(self.test_dir, "not_video.txt"), 'a').close()

        video_files = get_video_files(self.test_dir)
        filenames = [os.path.basename(f) for f in video_files]

        self.assertEqual(len(filenames), 3)
        self.assertIn("video1.mp4", filenames)
        self.assertIn("VIDEO2.MP4", filenames)
        self.assertIn("video3.mkv", filenames)
        self.assertEqual(filenames, sorted(filenames))

    def test_get_audio_files_case_insensitive(self):
        # Create files with different cases
        open(os.path.join(self.test_dir, "audio1.mp3"), 'a').close()
        open(os.path.join(self.test_dir, "AUDIO2.MP3"), 'a').close()
        open(os.path.join(self.test_dir, "audio3.wav"), 'a').close()
        open(os.path.join(self.test_dir, "not_audio.txt"), 'a').close()

        audio_files = get_audio_files(self.test_dir)
        filenames = [os.path.basename(f) for f in audio_files]

        self.assertEqual(len(filenames), 3)
        self.assertIn("audio1.mp3", filenames)
        self.assertIn("AUDIO2.MP3", filenames)
        self.assertIn("audio3.wav", filenames)
        self.assertEqual(filenames, sorted(filenames))

    def test_get_image_paths_length_zero(self):
        # Create image files
        open(os.path.join(self.test_dir, "img1.png"), 'a').close()
        open(os.path.join(self.test_dir, "img2.jpg"), 'a').close()
        open(os.path.join(self.test_dir, "img3.webp"), 'a').close()

        # Test length=0 returns all
        images = get_image_paths_from_directory(self.test_dir, start_index=0, length=0)
        self.assertEqual(len(images), 3)

        # Test length=0 with start_index
        images = get_image_paths_from_directory(self.test_dir, start_index=1, length=0)
        self.assertEqual(len(images), 2)
        filenames = sorted([os.path.basename(f) for f in images])
        self.assertEqual(filenames, ["img2.jpg", "img3.webp"])

        # Test normal length
        images = get_image_paths_from_directory(self.test_dir, start_index=0, length=2)
        self.assertEqual(len(images), 2)

if __name__ == '__main__':
    unittest.main()
