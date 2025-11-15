import os
import subprocess
import tempfile
import torchaudio
import shutil
from ..func import video_type

class ExtractAudio:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_path": ("STRING", {"default":"C:/Users/Desktop/video.mp4",}),
            },
            "optional": {
                "output_format": (["wav", "mp3", "flac"], {"default": "wav"}),
                "save_to_disk": ("BOOLEAN", {"default": False}),
                "output_path": ("STRING", {"default":""}),
            }
        }

    RETURN_TYPES = ("AUDIO", "STRING")
    RETURN_NAMES = ("audio", "audio_path")
    FUNCTION = "extract_audio"
    OUTPUT_NODE = True
    CATEGORY = "🔥FFmpeg"
  
    def extract_audio(self, video_path, output_format="wav", save_to_disk=False, output_path=""):
        try:
            video_path = os.path.abspath(video_path).strip()

            if not video_path.lower().endswith(video_type()):
                raise ValueError("video_path："+video_path+"不是视频文件（video_path:"+video_path+" is not a video file）")
            if not os.path.isfile(video_path):
                raise ValueError("video_path："+video_path+"不存在（video_path:"+video_path+" does not exist）")
            
            temp_audio = tempfile.mktemp(suffix=f'.{output_format}')

            if output_format == "mp3":
                command = [
                    'ffmpeg', '-i', video_path,
                    '-vn', '-c:a', 'libmp3lame', '-q:a','2',
                    temp_audio,
                ]
            elif output_format == "wav":
                command = [
                    'ffmpeg', '-i', video_path,
                    '-vn','-c:a','pcm_s16le',
                    temp_audio,
                ]
            elif output_format == "flac":
                command = [
                    'ffmpeg', '-i', video_path,
                    '-vn','-c:a','flac',
                    temp_audio,
                ]
            else:
                raise ValueError(f"Unsupported audio format: {output_format}")
            
            result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if result.returncode != 0:
                 print(f"Error: {result.stderr.decode('utf-8')}")
                 raise ValueError(f"Error: {result.stderr.decode('utf-8')}")
            else:
                print(result.stdout)

            waveform, sample_rate = torchaudio.load(temp_audio)

            audio_data = {
                'waveform': waveform.unsqueeze(0),
                'sample_rate': sample_rate
            }

            if save_to_disk:
                if not output_path or not os.path.isdir(output_path):
                    from folder_paths import get_output_directory
                    output_path = get_output_directory()

                file_name = os.path.splitext(os.path.basename(video_path))[0]
                final_path = os.path.join(output_path, f"{file_name}.{output_format}")
                shutil.move(temp_audio, final_path)
                return (audio_data, final_path)
            else:
                return (audio_data, temp_audio)
        except Exception as e:
            raise ValueError(e)
