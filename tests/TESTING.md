# Testing Guide for ComfyUI-FFmpeg

This guide covers running tests for the ComfyUI-FFmpeg custom nodes.

## Quick Start

```powershell
cd C:\_stability_matrix\Data\Packages\Comfy-new\custom_nodes\ComfyUI-FFmpeg

# ---------------------------------------------------------
# CRITICAL: ALWAYS USE THIS EXACT COMMAND FORMAT
# Do NOT use 'python' or 'pytest' directly.
# ---------------------------------------------------------

# Run all tests
..\..\venv\Scripts\python tests\run_tests.py

# Run with verbose output
..\..\venv\Scripts\python tests\run_tests.py -v

# Run only unit tests
..\..\venv\Scripts\python tests\run_tests.py unit/
```

---

## Test Structure

```
tests/
├── conftest.py          # Centralized ComfyUI mocking
├── pytest.ini           # Local pytest config (overrides parent)
├── run_tests.py         # Wrapper script for proper execution
├── unit/                # Fast unit tests (no FFmpeg needed)
│   └── test_func_unit.py
├── integration/         # Integration tests (require FFmpeg)
│   ├── test_nodes_general.py
│   ├── test_stream_analysis.py
│   └── test_lossless_cut.py  # Skipped (complex mocking)
└── videos/              # Test video assets (auto-generated)
```

---

## Test Categories

### Unit Tests (6 tests)

Fast tests that validate utility functions without FFmpeg.

| Test | Description |
|------|-------------|
| `test_validate_time_format` | Time format validation (`HH:MM:SS`) |
| `test_set_file_name` | Timestamped filename generation |
| `test_generate_template_string` | Frame sequence template strings |
| `test_video_type` | Video extension definitions |
| `test_audio_type` | Audio extension definitions |
| `test_clear_memory` | Memory cleanup function |

### Integration Tests (8 tests)

Tests that require FFmpeg installed and use node classes.

| Test | Description |
|------|-------------|
| `test_add_img_watermark` | Image watermark overlay |
| `test_add_text_watermark` | Text watermark overlay |
| `test_pip_video` | Picture-in-Picture effect |
| `test_merge_videos` | Video concatenation |
| `test_stitch_videos` | Side-by-side video stitching |
| `test_frames2video` | Image frames to video conversion |
| `test_stream_analysis` | Video metadata extraction |
| `test_keyframe_aware_cutting` | **Skipped** - Known flaky test |

---

## Test Markers

```bash
# Run by marker
pytest -m unit           # Fast, no FFmpeg
pytest -m integration    # Requires FFmpeg
```

---

## Known Skipped Tests

| Test | Reason |
|------|--------|
| `test_lossless_cut` | Complex mock interaction with `folder_paths` at import time |
| `test_keyframe_aware_cutting` | Known flaky test (per AGENTS.md) |

---

## How It Works

### Problem Solved

The IDE shows "No tests have been found" because:

1. **Parent `pytest.ini` Interference**: ComfyUI's root `pytest.ini` restricts pytest to `tests/` at the ComfyUI root level.
2. **ComfyUI Module Dependencies**: Nodes import `folder_paths` and `comfy` which don't exist in test environment.

### Solution

1. **`tests/conftest.py`**: Mocks ComfyUI modules (`folder_paths`, `comfy`) at module load time (before test collection).

2. **`tests/pytest.ini`**: Local config with empty `pythonpath =` to override parent settings.

3. **`tests/run_tests.py`**: Wrapper script that changes to `tests/` directory before running pytest.

---

## Adding New Tests

### Unit Tests

1. Create test file in `tests/unit/test_*.py`
2. Add `@pytest.mark.unit` marker
3. Import from `func` module (path is set up by conftest)

```python
import pytest

@pytest.mark.unit
def test_my_function():
    from func import my_function
    assert my_function("input") == "expected"
```

### Integration Tests

1. Create test file in `tests/integration/test_*.py`
2. Add `@pytest.mark.integration` marker
3. Import node classes directly (conftest provides mocks)

```python
import pytest
from nodes.my_node import MyNode

@pytest.mark.integration
def test_my_node():
    node = MyNode()
    result = node.execute(input_data)
    assert result is not None
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: folder_paths` | Mocks not loading - clear `__pycache__` and run via `run_tests.py` |
| "No tests found" in IDE | Run from `tests/` directory or use `run_tests.py` |
| `ModuleNotFoundError` (pytest) | **CRITICAL**: You are likely using the wrong python. Use `..\..\venv\Scripts\python` |
| Tests hang | Check FFmpeg is installed and in PATH |
| Import errors | Clear `__pycache__` directories |
| Parent pytest.ini override | Local `tests/pytest.ini` must have `pythonpath =` (empty) |
