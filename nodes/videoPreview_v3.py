import os
import shutil
import folder_paths
from comfy_api.latest import io

class VideoPreviewV3(io.ComfyNode):
    """
    A V3 node to preview a video file in the ComfyUI frontend.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="VideoPreviewV3",
            display_name="🔥Video Preview (V3)",
            category="🔥FFmpeg/Output",
            inputs=[
                io.String.Input("video", tooltip="The video file to preview."),
            ],
            outputs=[],  # Preview nodes usually don't have outputs
        )

    @classmethod
    def execute(cls, video) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        # ComfyUI's internal preview logic expects files to be in the output directory
        # specifically in a way the frontend can fetch them via /view?filename=...
        filename = os.path.basename(video)
        output_dir = folder_paths.get_output_directory()
        dest_path = os.path.join(output_dir, filename)
        
        if os.path.abspath(video) != os.path.abspath(dest_path):
            shutil.copy(video, dest_path)
            
        # Return UI data for the JS widget
        # The frontend will look for "video" in the ui results
        return io.NodeOutput(ui={"video": [filename, "output"]})
