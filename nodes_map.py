from .nodes.addTextWatermark import *
from .nodes.frames2video import *
from .nodes.video2frames import *
from .nodes.addImgWatermark import *
from .nodes.videoFlip import *
from .nodes.extractAudio import *
from .nodes.loadImageFromDir import *
from .nodes.imageCopy import *
from .nodes.imagePath2Tensor import *
from .nodes.mergingVideoByTwo import *
from .nodes.mergingVideoByPlenty import *
from .nodes.stitchingVideo import *
from .nodes.multiCuttingVideo import *
from .nodes.singleCuttingVideo import *
from .nodes.addAudioLegacy import *
from .nodes.addAudio import *
from .nodes.imagesSave import *
from .nodes.pipVideo import *
from .nodes.videoTransition import *
from .nodes.videoPlayback import *
from .nodes.genericFFmpeg import *
from .nodes.losslessRemux import *
from .nodes.streamAnalysis import *
from .nodes.losslesscut import *
from .nodes.filtergraph import *
from .nodes.streamMapping import *
from .nodes.subtitle import *
from .nodes.audioFilter import *

NODE_CLASS_MAPPINGS = {
    "Filtergraph": Filtergraph,
    "StreamMapping": StreamMapping,
    "Subtitle": Subtitle,
    "AudioFilter": AudioFilter,
    "StreamAnalysis": StreamAnalysis,
    "LosslessCut": LosslessCut,
    "LosslessRemux": LosslessRemux,
    "GenericFFmpeg": GenericFFmpeg,
    "Video2Frames": Video2Frames,
    "Frames2Video": Frames2Video,
    "AddTextWatermark": AddTextWatermark,
    "AddImgWatermark": AddImgWatermark,
    "VideoFlip": VideoFlip,
    "ExtractAudio": ExtractAudio,
    "LoadImageFromDir": LoadImageFromDir,
    "ImageCopy": ImageCopy,
    "ImagePath2Tensor": ImagePath2Tensor,
    "MergingVideoByTwo": MergingVideoByTwo,
    "MergingVideoByPlenty": MergingVideoByPlenty,
    "StitchingVideo": StitchingVideo,
    "MultiCuttingVideo": MultiCuttingVideo,
    "SingleCuttingVideo": SingleCuttingVideo,
    "AddAudio": AddAudio,
    "AddAudioLegacy": AddAudioLegacy,
    "ImagesSave": ImagesSave,
    "PipVideo": PipVideo,
    "VideoTransition": VideoTransition,
    "VideoPlayback": VideoPlayback,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Filtergraph": "🔥Filtergraph",
    "StreamMapping": "🔥StreamMapping",
    "Subtitle": "🔥Subtitle",
    "AudioFilter": "🔥AudioFilter",
    "StreamAnalysis": "🔥StreamAnalysis",
    "LosslessCut": "🔥LosslessCut",
    "LosslessRemux": "🔥LosslessRemux",
    "GenericFFmpeg": "🔥GenericFFmpeg",
    "Video2Frames": "🔥Video2Frames",
    "Frames2Video": "🔥Frames2Video",
    "AddTextWatermark": "🔥AddTextWatermark",
    "AddImgWatermark": "🔥AddImgWatermark",
    "VideoFlip": "🔥VideoFlip",
    "ExtractAudio": "🔥ExtractAudio",
    "LoadImageFromDir": "🔥LoadImageFromDir",
    "ImageCopy": "🔥ImageCopy",
    "ImagePath2Tensor": "🔥ImagePath2Tensor",
    "MergingVideoByTwo": "🔥MergingVideoByTwo",
    "MergingVideoByPlenty": "🔥MergingVideoByPlenty",
    "StitchingVideo": "🔥StitchingVideo",
    "MultiCuttingVideo": "🔥MultiCuttingVideo",
    "SingleCuttingVideo": "🔥SingleCuttingVideo",
    "AddAudio": "🔥AddAudio",
    "AddAudioLegacy": "🔥AddAudio (from path)",
    "ImagesSave": "🔥ImagesSave",
    "PipVideo": "🔥PipVideo",
    "VideoTransition": "🔥VideoTransition",
    "VideoPlayback": "🔥VideoPlayback",
}
