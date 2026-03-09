import os
import subprocess
import tempfile
import shutil
import folder_paths
import torchaudio
from PIL import Image
import numpy as np
from comfy_api.latest import io

# Global cache for detected hardware encoders
_DETECTED_ENCODERS = None

def detect_hw_encoders():
    global _DETECTED_ENCODERS
    if _DETECTED_ENCODERS is not None:
        return _DETECTED_ENCODERS
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True, text=True
        )
        encoders = []
        # Mapping of friendly names to ffmpeg encoder names
        hw_map = {
            "h264_nvenc (NVIDIA)": "h264_nvenc",
            "hevc_nvenc (NVIDIA)": "hevc_nvenc",
            "h264_qsv (Intel)": "h264_qsv",
            "hevc_qsv (Intel)": "hevc_qsv",
            "h264_videotoolbox (Apple)": "h264_videotoolbox",
            "hevc_videotoolbox (Apple)": "hevc_videotoolbox",
            "h264_vaapi (Linux/Intel/AMD)": "h264_vaapi",
            "hevc_vaapi (Linux/Intel/AMD)": "hevc_vaapi",
        }
        
        for friendly, internal in hw_map.items():
            if internal in result.stdout:
                encoders.append(friendly)
                
        if not encoders:
            encoders = ["libx264 (CPU)"]
        else:
            # Always have CPU fallback at the end
            encoders.append("libx264 (CPU)")
            
        _DETECTED_ENCODERS = encoders
        return _DETECTED_ENCODERS
    except Exception:
        return ["libx264 (CPU)"]

class EncodeWithHWAccelV3(io.ComfyNode):
    """
    A V3 node to encode video using auto-detected hardware acceleration.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        encoders = detect_hw_encoders()
        return io.Schema(
            node_id="EncodeWithHWAccelV3",
            display_name="🔥Encode with HW Accel (V3)",
            category="🔥FFmpeg/Output",
            inputs=[
                io.Image.Input("images", tooltip="Input images (tensor batch)."),
                io.Int.Input("fps", default=24, min=1),
                io.Combo.Input("encoder", encoders, default=encoders[0]),
                io.Int.Input("quality", default=23, min=0, max=51, tooltip="CQ/CRF value. Lower is better."),
                io.String.Input("filename", default="hw_encoded.mp4"),
                io.Audio.Input("audio", optional=True),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, images, fps, encoder, quality, filename, audio=None) -> io.NodeOutput:
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        # Extract internal encoder name
        internal_encoder = encoder.split(" ")[0]
        quality_flag = "-cq" if "nvenc" in internal_encoder or "qsv" in internal_encoder or "videotoolbox" in internal_encoder else "-crf"
        
        try:
            for i, img_tensor in enumerate(images):
                img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
                Image.fromarray(img_np).save(os.path.join(temp_dir, f"{i:05d}.png"))

            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(temp_dir, "%05d.png"),
            ]

            audio_file = None
            if audio:
                audio_file = tempfile.mktemp(suffix=".wav")
                waveform = audio["waveform"]
                if waveform.dim() == 3:
                     waveform = waveform.squeeze(0)
                torchaudio.save(audio_file, waveform.cpu(), audio["sample_rate"])
                cmd.extend(["-i", audio_file])

            cmd.extend([
                "-c:v", internal_encoder,
                quality_flag, str(quality),
                "-pix_fmt", "yuv420p",
            ])

            if audio:
                cmd.extend(["-c:a", "aac", "-shortest"])

            cmd.append(output_path)
            subprocess.run(cmd, check=True, capture_output=True, text=True)

            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)

            return io.NodeOutput(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg HW encoding failed: {e.stderr}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
