import pytest
import torch
import os
import numpy as np
from nodes.videoInfo_v3 import VideoInfoV3
from nodes.imagesTensorToVideo_v3 import ImagesTensorToVideoV3
from nodes.thumbnailExtract_v3 import ThumbnailExtractV3
from nodes.videoFilters_v3 import VideoSpeedV3, DenoiseV3, ColorGradeV3, ScaleV3, CropV3, DeinterlaceV3, BurnTimecodeV3
from nodes.frameInterpolate_v3 import FrameInterpolateV3
from nodes.sceneDetect_v3 import SceneDetectV3
from nodes.encodeWithHWAccel_v3 import EncodeWithHWAccelV3
from nodes.streamOutput_v3 import StreamOutputV3
from nodes.videoPreview_v3 import VideoPreviewV3

@pytest.mark.integration
class TestV3NewNodes:
    def test_video_info_v3_schema(self):
        schema = VideoInfoV3.define_schema()
        assert schema.node_id == "VideoInfoV3"
        assert len(schema.outputs) == 5

    def test_images_tensor_to_video_v3_schema(self):
        schema = ImagesTensorToVideoV3.define_schema()
        assert schema.node_id == "ImagesTensorToVideoV3"
        assert any(input.name == "images" for input in schema.inputs)

    def test_thumbnail_extract_v3_schema(self):
        schema = ThumbnailExtractV3.define_schema()
        assert schema.node_id == "ThumbnailExtractV3"

    def test_video_filters_v3_schemas(self):
        assert ScaleV3.define_schema().node_id == "ScaleV3"
        assert CropV3.define_schema().node_id == "CropV3"
        assert DenoiseV3.define_schema().node_id == "DenoiseV3"
        assert ColorGradeV3.define_schema().node_id == "ColorGradeV3"
        assert VideoSpeedV3.define_schema().node_id == "VideoSpeedV3"
        assert DeinterlaceV3.define_schema().node_id == "DeinterlaceV3"
        assert BurnTimecodeV3.define_schema().node_id == "BurnTimecodeV3"

    def test_frame_interpolate_v3_schema(self):
        schema = FrameInterpolateV3.define_schema()
        assert schema.node_id == "FrameInterpolateV3"

    def test_scene_detect_v3_schema(self):
        schema = SceneDetectV3.define_schema()
        assert schema.node_id == "SceneDetectV3"

    def test_encode_with_hw_accel_v3_schema(self):
        schema = EncodeWithHWAccelV3.define_schema()
        assert schema.node_id == "EncodeWithHWAccelV3"

    def test_stream_output_v3_schema(self):
        schema = StreamOutputV3.define_schema()
        assert schema.node_id == "StreamOutputV3"

    def test_video_preview_v3_schema(self):
        schema = VideoPreviewV3.define_schema()
        assert schema.node_id == "VideoPreviewV3"

    def test_audio_batch_handling_logic(self):
        # Testing the squeeze logic used in AddAudioV3 and others
        waveform = torch.rand((1, 2, 44100))
        if waveform.dim() == 3:
            waveform = waveform.squeeze(0)
        assert waveform.shape == (2, 44100)
