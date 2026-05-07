import sys
from unittest.mock import MagicMock
sys.modules['comfy'] = MagicMock()
sys.modules['comfy.model_management'] = MagicMock()
sys.modules['folder_paths'] = MagicMock()

import time
import os
import random

from func import video_type, audio_type

def benchmark():
    video_exts_tuple = video_type()
    video_exts_set = set(video_type())

    # Generate mock filenames
    filenames = []
    exts = list(video_exts_tuple) + ['.txt', '.png', '.jpg', '.pdf', '.docx']
    for i in range(1000000):
        filenames.append(f"file_{i}{random.choice(exts)}")

    start = time.time()
    res1 = []
    for filename in filenames:
        if filename.lower().endswith(video_exts_tuple):
            res1.append(filename)
    t1 = time.time() - start

    start = time.time()
    res2 = []
    for filename in filenames:
        if os.path.splitext(filename)[1].lower() in video_exts_set:
            res2.append(filename)
    t2 = time.time() - start

    print(f"Endswith tuple time: {t1:.4f}s")
    print(f"os.path.splitext set time: {t2:.4f}s")
    print(f"Improvement: {(t2-t1)/t2*100:.2f}%")

if __name__ == '__main__':
    benchmark()
