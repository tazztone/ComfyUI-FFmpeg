import os
import subprocess
import shlex
import time

import os
import subprocess
import tempfile
import torchaudio
import folder_paths

class ApplyAudioFilter:
    """
    A node to apply a raw FFmpeg audio filtergraph to an audio stream.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO", {
                    "tooltip": "The audio to apply the filter to."
                }),
                "filtergraph": ("STRING", {
                    "default": "loudnorm",
                    "multiline": True,
                    "tooltip": "The FFmpeg audio filtergraph to apply."
                }),
                "filename": ("STRING", {
                    "default": "filtered_audio.wav",
                    "tooltip": "The name of the output audio file."
                }),
            },
        }

    RETURN_TYPES = ("AUDIO", "STRING")
    FUNCTION = "apply_filter"
    CATEGORY = "🔥FFmpeg/Audio"

    def apply_filter(self, audio, filtergraph, filename):
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            torchaudio.save(temp_audio_file.name, audio['waveform'].cpu(), audio['sample_rate'])

            command = [
                'ffmpeg', '-y', '-i', temp_audio_file.name,
                '-af', filtergraph,
                output_path
            ]
            subprocess.run(command, check=True)

        waveform, sample_rate = torchaudio.load(output_path)
        filtered_audio = {'waveform': waveform.unsqueeze(0), 'sample_rate': sample_rate}

        return (filtered_audio, output_path)
