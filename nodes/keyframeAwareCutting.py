import os
import subprocess
import json
from datetime import datetime, timedelta

class KeyframeAwareCutting:
    """
    A node to cut a video at the nearest keyframes to the specified start and end times.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Specifies the input types for the node.
        """
        return {
            "required": {
                "video_path": ("STRING", {
                    "default": "C:/Users/Desktop/video.mp4",
                    "tooltip": "Path to the video file to be cut."
                }),
                "start_time": ("STRING", {
                    "default": "00:00:00",
                    "tooltip": "Start time for the cut (HH:MM:SS). The cut will snap to the nearest keyframe."
                }),
                "end_time": ("STRING", {
                    "default": "00:00:10",
                    "tooltip": "End time for the cut (HH:MM:SS). The cut will snap to the nearest keyframe."
                }),
                "output_path": ("STRING", {
                    "default": "C:/Users/Desktop/output",
                    "tooltip": "Directory to save the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_output_path",)
    FUNCTION = "cut_video"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def get_keyframes(self, video_path):
        """
        Gets the timestamps of all keyframes in the video.
        """
        command = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_frames',
            '-show_entries', 'frame=pkt_pts_time,pict_type', '-of', 'json', video_path
        ]
        result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, text=True, encoding='utf-8')
        data = json.loads(result.stdout)
        keyframes = [float(frame['pkt_pts_time']) for frame in data.get('frames', []) if frame.get('pict_type') == 'I' and 'pkt_pts_time' in frame]
        return keyframes

    def find_nearest_keyframe(self, time_in_seconds, keyframes):
        """
        Finds the nearest keyframe to the given time.
        """
        if not keyframes:
            return time_in_seconds
        return min(keyframes, key=lambda x: abs(x - time_in_seconds))

    def cut_video(self, video_path, start_time, end_time, output_path):
        """
        Cuts the video at the nearest keyframes.
        """
        try:
            video_path = os.path.abspath(video_path).strip()
            if not os.path.isfile(video_path):
                raise ValueError(f"Video file not found: {video_path}")

            time_format = "%H:%M:%S"
            start_dt = datetime.strptime(start_time, time_format)
            end_dt = datetime.strptime(end_time, time_format)
            start_seconds = (start_dt - datetime(1900, 1, 1)).total_seconds()
            end_seconds = (end_dt - datetime(1900, 1, 1)).total_seconds()

            keyframes = self.get_keyframes(video_path)
            start_keyframe = self.find_nearest_keyframe(start_seconds, keyframes)
            end_keyframe = self.find_nearest_keyframe(end_seconds, keyframes)

            if start_keyframe >= end_keyframe:
                raise ValueError("Start time must be less than end time after snapping to keyframes.")

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            output_file_path = os.path.join(output_path, file_name)

            command = [
                'ffmpeg', '-y', '-i', video_path,
                '-ss', str(start_keyframe),
                '-to', str(end_keyframe),
                '-c', 'copy', output_file_path
            ]

            subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True, text=True, encoding='utf-8')

            return (output_file_path,)

        except subprocess.CalledProcessError as e:
            raise ValueError(f"ffmpeg error:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        except Exception as e:
            raise ValueError(e)
