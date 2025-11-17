import os
import subprocess
import json
import torch
import numpy as np
from PIL import Image
import folder_paths

KEYFRAME_CACHE = {}

class LosslessCutLogic:
    def __init__(self):
        self.keyframes = []

    def get_keyframes(self, video_path):
        global KEYFRAME_CACHE
        if video_path in KEYFRAME_CACHE:
            self.keyframes = KEYFRAME_CACHE[video_path]
            return self.keyframes

        command = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'frame=pkt_pts_time,pict_type', '-of', 'json', video_path
        ]
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            data = json.loads(result.stdout)
            self.keyframes = sorted([float(frame['pkt_pts_time']) for frame in data.get('frames', []) if frame.get('pict_type') == 'I' and 'pkt_pts_time' in frame])
            KEYFRAME_CACHE[video_path] = self.keyframes
            return self.keyframes
        except Exception as e:
            print(f"Error getting keyframes: {e}")
            return []

    def process_event(self, video, video_path_, in_point, out_point, current_position, button):
        if video != video_path_ or not self.keyframes:
            self.get_keyframes(video)
            video_path_ = video
            if not self.keyframes:
                return -1.0, -1.0, -1.0, video_path_
            current_position, in_point, out_point = self.keyframes[0], self.keyframes[0], self.keyframes[-1]

        if button:
            if button == "prev_kf":
                prev_kfs = [k for k in self.keyframes if k < current_position]
                current_position = max(prev_kfs) if prev_kfs else current_position
            elif button == "next_kf":
                next_kfs = [k for k in self.keyframes if k > current_position]
                current_position = min(next_kfs) if next_kfs else current_position
            elif button == "set_in":
                if current_position < out_point:
                    in_point = current_position
            elif button == "set_out":
                if current_position > in_point:
                    out_point = current_position

        return in_point, out_point, current_position, video_path_

class LosslessCut:
    def __init__(self):
        self.logic = LosslessCutLogic()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "path/to/video.mp4"}),
                "action": (["do nothing", "cut video"],),
            },
            "hidden": {
                "in_point": ("FLOAT", {"default": -1.0}), "out_point": ("FLOAT", {"default": -1.0}),
                "current_position": ("FLOAT", {"default": -1.0}), "video_path_": ("STRING", {"default": ""}),
                "button": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("video_output_path", "preview_image")
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg/Editing"

    def get_frame_at_time(self, video_path, time_sec):
        temp_dir = folder_paths.get_temp_directory()
        output_file = os.path.join(temp_dir, f"preview.png")

        command = ['ffmpeg', '-y', '-ss', str(time_sec), '-i', video_path, '-vframes', '1', output_file]
        try:
            subprocess.run(command, check=True, capture_output=True)
            image = Image.open(output_file)
            os.remove(output_file)
            return torch.from_numpy(np.array(image).astype(np.float32) / 255.0)[None,]
        except Exception as e:
            print(f"Error generating preview: {e}")
            return torch.zeros((1, 256, 256, 3))

    def execute(self, video, action, in_point, out_point, current_position, video_path_, **kwargs):
        if not video or not os.path.isfile(video):
            return {"result": ("", torch.zeros((1, 256, 256, 3)))}

        in_point, out_point, current_position, video_path_ = self.logic.process_event(
            video, video_path_, in_point, out_point, current_position, kwargs.get("button", [None])[0]
        )

        output_file_path = ""
        if action == "cut video":
            output_dir = folder_paths.get_output_directory()
            filename = f"cut_{os.path.basename(video)}_{in_point:.2f}_{out_point:.2f}.mp4"
            output_file_path = os.path.join(output_dir, filename)

            command = ['ffmpeg', '-y', '-ss', str(in_point), '-to', str(out_point), '-i', video, '-c', 'copy', output_file_path]
            try:
                subprocess.run(command, check=True, capture_output=True)
            except Exception as e:
                print(f"ffmpeg error: {e}")
                output_file_path = ""

        preview_image = self.get_frame_at_time(video, current_position)

        return {
            "ui": {"in_point": [in_point], "out_point": [out_point], "current_position": [current_position], "video_path_": [video_path_]},
            "result": (output_file_path, preview_image)
        }
