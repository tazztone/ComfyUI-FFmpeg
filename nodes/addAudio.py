import os
import subprocess
import tempfile
import folder_paths
from ..func import set_file_name, video_type, audio_type, has_audio

class AddAudio:
    """A node to add audio to a video file.

    This node takes a video file and an audio source (either from an upstream
    node or a file path) and combines them into a new video file. It performs
    a lossless remux, meaning the video stream is copied without re-encoding,
    preserving its original quality.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """Specifies the input types for the node.

        Returns:
            dict: A dictionary containing the input types.
        """
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
                # Accept AUDIO from VHS nodes or other audio processing nodes
                "audio": ("AUDIO", {
                    "tooltip": "Processed audio from upstream nodes (VHS, TTS, RVC, etc.)"
                }),
                # Alternative: accept audio file path if no audio input connected
                "audio_file_path": ("STRING", {
                    "default": "",
                    "tooltip": "Path to audio file (used only if audio input not connected)"
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

    def add_audio_improved(self, video_path, output_path, audio=None, audio_file_path="", delay_play=0):
        """Adds audio to a video file.

        This method takes a video file and an audio source and combines them
        using FFmpeg. It prioritizes audio data from an upstream node but can
        fall back to an audio file path.

        Args:
            video_path (str): The path to the input video file.
            output_path (str): The directory to save the output video file.
            audio (dict, optional): Audio data from an upstream node.
                Defaults to None.
            audio_file_path (str, optional): The path to an audio file.
                Defaults to "".
            delay_play (int, optional): The audio delay in seconds.
                Defaults to 0.

        Returns:
            tuple: A tuple containing the path to the output video file and
                   a tuple with a boolean and a list of filenames.
        """
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
                raise ValueError(f"output_path: {output_path} is not a directory")

            # Handle audio input - priority to AUDIO data type
            temp_audio_file = None

            if audio is not None:
                # Audio data type from VHS or other nodes
                # VHS AUDIO format: {'waveform': tensor, 'sample_rate': int}
                print("📥 Received AUDIO data from upstream node")

                # Save AUDIO to temporary file for FFmpeg processing
                import torch
                import torchaudio

                waveform = audio['waveform'] # Shape: [batch, channels, samples]
                sample_rate = audio['sample_rate']

                # Create temporary audio file
                temp_audio_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix='.wav',
                    dir=output_path
                )
                temp_audio_path = temp_audio_file.name
                temp_audio_file.close()

                # Save waveform to temporary WAV file
                # Ensure correct shape: [channels, samples]
                if waveform.dim() == 3:
                    waveform = waveform.squeeze(0) # Remove batch dimension

                torchaudio.save(temp_audio_path, waveform.cpu(), sample_rate)
                audio_source = temp_audio_path
                print(f"💾 Saved AUDIO to temporary file: {audio_source}")

            elif audio_file_path and os.path.isfile(audio_file_path):
                # Fallback to file path
                audio_source = os.path.abspath(audio_file_path)
                print(f"📁 Using audio file path: {audio_source}")

                if not audio_file_path.lower().endswith(audio_type()):
                    raise ValueError(f"audio_file_path: {audio_file_path} is not an audio file")
            else:
                raise ValueError("No audio input provided. Connect AUDIO input or specify audio_file_path")

            # Generate output filename
            file_name = set_file_name(video_path)
            output_file_path = os.path.join(output_path, file_name)

            # Build FFmpeg command for lossless remux
            # Uses -c:v copy (video stream copied without re-encoding)
            command = [
                'ffmpeg',
                '-i', video_path, # Input video
                '-itsoffset', str(delay_play), # Audio delay
                '-i', audio_source, # Input audio
                '-map', '0:v', # Map video from first input
                '-map', '1:a', # Map audio from second input
                '-c:v', 'copy', # Copy video stream (LOSSLESS!)
                '-c:a', 'aac', # Encode audio to AAC (MP4 compatible)
                '-b:a', '192k', # Audio bitrate
                '-shortest', # Match shortest stream duration
                '-y', # Overwrite output file
                output_file_path,
            ]

            print(f"🔧 Running FFmpeg command:")
            print(f" {' '.join(command)}")

            # Execute FFmpeg
            result = subprocess.run(
                command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )

            # Check for errors
            if result.returncode != 0:
                print(f"❌ FFmpeg error: {result.stderr}")
                raise ValueError(f"FFmpeg failed: {result.stderr}")
            else:
                print(f"✅ Lossless remux completed: {output_file_path}")

            # Clean up temporary audio file
            if temp_audio_file is not None:
                try:
                    os.unlink(temp_audio_path)
                    print(f"🗑️ Cleaned up temporary audio file")
                except:
                    pass

            # Return VHS_FILENAMES format for compatibility
            filenames = (True, [output_file_path])

            return (output_file_path, filenames)

        except Exception as e:
            # Clean up temp file on error
            if temp_audio_file is not None:
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass
            raise ValueError(f"AddAudioImproved error: {e}")
