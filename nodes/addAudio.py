import os
import subprocess
import tempfile
import torch
import torchaudio
from ..func import set_file_name, video_type, audio_type, has_audio

class AddAudio:
    """
    Enhanced AddAudio node with VHS-compatible inputs/outputs.
    Accepts AUDIO data type and optional video_path for lossless remux.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {
                    "default": "C:/Users/Desktop/video.mp4",
                    "tooltip": "Path to original video file for lossless remux"
                }),
                "output_path": ("STRING", {
                    "default": "C:/Users/Desktop/output/",
                    "tooltip": "Directory to save remuxed video"
                }),
            },
            "optional": {
                "audio": ("AUDIO", {
                    "tooltip": "Processed audio from upstream nodes (VHS, TTS, RVC, etc.)"
                }),
                "audio_file_path": ("STRING", {
                    "default": "",
                    "tooltip": "Path to audio file (used only if audio input not connected)"
                }),
                "audio_codec": (["copy", "aac", "mp3", "opus"], {
                    "default": "aac",
                    "tooltip": "Audio codec (copy = lossless if compatible)"
                }),
                "audio_bitrate": ("STRING", {
                    "default": "192k",
                    "tooltip": "Audio bitrate (e.g., 128k, 192k, 320k)"
                }),
                "filename_prefix": ("STRING", {
                    "default": "",
                    "tooltip": "Prefix for output filename (optional)"
                }),
                "delay_play": ("INT", {
                    "default": 0,
                    "min": 0,
                    "tooltip": "Audio delay in seconds"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "VHS_FILENAMES")
    RETURN_NAMES = ("video_path", "filenames")
    FUNCTION = "add_audio_improved"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"

    def add_audio_improved(self, video_path, output_path, audio=None, audio_file_path="",
                          audio_codec="aac", audio_bitrate="192k", filename_prefix="", delay_play=0):
        """
        Enhanced AddAudio with full codec control and robust error handling.
        """
        # Initialize temp file variables at function scope
        temp_audio_file = None
        temp_audio_path = None

        try:
            video_path = os.path.abspath(video_path).strip()
            output_path = os.path.abspath(output_path).strip()

            # Validate video path
            if not video_path.lower().endswith(video_type()):
                raise ValueError(f"video_path: {video_path} is not a video file")
            if not os.path.isfile(video_path):
                raise ValueError(f"video_path: {video_path} does not exist")

            # Validate output directory
            if not os.path.isdir(output_path):
                os.makedirs(output_path, exist_ok=True)
                print(f"📁 Created output directory: {output_path}")

            # Handle audio input
            if audio is not None:
                print("📥 Received AUDIO data from upstream node")

                waveform = audio['waveform']
                sample_rate = audio['sample_rate']

                # Robust batch dimension handling
                while waveform.dim() > 2:
                    waveform = waveform.squeeze(0)

                if waveform.dim() == 1:
                    waveform = waveform.unsqueeze(0)

                # Create temporary audio file
                temp_audio_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix='.wav',
                    dir=output_path
                )
                temp_audio_path = temp_audio_file.name
                temp_audio_file.close()

                torchaudio.save(temp_audio_path, waveform.cpu(), sample_rate)
                audio_source = temp_audio_path
                print(f"💾 Saved AUDIO to temporary file: {audio_source}")

            elif audio_file_path and os.path.isfile(audio_file_path):
                audio_source = os.path.abspath(audio_file_path)
                print(f"📁 Using audio file path: {audio_source}")

                if not audio_file_path.lower().endswith(audio_type()):
                    raise ValueError(f"audio_file_path: {audio_file_path} is not an audio file")
            else:
                raise ValueError("No audio input provided. Connect AUDIO input or specify audio_file_path")

            # Generate output filename with optional prefix
            base_name = set_file_name(video_path)
            if filename_prefix:
                file_name = f"{filename_prefix}_{base_name}"
            else:
                file_name = base_name

            output_file_path = os.path.join(output_path, file_name)

            # Smart codec selection based on container
            _, ext = os.path.splitext(output_file_path)
            ext = ext.lower()

            if ext == '.mkv' and audio_codec == 'aac':
                # MKV can use copy for most codecs
                print("ℹ️  MKV container detected - attempting audio stream copy")
                final_audio_codec = 'copy'
            elif ext in ['.mp4', '.m4v'] and audio_codec == 'copy':
                # MP4 needs AAC or MP3
                print("ℹ️  MP4 container detected - using AAC for compatibility")
                final_audio_codec = 'aac'
            else:
                final_audio_codec = audio_codec

            # Build FFmpeg command
            command = [
                'ffmpeg',
                '-i', video_path,
                '-itsoffset', str(delay_play),
                '-i', audio_source,
                '-map', '0:v',
                '-map', '1:a',
                '-c:v', 'copy',  # LOSSLESS VIDEO!
            ]

            # Add audio codec parameters
            if final_audio_codec == 'copy':
                command.extend(['-c:a', 'copy'])
            else:
                command.extend(['-c:a', final_audio_codec, '-b:a', audio_bitrate])

            command.extend([
                '-shortest',
                '-y',
                output_file_path,
            ])

            print(f"🔧 FFmpeg command: {' '.join(command)}")

            # Execute FFmpeg
            result = subprocess.run(
                command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )

            # Enhanced error handling
            if result.returncode != 0:
                error_lines = result.stderr.split('\n')
                relevant_errors = [line for line in error_lines if 'error' in line.lower()]
                error_msg = '\n'.join(relevant_errors[-3:]) if relevant_errors else result.stderr

                raise ValueError(
                    f"FFmpeg remux failed. Common causes:\n"
                    f"• Audio/video format incompatibility\n"
                    f"• Invalid file paths\n"
                    f"• FFmpeg not installed\n\n"
                    f"FFmpeg output: {error_msg}"
                )
            else:
                print(f"✅ Lossless remux completed: {output_file_path}")

            # Clean up temporary audio file
            if temp_audio_path is not None:
                try:
                    os.unlink(temp_audio_path)
                    print(f"🗑️  Cleaned up temporary audio file")
                except Exception as e:
                    print(f"⚠️  Could not delete temp file: {e}")

            # Return VHS_FILENAMES format
            filenames = (True, [output_file_path])
            return (output_file_path, filenames)

        except Exception as e:
            # Clean up temp file on error
            if temp_audio_path is not None:
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass
            raise ValueError(f"AddAudio error: {e}")
