import os
import subprocess
import torchaudio
import folder_paths
from comfy_api.latest import io


class ExtractAudioV3(io.ComfyNode):
    """
    A V3 node to extract audio from a video file.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ExtractAudioV3",
            display_name="🔥Extract Audio (V3)",
            category="🔥FFmpeg/Audio",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.String.Input(
                    "filename",
                    default="extracted_audio.wav",
                    tooltip="Output audio filename.",
                ),
            ],
            outputs=[
                io.Audio.Output(tooltip="The extracted audio data."),
                io.String.Output(tooltip="The path to the audio file."),
            ],
        )

    @classmethod
    def execute(cls, video, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "44100",
            "-ac",
            "2",
            output_path,
        ]
        subprocess.run(command, check=True)

        waveform, sample_rate = torchaudio.load(output_path)
        audio_data = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}

        return io.NodeOutput(audio_data, output_path)
