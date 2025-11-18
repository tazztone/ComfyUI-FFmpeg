import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import json
from PIL import Image

# Mock ComfyUI modules
sys.modules["folder_paths"] = MagicMock()
sys.modules["torch"] = MagicMock()

from nodes.LosslessCut import LosslessCut

class TestLosslessCut(unittest.TestCase):
    def setUp(self):
        self.node = LosslessCut()
        self.video_path = "tests/videos/test_video.mp4"
        # Create a dummy video file for testing
        os.makedirs(os.path.dirname(self.video_path), exist_ok=True)
        with open(self.video_path, "w") as f:
            f.write("dummy video data")

    def tearDown(self):
        if os.path.exists(self.video_path):
            os.remove(self.video_path)
        # Clean up any created files during tests
        for f in os.listdir("/tmp"):
            if f.startswith("lossless_cut_") or f.startswith("preview_"):
                try:
                    os.remove(os.path.join("/tmp", f))
                except OSError:
                    pass

    @patch("nodes.LosslessCut.subprocess.run")
    def test_lossless_cut(self, mock_subprocess_run):
        # Mock ffprobe output
        keyframes_output = {"frames": [{"pkt_pts_time": "0.000000", "pict_type": "I"}, {"pkt_pts_time": "2.000000", "pict_type": "I"}, {"pkt_pts_time": "4.000000", "pict_type": "I"}]}

        # This mock will handle ffprobe and ffmpeg calls
        def subprocess_run_side_effect(*args, **kwargs):
            command = args[0]
            if command[0] == 'ffprobe':
                return MagicMock(stdout=json.dumps(keyframes_output))
            elif command[0] == 'ffmpeg':
                output_path = command[-1]
                if "-vframes" in command: # Preview generation
                    # Create a dummy PNG file
                    img = Image.new('RGB', (10, 10), color = 'red')
                    img.save(output_path, 'PNG')
                else: # Cut operation
                    with open(output_path, "w") as f:
                        f.write("dummy cut video")
                return MagicMock(returncode=0)
            return MagicMock(returncode=0)

        mock_subprocess_run.side_effect = subprocess_run_side_effect

        with patch('nodes.LosslessCut.folder_paths') as mock_folder_paths:
            mock_folder_paths.get_output_directory.return_value = "/tmp"
            mock_folder_paths.get_temp_directory.return_value = "/tmp"

            # Test cut action
            result = self.node.lossless_cut(
                video=self.video_path,
                action="cut",
                in_point=1.0,
                out_point=3.0,
                current_position=1.0
            )
            self.assertTrue(result["result"][0].startswith("/tmp/lossless_cut_"))
            self.assertTrue(os.path.exists(result["result"][0]))
            self.assertIsNone(result["result"][1])

            # Test next_kf action
            result = self.node.lossless_cut(
                video=self.video_path,
                action="next_kf",
                in_point=0.0,
                out_point=-1.0,
                current_position=0.0
            )
            self.assertIsNone(result["result"][0])
            self.assertIsNotNone(result["result"][1])
            self.assertEqual(result["ui"]["current_position"], 2.0)

            # Test prev_kf action
            result = self.node.lossless_cut(
                video=self.video_path,
                action="prev_kf",
                in_point=0.0,
                out_point=-1.0,
                current_position=4.0
            )
            self.assertIsNone(result["result"][0])
            self.assertIsNotNone(result["result"][1])
            self.assertEqual(result["ui"]["current_position"], 2.0)

            # Test set_in action
            result = self.node.lossless_cut(
                video=self.video_path,
                action="set_in",
                in_point=0.0,
                out_point=-1.0,
                current_position=2.0
            )
            self.assertIsNone(result["result"][0])
            self.assertIsNotNone(result["result"][1])
            self.assertEqual(result["ui"]["in_point"], 2.0)

            # Test set_out action
            result = self.node.lossless_cut(
                video=self.video_path,
                action="set_out",
                in_point=0.0,
                out_point=-1.0,
                current_position=4.0
            )
            self.assertIsNone(result["result"][0])
            self.assertIsNotNone(result["result"][1])
            self.assertEqual(result["ui"]["out_point"], 4.0)

if __name__ == "__main__":
    unittest.main()
