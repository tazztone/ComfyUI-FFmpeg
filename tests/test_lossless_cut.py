import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import json
from PIL import Image

# Mock ComfyUI and torch modules
torch_mock = MagicMock()
torch_mock.hub = MagicMock()

sys.modules["folder_paths"] = MagicMock()
sys.modules["torch"] = torch_mock
sys.modules["torchaudio"] = MagicMock()
sys.modules["comfy"] = MagicMock()
sys.modules["comfy.model_management"] = MagicMock()


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
            if f.startswith("lossless_cut_") or f.startswith("losslesscut_data_"):
                try:
                    os.remove(os.path.join("/tmp", f))
                except OSError:
                    pass

    @patch("nodes.LosslessCut.subprocess.run")
    def test_lossless_cut(self, mock_subprocess_run):
        # Mock ffprobe output
        keyframes_output = {
            "streams": [{"duration": "5.0", "r_frame_rate": "30/1"}],
            "packets": [{"pts_time": "0.000000", "flags": "K"}, {"pts_time": "2.000000", "flags": "K"}, {"pts_time": "4.000000", "flags": "K"}]
        }

        # This mock will handle ffprobe and ffmpeg calls
        def subprocess_run_side_effect(*args, **kwargs):
            command = args[0]
            if command[0] == 'ffprobe':
                return MagicMock(stdout=json.dumps(keyframes_output), returncode=0)
            elif command[0] == 'ffmpeg':
                output_path = command[-1]
                with open(output_path, "w") as f:
                    f.write("dummy cut video")
                return MagicMock(returncode=0)
            return MagicMock(returncode=0)

        mock_subprocess_run.side_effect = subprocess_run_side_effect

        with patch('nodes.LosslessCut.folder_paths') as mock_folder_paths:
            mock_folder_paths.get_output_directory.return_value = "/tmp"
            mock_folder_paths.get_temp_directory.return_value = "/tmp"

            # Test metadata extraction and saving
            result = self.node.lossless_cut(
                video=self.video_path,
                action="",
                in_point=1.0,
                out_point=3.0,
                current_position=1.0,
                node_id="test_node"
            )
            metadata_path = "/tmp/losslesscut_data_test_node.json"
            self.assertTrue(os.path.exists(metadata_path))
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            self.assertEqual(metadata["duration"], 5.0)
            self.assertEqual(metadata["fps"], 30.0)
            self.assertEqual(metadata["keyframes"], [0.0, 2.0, 4.0])


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

            # Test next_kf action
            result = self.node.lossless_cut(
                video=self.video_path,
                action="next_kf",
                in_point=0.0,
                out_point=-1.0,
                current_position=0.0
            )
            self.assertIsNone(result["result"][0])
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
            self.assertEqual(result["ui"]["out_point"], 4.0)

if __name__ == "__main__":
    unittest.main()
