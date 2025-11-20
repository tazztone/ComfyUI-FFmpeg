import os
import subprocess
try:
    from ..func import validate_file_exists, get_output_path
except ImportError:
    from func import validate_file_exists, get_output_path

class MergeVideos:
    """
    A node to merge two video files into a single video.
    This node concatenates two video files, handling audio and resolution differences.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video1": ("STRING", {
                    "default": "video1.mp4",
                    "tooltip": "The first video file to merge."
                }),
                "video2": ("STRING", {
                    "default": "video2.mp4",
                    "tooltip": "The second video file to merge."
                }),
                "resolution": (["720p", "1080p", "4K"], {
                    "default": "1080p",
                    "tooltip": "The resolution of the output video."
                }),
                "filename": ("STRING", {
                    "default": "merged_video.mp4",
                    "tooltip": "The name of the output video file."
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("merged_video",)
    FUNCTION = "merge_videos"
    CATEGORY = "🔥FFmpeg/Editing"

    def merge_videos(self, video1, video2, resolution, filename):
        validate_file_exists(video1, "Video 1")
        validate_file_exists(video2, "Video 2")

        output_path = get_output_path(filename)

        resolution_map = {
            "720p": "1280:720",
            "1080p": "1920:1080",
            "4K": "3840:2160",
        }

        command = [
            'ffmpeg', '-y', '-i', video1, '-i', video2,
            '-filter_complex',
            f"[0:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v0];"
            f"[1:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];"
            f"[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]",
            '-map', '[v]', '-map', '[a]',
            output_path
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg execution failed: {e}")

        return (output_path,)
