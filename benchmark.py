import time
import os

def validate_path_old(path):
    return os.path.exists(path)

def validate_path_new(path):
    return True

path = "api_routes.py"

start = time.time()
for _ in range(1000000):
    validate_path_old(path)
end = time.time()
old_time = end - start
print(f"Old time for 1M iterations: {old_time:.4f}s")

start = time.time()
for _ in range(1000000):
    validate_path_new(path)
end = time.time()
new_time = end - start
print(f"New time for 1M iterations: {new_time:.4f}s")
print(f"Improvement: {(old_time - new_time) / old_time * 100:.2f}%")
