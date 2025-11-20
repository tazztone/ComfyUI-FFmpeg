import os
import subprocess
try:
    from ..func import validate_file_exists, save_tensor_to_temp_file, get_output_path
except ImportError:
    from func import validate_file_exists, save_tensor_to_temp_file, get_output_path

class PictureInPicture:
    """
    A node to create a picture-in-picture (PiP) video.
    This node overlays one video on top of another, with options for positioning, scaling, and audio selection.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "background_video": ("STRING", {
                    "default": "background.mp4",
                    "tooltip": "The main video to be used as the background."
                }),
                "position": (["top_left", "top_right", "bottom_left", "bottom_right", "center"], {
                    "tooltip": "The position of the foreground video on the background video."
                }),
                "scale": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.1,
                    "max": 1.0,
                    "tooltip": "The scale of the foreground video."
                }),
                "audio_source": (["background", "foreground", "none"], {
                    "default": "background",
                    "tooltip": "The audio source for the output video."
                }),
                "filename": ("STRING", {
                    "default": "pip_video.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
            "optional": {
                "foreground_video": ("STRING", {
                    "default": "",
                    "tooltip": "Foreground video path (if not using image)."
                }),
                "foreground_image": ("IMAGE", {
                    "tooltip": "Foreground image from ComfyUI (alternative to video)."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_video",)
    FUNCTION = "create_pip_video"
    CATEGORY = "🔥FFmpeg/Editing"

    def create_pip_video(self, background_video, position, scale, audio_source, filename,
                         foreground_video="", foreground_image=None):

        validate_file_exists(background_video, "Background video")

        # Determine foreground source
        temp_files = []
        foreground_is_image = False
        if foreground_image is not None:
            foreground_path = save_tensor_to_temp_file(foreground_image[0], "fg")
            temp_files.append(foreground_path)
            foreground_is_image = True
        elif foreground_video:
            validate_file_exists(foreground_video, "Foreground video")
            foreground_path = foreground_video
        else:
            raise ValueError("Either foreground_video or foreground_image must be provided")

        output_path = get_output_path(filename)

        position_map = {
            "top_left": "10:10",
            "top_right": "W-w-10:10",
            "bottom_left": "10:H-h-10",
            "bottom_right": "W-w-10:H-h-10",
            "center": "(W-w)/2:(H-h)/2",
        }

        filter_complex = f"[1:v]scale=iw*{scale}:-1[fg];[0:v][fg]overlay={position_map[position]}"

        command = ['ffmpeg', '-y', '-i', background_video, '-i', foreground_path, '-filter_complex', filter_complex]

        # Handle audio mapping logic
        if foreground_is_image and audio_source == "foreground":
            print("Warning: Foreground is an image (no audio), ignoring audio_source='foreground'.")
            audio_source = "none"

        if audio_source != "none":
            audio_map = {"background": "0:a", "foreground": "1:a"}
            # Only map if the source actually has audio?
            # ffmpeg might fail if we map a stream that doesn't exist.
            # Assuming background has audio if selected.
            command.extend(['-map', '0:v', '-map', audio_map[audio_source], '-shortest'])

        command.append(output_path)

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")
        finally:
            # Cleanup temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

        return (output_path,)
