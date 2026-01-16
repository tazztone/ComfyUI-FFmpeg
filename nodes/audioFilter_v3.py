import os
import subprocess
import tempfile
import torchaudio
import folder_paths
from comfy_api.latest import io


class ApplyAudioFilterV3(io.ComfyNode):
    """
    A V3 node to apply a raw FFmpeg audio filtergraph.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ApplyAudioFilterV3",
            display_name="🔥Apply Audio Filter (V3)",
            category="🔥FFmpeg/Audio",
            inputs=[
                io.Audio.Input("audio", tooltip="Audio input."),
                io.String.Input(
                    "filtergraph",
                    default="loudnorm",
                    multiline=True,
                    tooltip="FFmpeg audio filtergraph.",
                ),
                io.String.Input(
                    "filename", default="filtered_audio.wav", tooltip="Output filename."
                ),
            ],
            outputs=[
                io.Audio.Output(tooltip="The filtered audio data."),
                io.String.Output(tooltip="The path to the audio file."),
            ],
        )

    @classmethod
    def execute(cls, audio, filtergraph, filename) -> io.NodeOutput:
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False
        ) as temp_audio_file:
            temp_name = temp_audio_file.name

        torchaudio.save(temp_name, audio["waveform"].cpu(), audio["sample_rate"])

        command = ["ffmpeg", "-y", "-i", temp_name, "-af", filtergraph, output_path]

        try:
            subprocess.run(command, check=True)
            waveform, sample_rate = torchaudio.load(output_path)
            filtered_audio = {
                "waveform": waveform.unsqueeze(0),
                "sample_rate": sample_rate,
            }
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)

        return io.NodeOutput(filtered_audio, output_path)
