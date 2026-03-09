import os
import subprocess
import folder_paths
from comfy_api.latest import io

class VideoFilterBase(io.ComfyNode):
    @classmethod
    def execute_ffmpeg(cls, video, filter_str, suffix) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        base, ext = os.path.splitext(os.path.basename(video))
        output_filename = f"{base}_{suffix}{ext}"
        output_path = os.path.join(folder_paths.get_output_directory(), output_filename)

        cmd = [
            "ffmpeg", "-y",
            "-i", video,
            "-vf", filter_str,
            "-c:a", "copy",  # Preserve audio
            output_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return io.NodeOutput(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg filter failed: {e.stderr}")

class VideoSpeedV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="VideoSpeedV3",
            display_name="🔥Video Speed (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Float.Input("speed", default=1.0, min=0.5, max=4.0, tooltip="Speed multiplier."),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, speed) -> io.NodeOutput:
        if speed == 1.0:
            return io.NodeOutput(video)
           
        # setpts for video, atempo for audio
        v_pts = 1.0 / speed
        v_filter = f"setpts={v_pts}*PTS"
       
        # Audio speed
        a_speed = speed
        a_filters = []
        while a_speed > 2.0:
            a_filters.append("atempo=2.0")
            a_speed /= 2.0
        while a_speed < 0.5:
            a_filters.append("atempo=0.5")
            a_speed *= 2.0
        a_filters.append(f"atempo={a_speed}")
        a_filter_str = ",".join(a_filters)
       
        base, ext = os.path.splitext(os.path.basename(video))
        output_filename = f"{base}_speed_{speed}{ext}"
        output_path = os.path.join(folder_paths.get_output_directory(), output_filename)

        cmd = [
            "ffmpeg", "-y",
            "-i", video,
            "-vf", v_filter,
            "-af", a_filter_str,
            output_path
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return io.NodeOutput(output_path)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg speed ramp failed: {e.stderr}")

class DenoiseV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="DenoiseV3",
            display_name="🔥Video Denoise (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Combo.Input("method", ["hqdn3d", "nlmeans"], default="hqdn3d"),
                io.Float.Input("strength", default=1.0, min=0.0, max=10.0),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, method, strength) -> io.NodeOutput:
        if method == "hqdn3d":
            v = 3 * strength
            filter_str = f"hqdn3d={v}:{v*0.67}:{v*1.5}:{v}"
        else:
            filter_str = f"nlmeans=s={strength}"
        return cls.execute_ffmpeg(video, filter_str, "denoised")

class ColorGradeV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ColorGradeV3",
            display_name="🔥Color Grade (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Float.Input("brightness", default=0.0, min=-1.0, max=1.0),
                io.Float.Input("contrast", default=1.0, min=0.0, max=2.0),
                io.Float.Input("saturation", default=1.0, min=0.0, max=3.0),
                io.Float.Input("gamma", default=1.0, min=0.1, max=10.0),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, brightness, contrast, saturation, gamma) -> io.NodeOutput:
        filter_str = f"eq=brightness={brightness}:contrast={contrast}:saturation={saturation}:gamma={gamma}"
        return cls.execute_ffmpeg(video, filter_str, "graded")

class ScaleV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="ScaleV3",
            display_name="🔥Scale Video (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Int.Input("width", default=1280, min=0),
                io.Int.Input("height", default=720, min=0),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, width, height) -> io.NodeOutput:
        w = width if width > 0 else -1
        h = height if height > 0 else -1
        filter_str = f"scale={w}:{h}"
        return cls.execute_ffmpeg(video, filter_str, f"scaled_{width}x{height}")

class CropV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="CropV3",
            display_name="🔥Crop Video (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Int.Input("w", default=720),
                io.Int.Input("h", default=720),
                io.Int.Input("x", default=0),
                io.Int.Input("y", default=0),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, w, h, x, y) -> io.NodeOutput:
        filter_str = f"crop={w}:{h}:{x}:{y}"
        return cls.execute_ffmpeg(video, filter_str, "cropped")

class DeinterlaceV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="DeinterlaceV3",
            display_name="🔥Deinterlace (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video) -> io.NodeOutput:
        return cls.execute_ffmpeg(video, "yadif", "deinterlaced")

class BurnTimecodeV3(VideoFilterBase):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="BurnTimecodeV3",
            display_name="🔥Burn Timecode (V3)",
            category="🔥FFmpeg/Filters",
            inputs=[
                io.String.Input("video", tooltip="Video file."),
                io.Int.Input("font_size", default=24),
                io.Combo.Input("position", ["top-left", "top-right", "bottom-left", "bottom-right", "bottom-center"], default="bottom-center"),
            ],
            outputs=[io.String.Output(tooltip="The output video path.")],
        )

    @classmethod
    def execute(cls, video, font_size, position) -> io.NodeOutput:
        pos_map = {
            "top-left": "x=10:y=10",
            "top-right": "x=w-tw-10:y=10",
            "bottom-left": "x=10:y=h-th-10",
            "bottom-right": "x=w-tw-10:y=h-th-10",
            "bottom-center": "x=(w-tw)/2:y=h-th-10",
        }
        p = pos_map[position]
        # Using a generic font path or assuming it's in the fonts dir of the plugin
        # ComfyUI-FFmpeg/fonts/
        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "Roboto-Regular.ttf")
        if not os.path.exists(font_path):
             # Fallback to just "Arial" and hope ffmpeg finds it
             filter_str = f"drawtext=text='%{{pts\\:hms}}':{p}:fontsize={font_size}:fontcolor=white:box=1:boxcolor=black@0.5"
        else:
             filter_str = f"drawtext=fontfile='{font_path}':text='%{{pts\\:hms}}':{p}:fontsize={font_size}:fontcolor=white:box=1:boxcolor=black@0.5"
       
        return cls.execute_ffmpeg(video, filter_str, "timecoded")
