import os
import subprocess
import tempfile
import torch
import torchaudio
from ..func import set_file_name, video_type, audio_type, has_audio

import os
import subprocess
import tempfile
import torch
import torchaudio
import folder_paths

class AddAudio:
    """
    A node to add an audio track to a video file.
    This node takes a video and an audio input and combines them into a single video file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {
                    "default": "video.mp4",
                    "tooltip": "The video file to add the audio to."
                }),
                "audio": ("AUDIO", {
                    "tooltip": "The audio to add to the video."
                }),
                "filename": ("STRING", {
                    "default": "video_with_audio.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "add_audio"
    CATEGORY = "🔥FFmpeg/Audio"

    def add_audio(self, video, audio, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            torchaudio.save(temp_audio_file.name, audio['waveform'].cpu(), audio['sample_rate'])

            command = [
                'ffmpeg', '-y', '-i', video, '-i', temp_audio_file.name,
                '-c:v', 'copy', '-c:a', 'aac', '-shortest',
                output_path
            ]
            subprocess.run(command, check=True)

        return (output_path,)
