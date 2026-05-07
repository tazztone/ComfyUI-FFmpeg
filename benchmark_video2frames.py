import time
import os
import shutil
import tempfile
import torch
import numpy as np
from PIL import Image

# Dummy function to mimic what Video2FramesV3 does
def benchmark():
    # Setup dummy images
    temp_dir = tempfile.mkdtemp()
    num_frames = 100
    for i in range(num_frames):
        img = Image.fromarray(np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8))
        img.save(os.path.join(temp_dir, f"{i:05d}.png"))

    frame_files = sorted(os.listdir(temp_dir))
    frame_files = [os.path.join(temp_dir, f) for f in frame_files]
    images = [Image.open(f) for f in frame_files]

    output_dir = tempfile.mkdtemp()

    start_time = time.time()

    # Old logic: decoding and re-encoding PNG frames
    for i, frame in enumerate(images):
        frame.save(os.path.join(output_dir, f"frame_{i:05d}.png"))

    old_time = time.time() - start_time

    shutil.rmtree(output_dir)
    output_dir = tempfile.mkdtemp()

    start_time = time.time()

    # New logic: shutil.copy2
    for i, frame_file in enumerate(frame_files):
        shutil.copy2(frame_file, os.path.join(output_dir, f"frame_{i:05d}.png"))

    new_time = time.time() - start_time

    print(f"Old logic time: {old_time:.4f}s")
    print(f"New logic time: {new_time:.4f}s")
    print(f"Improvement: {old_time / new_time:.2f}x faster")

    shutil.rmtree(temp_dir)
    shutil.rmtree(output_dir)

benchmark()
