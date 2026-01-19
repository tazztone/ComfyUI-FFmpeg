import os
import sys
import shutil
from unittest.mock import MagicMock
import pytest

# Add package root to path so we can import nodes/func
# This assumes running from tests/ directory or its subdirs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- MOCKING SETUP ---
# We must mock ComfyUI modules BEFORE they are imported by the nodes during test collection.
# This code runs when pytest imports conftest.py, which happens before test checking.

# Create temp directories for mocks
test_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_output"))
test_temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_temp"))
os.makedirs(test_output_dir, exist_ok=True)
os.makedirs(test_temp_dir, exist_ok=True)

# Mock folder_paths
mock_folder_paths = MagicMock()
mock_folder_paths.get_output_directory.return_value = test_output_dir
mock_folder_paths.get_temp_directory.return_value = test_temp_dir

# Check if folder_paths is already in modules (unlikely but safe to check)
if "folder_paths" not in sys.modules:
    sys.modules["folder_paths"] = mock_folder_paths

# Mock comfy
if "comfy" not in sys.modules:
    sys.modules["comfy"] = MagicMock()

# Mock comfy.model_management
if "comfy.model_management" not in sys.modules:
    sys.modules["comfy.model_management"] = MagicMock()

# --- Mock comfy_api for V3 nodes ---
# Create a mock for io types that behave like real classes


class MockComfyNode:
    """Base class for V3 nodes in test environment."""

    pass


class MockSchema:
    """Mock Schema class."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MockNodeOutput(tuple):
    """Mock NodeOutput that behaves like a tuple."""

    def __new__(cls, *args):
        return super().__new__(cls, args)


class MockInputType:
    """Mock for io.String, io.Int, io.Float, etc."""

    @staticmethod
    def Input(name, *args, **kwargs):
        m = MagicMock(name=name)
        m.name = name
        return m

    @staticmethod
    def Output(**kwargs):
        return MagicMock()


class MockHidden:
    """Mock for io.Hidden"""

    @staticmethod
    def Input(name, *args, **kwargs):
        m = MagicMock(name=name)
        m.name = name
        return m


# Build mock io module
mock_io = MagicMock()
mock_io.ComfyNode = MockComfyNode
mock_io.Schema = MockSchema
mock_io.NodeOutput = MockNodeOutput
mock_io.String = MockInputType
mock_io.Int = MockInputType
mock_io.Float = MockInputType
mock_io.Boolean = MockInputType
mock_io.Combo = MockInputType
mock_io.Image = MockInputType
mock_io.Audio = MockInputType
mock_io.Hidden = MockHidden

# Build mock comfy_api module structure
mock_comfy_api = MagicMock()
mock_comfy_api_latest = MagicMock()
mock_comfy_api_latest.io = mock_io


class MockComfyExtension:
    """Mock ComfyExtension class."""

    pass


mock_comfy_api_latest.ComfyExtension = MockComfyExtension

if "comfy_api" not in sys.modules:
    sys.modules["comfy_api"] = mock_comfy_api
if "comfy_api.latest" not in sys.modules:
    sys.modules["comfy_api.latest"] = mock_comfy_api_latest
if "comfy_api.latest.io" not in sys.modules:
    sys.modules["comfy_api.latest.io"] = mock_io


# Clean up at end of session
@pytest.fixture(scope="session", autouse=True)
def cleanup_environment():
    yield
    # Cleanup after session
    if os.path.exists(test_output_dir):
        try:
            shutil.rmtree(test_output_dir)
        except PermissionError:
            pass  # Sometimes windows holds locks
    if os.path.exists(test_temp_dir):
        try:
            shutil.rmtree(test_temp_dir)
        except PermissionError:
            pass
