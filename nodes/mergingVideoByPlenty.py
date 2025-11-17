import os
import subprocess
import folder_paths

class MergeVideoBatch:
    """
    A node to merge multiple video files from a directory into a single video.
    This node concatenates all video files in a specified directory into a single output video file.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video_directory": ("STRING", {"default": "videos"}),
                "resolution": (["720p", "1080p", "4K"], {"default": "1080p"}),
                "filename": ("STRING", {"default": "merged_video_batch.mp4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge_video_batch"
    CATEGORY = "🔥FFmpeg/Editing"

    def merge_video_batch(self, video_directory, resolution, filename):
        if not os.path.isdir(video_directory):
            raise FileNotFoundError(f"Video directory not found: {video_directory}")

        videos = sorted([os.path.join(video_directory, f) for f in os.listdir(video_directory) if f.endswith(".mp4")])
        if not videos:
            raise ValueError("No MP4 videos found in the directory.")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        resolution_map = {
            "720p": "1280:720",
            "1080p": "1920:1080",
            "4K": "3840:2160",
        }

        inputs = [item for video in videos for item in ['-i', video]]
        filter_complex = "".join([
            f"[{i}:v]scale={resolution_map[resolution]}:force_original_aspect_ratio=decrease,pad={resolution_map[resolution]}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}];"
            for i in range(len(videos))
        ])
        filter_complex += "".join([f"[v{i}][{i}:a?]" for i in range(len(videos))]) + f"concat=n={len(videos)}:v=1:a=1[v][a]"

        command = [
            'ffmpeg', '-y', *inputs,
            '-filter_complex', filter_complex,
            '-map', '[v]', '-map', '[a]',
            output_path
        ]

        subprocess.run(command, check=True)
        return (output_path,)