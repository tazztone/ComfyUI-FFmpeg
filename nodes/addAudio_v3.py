import os
import subprocess
import tempfile
import torchaudio
import folder_paths
from comfy_api.latest import io


class AddAudioV3(io.ComfyNode):
    """
    A V3 node to add an audio track (native ComfyUI AUDIO dict) to a video file.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="AddAudioV3",
            display_name="🔥Add Audio (V3)",
            category="🔥FFmpeg/Audio",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Audio.Input("audio", tooltip="Audio input.", optional=True),
                io.String.Input(
                    "filename",
                    default="video_with_audio.mp4",
                    tooltip="Output filename.",
                ),
            ],
            outputs=[
                io.String.Output(tooltip="The path to the output video file."),
            ],
        )

    @classmethod
    def execute(cls, video, audio, filename) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        # audio input is likely a dict {'waveform': ..., 'sample_rate': ...}
        # V3 likely passes this dict directly or wrapped?
        # Assuming dict structure from V1 based on usage.

        if audio is None:
             # Just copy the video to the output path if no audio is provided
             command = [
                "ffmpeg",
                "-y",
                "-i",
                video,
                "-c",
                "copy",
                output_path,
             ]
             subprocess.run(command, check=True)
             return io.NodeOutput(output_path)

        with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False
        ) as temp_audio_file:
            temp_name = temp_audio_file.name

        # Save audio to temp file
        waveform = audio["waveform"]
        if waveform.dim() == 3:
            waveform = waveform.squeeze(0)
            
        torchaudio.save(temp_name, waveform.cpu(), audio["sample_rate"])

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video,
            "-i",
            temp_name,
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            output_path,
        ]

        try:
            subprocess.run(command, check=True)
        finally:
            try:
                os.remove(temp_name)
            except OSError:
                pass

        return io.NodeOutput(output_path)
