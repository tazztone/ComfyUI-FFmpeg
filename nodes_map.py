from .nodes.videoFlip_v3 import VideoFlipV3
from .nodes.loadImageFromDir_v3 import LoadImagesFromDirectoryV3
from .nodes.imagesSave_v3 import SaveImagesV3
from .nodes.genericFFmpeg_v3 import GenericFFmpegV3
from .nodes.streamAnalysis_v3 import AnalyzeStreamsV3
from .nodes.singleCuttingVideo_v3 import TrimVideoV3
from .nodes.multiCuttingVideo_v3 import SplitVideoV3
from .nodes.videoPlayback_v3 import ReverseVideoV3
from .nodes.losslessRemux_v3 import RemuxVideoV3
from .nodes.keyframeAwareCutting_v3 import KeyframeTrimV3
from .nodes.mergingVideoByTwo_v3 import MergeVideosV3
from .nodes.mergingVideoByPlenty_v3 import MergeVideoBatchV3
from .nodes.stitchingVideo_v3 import StitchVideosV3
from .nodes.videoTransition_v3 import VideoTransitionV3
from .nodes.pipVideo_v3 import PictureInPictureV3
from .nodes.addTextWatermark_v3 import AddTextWatermarkV3
from .nodes.addImgWatermark_v3 import AddImgWatermarkV3
from .nodes.addAudio_v3 import AddAudioV3
from .nodes.extractAudio_v3 import ExtractAudioV3
from .nodes.audioFilter_v3 import ApplyAudioFilterV3
from .nodes.subtitle_v3 import HandleSubtitlesV3
from .nodes.filtergraph_v3 import ApplyFiltergraphV3
from .nodes.streamMapping_v3 import ApplyStreamMapV3
from .nodes.video2frames_v3 import Video2FramesV3
from .nodes.frames2video_v3 import Frames2VideoV3
from .nodes.LosslessCut_v3 import LosslessCutV3

NODE_CLASS_MAPPINGS_V3 = [
    LoadImagesFromDirectoryV3,
    SaveImagesV3,
    GenericFFmpegV3,
    AnalyzeStreamsV3,
    VideoFlipV3,
    TrimVideoV3,
    SplitVideoV3,
    ReverseVideoV3,
    RemuxVideoV3,
    KeyframeTrimV3,
    MergeVideosV3,
    MergeVideoBatchV3,
    StitchVideosV3,
    VideoTransitionV3,
    PictureInPictureV3,
    AddTextWatermarkV3,
    AddImgWatermarkV3,
    AddAudioV3,
    ExtractAudioV3,
    ApplyAudioFilterV3,
    HandleSubtitlesV3,
    ApplyFiltergraphV3,
    ApplyStreamMapV3,
    Video2FramesV3,
    Frames2VideoV3,
    LosslessCutV3,
]
