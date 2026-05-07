import pytest
from nodes.keyframeAwareCutting_v3 import KeyframeTrimV3

def test_find_nearest_keyframe():
    keyframes = [0.0, 2.5, 5.0, 7.5, 10.0]

    # Test exact match
    assert KeyframeTrimV3._find_nearest_keyframe(5.0, keyframes) == 5.0

    # Test closer to lower
    assert KeyframeTrimV3._find_nearest_keyframe(2.0, keyframes) == 2.5
    assert KeyframeTrimV3._find_nearest_keyframe(1.0, keyframes) == 0.0

    # Test closer to higher
    assert KeyframeTrimV3._find_nearest_keyframe(3.0, keyframes) == 2.5
    assert KeyframeTrimV3._find_nearest_keyframe(4.0, keyframes) == 5.0

    # Test boundary cases
    assert KeyframeTrimV3._find_nearest_keyframe(-1.0, keyframes) == 0.0
    assert KeyframeTrimV3._find_nearest_keyframe(11.0, keyframes) == 10.0

    # Test halfway (should pick one, usually the lower one due to how min() works with equal values,
    # but we just want to ensure it doesn't crash and returns one of the nearest)
    result = KeyframeTrimV3._find_nearest_keyframe(1.25, keyframes)
    assert result in [0.0, 2.5]

def test_find_nearest_keyframe_empty():
    assert KeyframeTrimV3._find_nearest_keyframe(5.0, []) is None

def test_find_nearest_keyframe_single():
    assert KeyframeTrimV3._find_nearest_keyframe(5.0, [1.0]) == 1.0
