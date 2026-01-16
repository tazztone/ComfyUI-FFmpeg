import sys
import os

# Add parent dir to path to allow importing nodes_map
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from nodes_map import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

    print("V3 Nodes found in NODE_DISPLAY_NAME_MAPPINGS:")
    v3_nodes = sorted([v for k, v in NODE_DISPLAY_NAME_MAPPINGS.items() if "(V3)" in v])
    for name in v3_nodes:
        print(f" - {name}")

    print(f"\nTotal V3 Nodes: {len(v3_nodes)}")

    print("\nMissing V3 Nodes (Expected 26):")
    expected = [
        "LoadImagesFromDirectoryV3",
        "SaveImagesV3",
        "GenericFFmpegV3",
        "AnalyzeStreamsV3",
        "VideoFlipV3",
        "TrimVideoV3",
        "SplitVideoV3",
        "ReverseVideoV3",
        "RemuxVideoV3",
        "KeyframeTrimV3",
        "MergeVideosV3",
        "MergeVideoBatchV3",
        "StitchVideosV3",
        "VideoTransitionV3",
        "PictureInPictureV3",
        "AddTextWatermarkV3",
        "AddImgWatermarkV3",
        "AddAudioV3",
        "ExtractAudioV3",
        "ApplyAudioFilterV3",
        "HandleSubtitlesV3",
        "ApplyFiltergraphV3",
        "ApplyStreamMapV3",
        "Video2FramesV3",
        "Frames2VideoV3",
        "LosslessCutV3",
    ]

    found_keys = [k for k in NODE_CLASS_MAPPINGS.keys() if k.endswith("V3")]
    missing = set(expected) - set(found_keys)
    if missing:
        for m in missing:
            print(f" - {m}")
    else:
        print(" - None")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
