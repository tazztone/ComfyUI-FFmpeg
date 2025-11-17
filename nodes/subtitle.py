import os
import subprocess
import shlex
import time

import os
import subprocess
import folder_paths

class HandleSubtitles:
    """
    A node to handle subtitles.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "subtitle_file": ("STRING", {"default": "subtitle.srt"}),
                "action": (["burn", "add", "extract"],),
                "filename": ("STRING", {"default": "video_with_subs.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "handle_subtitles"
    CATEGORY = "🔥FFmpeg/Advanced"

    def handle_subtitles(self, video, subtitle_file, action, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Input video not found: {video}")
        if action != 'extract' and not os.path.exists(subtitle_file):
            raise FileNotFoundError(f"Subtitle file not found: {subtitle_file}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        if action == 'burn':
            command = ['ffmpeg', '-y', '-i', video, '-vf', f"subtitles={subtitle_file}", output_path]
        elif action == 'add':
            command = ['ffmpeg', '-y', '-i', video, '-i', subtitle_file, '-c', 'copy', '-c:s', 'mov_text', output_path]
        elif action == 'extract':
            command = ['ffmpeg', '-y', '-i', video, '-map', '0:s:0', output_path]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr}")

        return (output_path,)
