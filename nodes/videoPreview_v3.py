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
            is_output_node=True,
            inputs=[
                io.String.Input("video", tooltip="The video file to preview."),
            ],
            outputs=[],  # Preview nodes usually don't have outputs
        )

    @classmethod
    def execute(cls, video) -> io.NodeOutput:
        if not os.path.exists(video):
            raise FileNotFoundError(f"Video file not found: {video}")

        # ComfyUI's internal preview logic expects files to be in the output or temp directory
        filename = os.path.basename(video)
        abs_video_path = os.path.abspath(video)
       
        output_dir = os.path.abspath(folder_paths.get_output_directory())
        temp_dir = os.path.abspath(folder_paths.get_temp_directory())
       
        if abs_video_path.startswith(temp_dir):
            folder_type = "temp"
        else:
            folder_type = "output"
            # If it's not in either, we might still need to copy it to output
            # but usually for this plugin, videos are generated in output/ already.
            if not abs_video_path.startswith(output_dir):
                 dest_path = os.path.join(output_dir, filename)
                 if abs_video_path != os.path.abspath(dest_path):
                     shutil.copy(video, dest_path)

        # Return UI data for the JS widget
        return io.NodeOutput(ui={"video": [filename, folder_type]})
