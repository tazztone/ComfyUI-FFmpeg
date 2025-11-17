#!/bin/bash
# Jules Environment Setup Script

# This script verifies the pre-installed tools in the Jules environment and
# installs project-specific dependencies for ComfyUI-FFmpeg.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Verifying Pre-installed Software Versions ---"

# --- System Tools Verification ---
echo "Verifying system tools..."
echo "--- Python ---"
python3 --version
pip --version

echo "--- Docker ---"
docker --version
docker compose version
echo "System tool verification complete."
echo ""

# --- Project-Specific Dependency Installation ---
echo "--- Installing Project-Specific Dependencies ---"

# Install FFmpeg, a core dependency for this project.
echo "Installing FFmpeg..."
sudo apt-get update -y
sudo apt-get install -y ffmpeg
echo "FFmpeg installation complete."
echo ""

# Install Python dependencies from requirements files.
if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  pip install -r requirements.txt
  echo "Python dependencies from requirements.txt installed."
else
  echo "No requirements.txt found. Skipping pip installation."
fi
echo ""

if [ -f "requirements-test.txt" ]; then
  echo "Installing Python dependencies from requirements-test.txt..."
  pip install -r requirements-test.txt
  echo "Python dependencies from requirements-test.txt installed."
else
  echo "No requirements-test.txt found. Skipping pip installation."
fi
echo ""

echo "--- Environment setup complete! ---"
