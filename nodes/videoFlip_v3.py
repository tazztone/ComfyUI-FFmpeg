import os
import subprocess
import folder_paths

# Try to import the new V3 schema definition
try:
    from comfy.nodes.package import define_schema, async_comfy_entrypoint
except ImportError:
    # Fallback or handled gracefully if not available,
    # but for this prototype we assume the user has a modern ComfyUI.
    # We'll define dummy decorators to allow import without crashing,
    # but the node won't register as a V3 node without the real ones.
    def define_schema(schema_def):
        def decorator(cls):
            cls._V3_SCHEMA = schema_def
            return cls

        return decorator

    def async_comfy_entrypoint(func):
        return func


@define_schema(
    {
        "name": "🔥VideoFlip (V3)",
        "category": "🔥FFmpeg/Editing",
        "inputs": {
            "video": "STRING",  # Inputs are simplified in V3 for prototype
            "flip_type": (
                ["horizontal", "vertical", "both"],
                {"default": "horizontal"},
            ),
            "filename": ("STRING", {"default": "flipped_video_v3.mp4"}),
        },
        "outputs": {
            "output_path": "STRING",
        },
    }
)
class VideoFlipV3:
    """
    A V3 prototype node to flip a video horizontally, vertically, or both.
    """

    @async_comfy_entrypoint
    async def flip_video(self, video: str, flip_type: str, filename: str) -> str:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        output_path = os.path.join(folder_paths.get_output_directory(), filename)

        flip_map = {
            "horizontal": "hflip",
            "vertical": "vflip",
            "both": "hflip,vflip",
        }

        command = ["ffmpeg", "-y", "-i", video, "-vf", flip_map[flip_type], output_path]

        # In a real V3 async node, we would want to run this in an executor
        # to avoid blocking the event loop, but subprocess.run is synchronous.
        # For now, we keep it simple as a proof of concept.
        subprocess.run(command, check=True)

        return output_path
