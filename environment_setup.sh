#!/bin/bash
# Jules Environment Setup Script

# This script verifies the pre-installed tools in the Jules environment and
# provides a framework for installing project-specific dependencies.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Verifying Pre-installed Software Versions ---"

# --- System Tools Verification ---
# These checks confirm that the tools listed in the Jules documentation are available.
echo "Verifying system tools..."
echo "--- Python ---"
python3 --version
pip --version
poetry --version
uv --version

echo "--- NodeJS ---"
node --version
npm --version
yarn --version
pnpm --version

echo "--- Java ---"
java -version

echo "--- Go ---"
go version

echo "--- Rust ---"
rustc --version
cargo --version

echo "--- Docker ---"
docker --version
docker compose version
echo "System tool verification complete."
echo ""

# --- Project-Specific Dependency Installation ---
# This section is for installing dependencies required by YOUR project.
# Customize the commands below based on your project's needs.

echo "--- Installing Project-Specific Dependencies ---"

# Example: Installing a system package with apt-get
# The 'tree' utility is a small, useful tool for listing directory contents.
echo "Installing 'tree' utility..."
sudo apt-get update -y
sudo apt-get install -y tree
echo "'tree' installation complete."
echo ""

# Example: Installing Python dependencies from a requirements file
# If your project has a requirements.txt, uncomment the following lines:
# if [ -f "requirements.txt" ]; then
#   echo "Installing Python dependencies from requirements.txt..."
#   pip install -r requirements.txt
#   echo "Python dependencies installed."
# else
#   echo "No requirements.txt found. Skipping pip installation."
# fi
# echo ""

# Example: Installing Node.js dependencies from a package.json file
# If your project has a package.json, uncomment the following lines:
# if [ -f "package.json" ]; then
#   echo "Installing Node.js dependencies from package.json..."
#   npm install
#   echo "Node.js dependencies installed."
# else
#   echo "No package.json found. Skipping npm installation."
# fi
# echo ""

echo "--- Environment setup complete! ---"
