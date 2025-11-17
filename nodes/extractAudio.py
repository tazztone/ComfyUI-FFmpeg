import os
import subprocess
import tempfile
import torchaudio
import shutil
from ..func import video_type

import os
import subprocess
import tempfile
import torchaudio
import shutil
import folder_paths

class ExtractAudio:
    """
    A node to extract audio from a video file.
    This node takes a video file and extracts its audio track, saving it as a separate audio file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("STRING", {"default": "video.mp4"}),
                "filename": ("STRING", {"default": "extracted_audio.wav"}),
            },
        }

    RETURN_TYPES = ("AUDIO", "STRING")
    FUNCTION = "extract_audio"
    CATEGORY = "🔥FFmpeg/Audio"

    def extract_audio(self, video, filename):
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = ['ffmpeg', '-y', '-i', video, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_path]
        subprocess.run(command, check=True)

        waveform, sample_rate = torchaudio.load(output_path)
        audio_data = {'waveform': waveform.unsqueeze(0), 'sample_rate': sample_rate}

        return (audio_data, output_path)
