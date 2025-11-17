import os
import subprocess
from ..func import set_file_name,video_type,audio_type,has_audio

import os
import subprocess
import folder_paths

class AddAudioFile:
    """
    A node to add an audio track to a video file from a file path.
    This node takes a video and an audio file and combines them into a single video file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "audio_file": ("STRING", {"default": "audio.wav"}),
                "filename": ("STRING", {"default": "video_with_audio_file.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "add_audio_file"
    CATEGORY = "🔥FFmpeg/Audio"

    def add_audio_file(self, video, audio_file, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            'ffmpeg', '-y', '-i', video, '-i', audio_file,
            '-c:v', 'copy', '-c:a', 'aac', '-shortest',
            output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)