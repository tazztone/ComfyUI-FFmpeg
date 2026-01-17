import json
import uuid


def create_node(id, type, pos, inputs=[], widgets_values=[]):
    return {
        "id": id,
        "type": type,
        "pos": pos,
        "size": [300, 100],
        "flags": {},
        "order": id,
        "mode": 0,
        "inputs": inputs,
        "outputs": [{"name": "STRING", "type": "STRING", "links": []}],
        "properties": {"Node name for S&R": type},
        "widgets_values": widgets_values,
    }


def create_link(id, origin_id, origin_slot, target_id, target_slot, type="STRING"):
    return [id, origin_id, origin_slot, target_id, target_slot, type]


workflow = {
    "version": 0.4,
    "nodes": [],
    "links": [],
    "groups": [],
    "config": {},
    "extra": {},
}

# --- Nodes ---

# 1. Load Images (Source)
node_load = create_node(
    1, "LoadImagesFromDirectoryV3", [100, 100], widgets_values=["images"]
)
node_load["outputs"][0] = {
    "name": "IMAGE",
    "type": "IMAGE",
    "links": [],
}  # Override output type

# 2. Frames to Video
node_f2v = create_node(
    2,
    "Frames2VideoV3",
    [500, 100],
    inputs=[{"name": "images", "type": "IMAGE", "link": 1}],
    widgets_values=[24, "h264_cpu", 23, "medium", "video_from_frames.mp4"],
)

# 3. Add Text Watermark
node_watermark = create_node(
    3,
    "AddTextWatermarkV3",
    [900, 100],
    inputs=[{"name": "video", "type": "STRING", "link": 2}],
    widgets_values=["ComfyUI", 48, "white", 10, 10, "default"],
)

# 4. Flip Video
node_flip = create_node(
    4,
    "VideoFlipV3",
    [1300, 100],
    inputs=[{"name": "video", "type": "STRING", "link": 3}],
    widgets_values=["horizontal", "flipped_video_v3.mp4"],
)

# 5. Reverse Video
node_reverse = create_node(
    5,
    "ReverseVideoV3",
    [1700, 100],
    inputs=[{"name": "video", "type": "STRING", "link": 4}],
    widgets_values=[True, "reversed_video.mp4"],
)

# 6. Extract Audio
node_extract = create_node(
    6,
    "ExtractAudioV3",
    [900, 400],
    inputs=[{"name": "video", "type": "STRING", "link": 2}],
    widgets_values=["extracted_audio.wav"],
)
node_extract["outputs"] = [
    {"name": "AUDIO", "type": "AUDIO", "links": []},
    {"name": "STRING", "type": "STRING", "links": []},
]

# 7. Trim Video (Independent Branch)
node_trim = create_node(
    7,
    "TrimVideoV3",
    [100, 400],
    widgets_values=["sample.mp4", "00:00:00", "00:00:05", "trimmed_video.mp4"],
)
# Manually add input slot for video link (even if using widget value initially, V3 has optional inputs)
node_trim["inputs"] = [{"name": "video", "type": "STRING", "link": None}]

# 8. Split Video
node_split = create_node(
    8,
    "SplitVideoV3",
    [500, 400],
    inputs=[{"name": "video", "type": "STRING", "link": None}],
    widgets_values=[5, "split_"],
)

# 9. Merge Videos (Two)
node_merge = create_node(
    9,
    "MergeVideosV3",
    [900, 700],
    inputs=[
        {"name": "video1", "type": "STRING", "link": None},
        {"name": "video2", "type": "STRING", "link": None},
    ],
    widgets_values=["1080p", "merged_video.mp4"],
)

# 10. Picture In Picture
node_pip = create_node(
    10,
    "PictureInPictureV3",
    [1300, 700],
    inputs=[
        {
            "name": "background_video",
            "type": "STRING",
            "link": 4,
        },  # Using flipped video as BG
        {"name": "foreground_video", "type": "STRING", "link": None},
        {"name": "foreground_image", "type": "IMAGE", "link": None},
    ],
    widgets_values=["top_right", 0.5, "background", "pip.mp4", "", ""],
)

# 11. Generic FFmpeg
node_generic = create_node(
    11,
    "GenericFFmpegV3",
    [100, 700],
    inputs=[{"name": "video", "type": "STRING", "link": None}],
    widgets_values=["-vf hflip", "generic_out.mp4"],
)

# 12. Save Images (from Load)
node_save = create_node(
    12,
    "SaveImagesV3",
    [500, 700],
    inputs=[{"name": "images", "type": "IMAGE", "link": 1}],
    widgets_values=["saved_images", "img"],
)

# Add nodes to workflow
nodes_list = [
    node_load,
    node_f2v,
    node_watermark,
    node_flip,
    node_reverse,
    node_extract,
    node_trim,
    node_split,
    node_merge,
    node_pip,
    node_generic,
    node_save,
]
workflow["nodes"] = nodes_list

# -- Generate Links --
# Link ID 1: Load(Image) -> F2V(Image)
# Link ID 2: F2V(String) -> Watermark(Video)
# Link ID 3: Watermark(String) -> Flip(Video)
# Link ID 4: Flip(String) -> Reverse(Video)
# Link ID 5: Flip(String) -> PiP(BG) [Already in inputs def]

links = []
links.append(create_link(1, 1, 0, 2, 0, "IMAGE"))  # Load -> F2V
links.append(create_link(2, 2, 0, 3, 0, "STRING"))  # F2V -> Watermark
links.append(create_link(3, 3, 0, 4, 0, "STRING"))  # Watermark -> Flip
links.append(create_link(4, 4, 0, 5, 0, "STRING"))  # Flip -> Reverse
links.append(create_link(5, 4, 0, 10, 0, "STRING"))  # Flip -> PiP
links.append(create_link(6, 1, 0, 12, 0, "IMAGE"))  # Load -> Save

workflow["links"] = links

print(json.dumps(workflow, indent=2))
