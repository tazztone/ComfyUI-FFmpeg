from .nodes.addTextWatermark import AddTextWatermark
from .nodes.frames2video import Frames2Video
from .nodes.video2frames import Video2Frames
from .nodes.addImgWatermark import AddImgWatermark
from .nodes.videoFlip import VideoFlip
from .nodes.extractAudio import ExtractAudio
from .nodes.loadImageFromDir import LoadImagesFromDirectory
from .nodes.imageCopy import CopyImages
from .nodes.mergingVideoByTwo import MergeVideos
from .nodes.mergingVideoByPlenty import MergeVideoBatch
from .nodes.stitchingVideo import StitchVideos
from .nodes.multiCuttingVideo import SplitVideo
from .nodes.singleCuttingVideo import TrimVideo
from .nodes.addAudioLegacy import AddAudioFile
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

NODE_CLASS_MAPPINGS = {
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
    "CopyImages": CopyImages,
    "MergeVideos": MergeVideos,
    "MergeVideoBatch": MergeVideoBatch,
    "StitchVideos": StitchVideos,
    "SplitVideo": SplitVideo,
    "TrimVideo": TrimVideo,
    "AddAudio": AddAudio,
    "AddAudioFile": AddAudioFile,
    "SaveImages": SaveImages,
    "PictureInPicture": PictureInPicture,
    "VideoTransition": VideoTransition,
    "ReverseVideo": ReverseVideo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
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
    "CopyImages": "🔥Copy Images",
    "MergeVideos": "🔥Merge Videos",
    "MergeVideoBatch": "🔥Merge Video Batch",
    "StitchVideos": "🔥Stitch Videos",
    "SplitVideo": "🔥Split Video",
    "TrimVideo": "🔥Trim Video",
    "AddAudio": "🔥Add Audio",
    "AddAudioFile": "🔥Add Audio File",
    "SaveImages": "🔥Save Images",
    "PictureInPicture": "🔥Picture In Picture",
    "VideoTransition": "🔥Video Transition",
    "ReverseVideo": "🔥Reverse Video",
}
