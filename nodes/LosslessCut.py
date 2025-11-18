import os
import subprocess
import json
from datetime import datetime, timedelta

import os
import subprocess
import json
from datetime import datetime
import folder_paths

class LosslessCut:
    """
    A node to cut a video at the nearest keyframes to the specified start and end times, with an interactive UI.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "action": ("STRING", {"default": "cut"}),
                "in_point": ("FLOAT", {"default": 0.0, "min": 0.0, "step": 0.01}),
                "out_point": ("FLOAT", {"default": -1.0, "min": -1.0, "step": 0.01}),
                "current_position": ("FLOAT", {"default": 0.0, "min": 0.0, "step": 0.01}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING", "IMAGE",)
    FUNCTION = "lossless_cut"
    CATEGORY = "🔥FFmpeg/Editing"

    def _get_keyframes(self, video):
        command = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
            'frame=pkt_pts_time,pict_type', '-of', 'json', video
        ]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        frames = json.loads(result.stdout)['frames']
        return [float(f['pkt_pts_time']) for f in frames if f['pict_type'] == 'I']

    def _find_nearest_keyframe(self, time_sec, keyframes):
        return min(keyframes, key=lambda x: abs(x - time_sec))

    def lossless_cut(self, video, action, in_point, out_point, current_position, prompt=None, extra_pnginfo=None):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        keyframes = self._get_keyframes(video)
        if out_point == -1:
            out_point = keyframes[-1]

        if action == "next_kf":
            current_position = min([kf for kf in keyframes if kf > current_position] or [current_position])
        elif action == "prev_kf":
            current_position = max([kf for kf in keyframes if kf < current_position] or [current_position])
        elif action == "set_in":
            in_point = current_position
        elif action == "set_out":
            out_point = current_position
        elif action == "cut":
            start_keyframe = self._find_nearest_keyframe(in_point, keyframes)
            end_keyframe = self._find_nearest_keyframe(out_point, keyframes)

            if start_keyframe >= end_keyframe:
                raise ValueError("Start time must be before end time.")

            filename = f"lossless_cut_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            output_path = os.path.join(folder_paths.get_output_directory(), filename)

            command = [
                'ffmpeg', '-y', '-i', video, '-ss', str(start_keyframe),
                '-to', str(end_keyframe), '-c', 'copy', output_path
            ]
            subprocess.run(command, check=True)
            return {"result": (output_path, None), "ui": {"in_point": in_point, "out_point": out_point, "current_position": current_position, "keyframes": keyframes}}

        # Generate a preview frame
        preview_image = self._generate_preview(video, current_position)

        return {"result": (None, preview_image), "ui": {"in_point": in_point, "out_point": out_point, "current_position": current_position, "keyframes": keyframes}}

    def _generate_preview(self, video, time_sec):
        import numpy as np
        from PIL import Image
        import torch

        output_path = os.path.join(folder_paths.get_temp_directory(), f"preview_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
        command = [
            'ffmpeg', '-y', '-i', video, '-ss', str(time_sec),
            '-vframes', '1', output_path
        ]
        subprocess.run(command, check=True, capture_output=True)

        i = Image.open(output_path)
        i = i.convert("RGB")
        image = np.array(i).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        return image
