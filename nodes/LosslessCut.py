import os
import subprocess
import json
from datetime import datetime
import folder_paths

class LosslessCut:
    """
    A node to cut a video at the nearest keyframes to the specified start and end times, with an interactive UI.
    """
    WEB_DIRECTORY = "web"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "action": ("STRING", {"default": ""}),
                "in_point": ("FLOAT", {"default": 0.0, "min": 0.0, "step": 0.01}),
                "out_point": ("FLOAT", {"default": -1.0, "min": -1.0, "step": 0.01}),
                "current_position": ("FLOAT", {"default": 0.0, "min": 0.0, "step": 0.01}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "node_id": ("STRING", {"default": "0"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "lossless_cut"
    CATEGORY = "🔥FFmpeg/Editing"

    def extract_video_metadata(self, video_path):
        """Extracts video metadata using ffprobe."""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=duration,r_frame_rate',
            '-show_entries', 'packet=pts_time,flags',
            '-of', 'json',
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)

        keyframes = []
        if 'packets' in data:
            for packet in data.get('packets', []):
                if 'K' in packet.get('flags', ''):
                    keyframes.append(float(packet['pts_time']))

        fps_str = data['streams'][0]['r_frame_rate']
        num, den = map(int, fps_str.split('/'))
        fps = num / den

        metadata = {
            'duration': float(data['streams'][0]['duration']),
            'fps': fps,
            'keyframes': keyframes
        }
        return metadata

    def save_metadata_for_web(self, metadata, node_id):
        """Saves metadata to a JSON file for the web UI."""
        temp_dir = folder_paths.get_temp_directory()
        temp_file = os.path.join(temp_dir, f"losslesscut_data_{node_id}.json")
        with open(temp_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def lossless_cut(self, video, action, in_point, out_point, current_position, node_id="0", prompt=None, extra_pnginfo=None):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        metadata = self.extract_video_metadata(video)
        self.save_metadata_for_web(metadata, node_id)

        keyframes = metadata['keyframes']
        if out_point == -1:
            out_point = keyframes[-1] if keyframes else 0

        if action == "next_kf":
            current_position = min([kf for kf in keyframes if kf > current_position] or [current_position])
        elif action == "prev_kf":
            current_position = max([kf for kf in keyframes if kf < current_position] or [current_position])
        elif action == "set_in":
            in_point = current_position
        elif action == "set_out":
            out_point = current_position
        elif action == "cut":
            start_keyframe = min(keyframes, key=lambda x: abs(x - in_point))
            end_keyframe = min(keyframes, key=lambda x: abs(x - out_point))

            if start_keyframe >= end_keyframe:
                raise ValueError("Start time must be before end time.")

            filename = f"lossless_cut_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            output_path = os.path.join(folder_paths.get_output_directory(), filename)

            command = [
                'ffmpeg', '-y', '-i', video, '-ss', str(start_keyframe),
                '-to', str(end_keyframe), '-c', 'copy', output_path
            ]
            subprocess.run(command, check=True)
            return {"result": (output_path,), "ui": {"in_point": in_point, "out_point": out_point, "current_position": current_position}}

        return {"result": (None,), "ui": {"in_point": in_point, "out_point": out_point, "current_position": current_position}}
