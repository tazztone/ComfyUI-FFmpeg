import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import json
import pytest

from nodes.LosslessCut import LosslessCut


class TestLosslessCut(unittest.TestCase):
    def setUp(self):
        self.node = LosslessCut()

        # Setup video path
        self.video_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../videos")
        )
        os.makedirs(self.video_dir, exist_ok=True)
        self.video_path = os.path.join(self.video_dir, "test_lossless.mp4")

        # Create a dummy video file for testing
        with open(self.video_path, "w") as f:
            f.write("dummy video data")

    def tearDown(self):
        if os.path.exists(self.video_path):
            os.remove(self.video_path)

    @pytest.mark.integration
    @patch("nodes.LosslessCut.subprocess.run")
    def test_lossless_cut(self, mock_subprocess_run):
        # Mock ffprobe output
        keyframes_output = {
            "streams": [{"duration": "5.0", "r_frame_rate": "30/1"}],
            "packets": [
                {"pts_time": "0.000000", "flags": "K"},
                {"pts_time": "2.000000", "flags": "K"},
                {"pts_time": "4.000000", "flags": "K"},
            ],
        }

        # This mock will handle ffprobe and ffmpeg calls
        def subprocess_run_side_effect(*args, **kwargs):
            command = args[0]
            if len(command) > 0 and command[0] == "ffprobe":
                return MagicMock(stdout=json.dumps(keyframes_output), returncode=0)
            elif len(command) > 0 and command[0] == "ffmpeg":
                output_path = command[-1]
                # Ensure dir exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w") as f:
                    f.write("dummy cut video")
                return MagicMock(returncode=0)
            return MagicMock(returncode=0)

        mock_subprocess_run.side_effect = subprocess_run_side_effect

        # We don't need to mock folder_paths here IF conftest.py did its job,
        # but LosslessCut might use it in a way that needs specific method mocks not in conftest?
        # conftest mocks get_output_directory and get_temp_directory.
        # Let's see what LosslessCut uses. It likely uses folder_paths.get_output_directory()

        # Execute logic
        result = self.node.lossless_cut(
            video=self.video_path,
            action="",
            in_point=1.0,
            out_point=3.0,
            current_position=1.0,
            node_id="test_node",
        )

        # Check metadata file
        # Note: conftest sets temp dir to tests/tmp_temp
        # We need to find where the file was actually written.
        # LosslessCut usually uses folder_paths.get_temp_directory()
        # In conftest, we set it to 'tmp_temp'

        # We can inspect the calls if needed, or check the file system.
        # However, to retain the original test logic which asserted file existence,
        # we rely on the mocked folder_paths returning a predictable path.

        # The previous test mocked folder_paths locally. The conftest global mock is essentially the same.
        # But we need to know the path to check.
        # Import folder_paths to get the path
        import folder_paths

        temp_dir = folder_paths.get_temp_directory()
        output_dir = folder_paths.get_output_directory()
        metadata_path = os.path.join(temp_dir, "losslesscut_data_test_node.json")

        self.assertTrue(os.path.exists(metadata_path))
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertEqual(metadata["duration"], 5.0)
        self.assertEqual(metadata["keyframes"], [0.0, 2.0, 4.0])

        # Test cut action
        result = self.node.lossless_cut(
            video=self.video_path,
            action="cut",
            in_point=1.0,
            out_point=3.0,
            current_position=1.0,
        )
        self.assertTrue(
            result["result"][0].startswith(os.path.join(output_dir, "lossless_cut_"))
        )
        self.assertTrue(os.path.exists(result["result"][0]))

        # Test next_kf action
        result = self.node.lossless_cut(
            video=self.video_path,
            action="next_kf",
            in_point=0.0,
            out_point=-1.0,
            current_position=0.0,
        )
        self.assertIsNone(result["result"][0])
        self.assertEqual(result["ui"]["current_position"], 2.0)


if __name__ == "__main__":
    unittest.main()
