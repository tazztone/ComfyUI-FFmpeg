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
