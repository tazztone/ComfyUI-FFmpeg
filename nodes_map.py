from .nodes.addTextWatermark import AddTextWatermark
from .nodes.frames2video import Frames2Video
from .nodes.video2frames import Video2Frames
from .nodes.addImgWatermark import AddImgWatermark
from .nodes.videoFlip import VideoFlip
from .nodes.extractAudio import ExtractAudio
from .nodes.loadImageFromDir import LoadImagesFromDirectory

from .nodes.mergingVideoByTwo import MergeVideos
from .nodes.mergingVideoByPlenty import MergeVideoBatch
from .nodes.stitchingVideo import StitchVideos
from .nodes.multiCuttingVideo import SplitVideo
from .nodes.singleCuttingVideo import TrimVideo

from .nodes.addAudio import AddAudio
from .nodes.imagesSave import SaveImages
from .nodes.pipVideo import PictureInPicture
from .nodes.videoTransition import VideoTransition
from .nodes.videoPlayback import ReverseVideo
from .nodes.genericFFmpeg import GenericFFmpeg
from .nodes.losslessRemux import RemuxVideo
from .nodes.streamAnalysis import AnalyzeStreams
from .nodes.keyframeAwareCutting import KeyframeTrim
from .nodes.filtergraph import ApplyFiltergraph
from .nodes.streamMapping import ApplyStreamMap
from .nodes.subtitle import HandleSubtitles
from .nodes.audioFilter import ApplyAudioFilter
from .nodes.LosslessCut import LosslessCut

from .nodes.videoFlip_v3 import VideoFlipV3
from .nodes.loadImageFromDir_v3 import LoadImagesFromDirectoryV3
from .nodes.imagesSave_v3 import SaveImagesV3
from .nodes.genericFFmpeg_v3 import GenericFFmpegV3
from .nodes.streamAnalysis_v3 import AnalyzeStreamsV3

# Batch 2 Imports
from .nodes.singleCuttingVideo_v3 import TrimVideoV3
from .nodes.multiCuttingVideo_v3 import SplitVideoV3
from .nodes.videoPlayback_v3 import ReverseVideoV3
from .nodes.losslessRemux_v3 import RemuxVideoV3
from .nodes.keyframeAwareCutting_v3 import KeyframeTrimV3

# Batch 3 Imports
from .nodes.mergingVideoByTwo_v3 import MergeVideosV3
from .nodes.mergingVideoByPlenty_v3 import MergeVideoBatchV3
from .nodes.stitchingVideo_v3 import StitchVideosV3
from .nodes.videoTransition_v3 import VideoTransitionV3
from .nodes.pipVideo_v3 import PictureInPictureV3

# Batch 4 Imports
from .nodes.addTextWatermark_v3 import AddTextWatermarkV3
from .nodes.addImgWatermark_v3 import AddImgWatermarkV3
from .nodes.addAudio_v3 import AddAudioV3
from .nodes.extractAudio_v3 import ExtractAudioV3
from .nodes.audioFilter_v3 import ApplyAudioFilterV3
from .nodes.subtitle_v3 import HandleSubtitlesV3
from .nodes.filtergraph_v3 import ApplyFiltergraphV3
from .nodes.streamMapping_v3 import ApplyStreamMapV3

# Batch 5 Imports
from .nodes.video2frames_v3 import Video2FramesV3
from .nodes.frames2video_v3 import Frames2VideoV3
from .nodes.LosslessCut_v3 import LosslessCutV3

NODE_CLASS_MAPPINGS = {
    # V3 Mappings
    "LoadImagesFromDirectoryV3": LoadImagesFromDirectoryV3,
    "SaveImagesV3": SaveImagesV3,
    "GenericFFmpegV3": GenericFFmpegV3,
    "AnalyzeStreamsV3": AnalyzeStreamsV3,
    "VideoFlipV3": VideoFlipV3,
    "TrimVideoV3": TrimVideoV3,
    "SplitVideoV3": SplitVideoV3,
    "ReverseVideoV3": ReverseVideoV3,
    "RemuxVideoV3": RemuxVideoV3,
    "KeyframeTrimV3": KeyframeTrimV3,
    "MergeVideosV3": MergeVideosV3,
    "MergeVideoBatchV3": MergeVideoBatchV3,
    "StitchVideosV3": StitchVideosV3,
    "VideoTransitionV3": VideoTransitionV3,
    "PictureInPictureV3": PictureInPictureV3,
    "AddTextWatermarkV3": AddTextWatermarkV3,
    "AddImgWatermarkV3": AddImgWatermarkV3,
    "AddAudioV3": AddAudioV3,
    "ExtractAudioV3": ExtractAudioV3,
    "ApplyAudioFilterV3": ApplyAudioFilterV3,
    "HandleSubtitlesV3": HandleSubtitlesV3,
    "ApplyFiltergraphV3": ApplyFiltergraphV3,
    "ApplyStreamMapV3": ApplyStreamMapV3,
    "Video2FramesV3": Video2FramesV3,
    "Frames2VideoV3": Frames2VideoV3,
    "LosslessCutV3": LosslessCutV3,
    "LosslessCut": LosslessCut,
    "ApplyFiltergraph": ApplyFiltergraph,
    "ApplyStreamMap": ApplyStreamMap,
    "HandleSubtitles": HandleSubtitles,
    "ApplyAudioFilter": ApplyAudioFilter,
    "AnalyzeStreams": AnalyzeStreams,
    "KeyframeTrim": KeyframeTrim,
    "RemuxVideo": RemuxVideo,
    "GenericFFmpeg": GenericFFmpeg,
    "Video2Frames": Video2Frames,
    "Frames2Video": Frames2Video,
    "AddTextWatermark": AddTextWatermark,
    "AddImgWatermark": AddImgWatermark,
    "VideoFlip": VideoFlip,
    "ExtractAudio": ExtractAudio,
    "LoadImagesFromDirectory": LoadImagesFromDirectory,
    "MergeVideos": MergeVideos,
    "MergeVideoBatch": MergeVideoBatch,
    "StitchVideos": StitchVideos,
    "SplitVideo": SplitVideo,
    "TrimVideo": TrimVideo,
    "AddAudio": AddAudio,
    "SaveImages": SaveImages,
    "PictureInPicture": PictureInPicture,
    "VideoTransition": VideoTransition,
    "ReverseVideo": ReverseVideo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagesFromDirectoryV3": "🔥Load Images from Directory (V3)",
    "SaveImagesV3": "🔥Save Images (V3)",
    "GenericFFmpegV3": "🔥Generic FFmpeg (V3)",
    "AnalyzeStreamsV3": "🔥Analyze Streams (V3)",
    "VideoFlipV3": "🔥Flip Video (V3)",
    "TrimVideoV3": "🔥Trim Video (V3)",
    "SplitVideoV3": "🔥Split Video (V3)",
    "ReverseVideoV3": "🔥Reverse Video (V3)",
    "RemuxVideoV3": "🔥Remux Video (V3)",
    "KeyframeTrimV3": "🔥Keyframe Trim (V3)",
    "MergeVideosV3": "🔥Merge Videos (V3)",
    "MergeVideoBatchV3": "🔥Merge Video Batch (V3)",
    "StitchVideosV3": "🔥Stitch Videos (V3)",
    "VideoTransitionV3": "🔥Video Transition (V3)",
    "PictureInPictureV3": "🔥Picture In Picture (V3)",
    "AddTextWatermarkV3": "🔥Add Text Watermark (V3)",
    "AddImgWatermarkV3": "🔥Add Image Watermark (V3)",
    "AddAudioV3": "🔥Add Audio (V3)",
    "ExtractAudioV3": "🔥Extract Audio (V3)",
    "ApplyAudioFilterV3": "🔥Apply Audio Filter (V3)",
    "HandleSubtitlesV3": "🔥Handle Subtitles (V3)",
    "ApplyFiltergraphV3": "🔥Apply Filtergraph (V3)",
    "ApplyStreamMapV3": "🔥Apply Stream Map (V3)",
    "Video2FramesV3": "🔥Video to Frames (V3)",
    "Frames2VideoV3": "🔥Frames to Video (V3)",
    "LosslessCutV3": "🔥Lossless Cut (V3)",
    "LosslessCut": "🔥Lossless Cut",
    "ApplyFiltergraph": "🔥Apply Filtergraph",
    "ApplyStreamMap": "🔥Apply Stream Map",
    "HandleSubtitles": "🔥Handle Subtitles",
    "ApplyAudioFilter": "🔥Apply Audio Filter",
    "AnalyzeStreams": "🔥Analyze Streams",
    "KeyframeTrim": "🔥Keyframe Trim",
    "RemuxVideo": "🔥Remux Video",
    "GenericFFmpeg": "🔥Generic FFmpeg",
    "Video2Frames": "🔥Video to Frames",
    "Frames2Video": "🔥Frames to Video",
    "AddTextWatermark": "🔥Add Text Watermark",
    "AddImgWatermark": "🔥Add Image Watermark",
    "VideoFlip": "🔥Flip Video",
    "ExtractAudio": "🔥Extract Audio",
    "LoadImagesFromDirectory": "🔥Load Images from Directory",
    "MergeVideos": "🔥Merge Videos",
    "MergeVideoBatch": "🔥Merge Video Batch",
    "StitchVideos": "🔥Stitch Videos",
    "SplitVideo": "🔥Split Video",
    "TrimVideo": "🔥Trim Video",
    "AddAudio": "🔥Add Audio",
    "SaveImages": "🔥Save Images",
    "PictureInPicture": "🔥Picture In Picture",
    "VideoTransition": "🔥Video Transition",
    "ReverseVideo": "🔥Reverse Video",
}
