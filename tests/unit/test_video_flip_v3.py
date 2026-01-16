import pytest
import sys
from unittest.mock import MagicMock


# Define dummy V3 components if not present in the environment
# This allows us to test the class structure even if the real comfy package isn't installed in the test env
def dummy_define_schema(schema_def):
    def decorator(cls):
        cls._V3_SCHEMA = schema_def
        return cls

    return decorator


def dummy_async_comfy_entrypoint(func):
    return func


# Mock comfy.nodes.package for import
# We need to ensure 'comfy' and 'comfy.nodes' exist before 'comfy.nodes.package'
if "comfy" not in sys.modules:
    sys.modules["comfy"] = MagicMock()
if "comfy.nodes" not in sys.modules:
    sys.modules["comfy.nodes"] = MagicMock()

# Setup the package mock
mock_package = MagicMock()
mock_package.define_schema = dummy_define_schema
mock_package.async_comfy_entrypoint = dummy_async_comfy_entrypoint
sys.modules["comfy.nodes.package"] = mock_package


@pytest.mark.unit
def test_videoflip_v3_structure():
    # Import the node
    from nodes.videoFlip_v3 import VideoFlipV3

    # Check if schema is attached
    assert hasattr(VideoFlipV3, "_V3_SCHEMA")
    schema = VideoFlipV3._V3_SCHEMA

    # Validate schema fields
    assert schema["name"] == "🔥VideoFlip (V3)"
    assert schema["category"] == "🔥FFmpeg/Editing"
    assert "video" in schema["inputs"]
    assert "flip_type" in schema["inputs"]
    assert "output_path" in schema["outputs"]

    # Check method existence
    node = VideoFlipV3()
    assert hasattr(node, "flip_video")
