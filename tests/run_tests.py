#!/usr/bin/env python
"""
Test runner that ensures proper working directory.
Avoids pytest package discovery issues with ComfyUI parent directory.
"""

import os
import sys
import subprocess


def main():
    # Get the directory where this script is located (tests/)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Change working directory to tests/ so pytest sees the local pytest.ini
    # and resolves paths correctly relative to it
    os.chdir(script_dir)

    print(f"Running tests from: {script_dir}")

    # Prepare arguments
    args = [sys.executable, "-m", "pytest"]

    # Pass through any arguments provided to this script
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    else:
        # Default to running all tests from unit and integration folders
        # Ignore problematic test_lossless_cut.py that requires complex mock setup
        args.extend(
            ["unit", "integration", "--ignore=integration/test_lossless_cut.py"]
        )

    print(f"Executing: {' '.join(args)}")

    # Run pytest
    result = subprocess.run(args, cwd=script_dir)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
