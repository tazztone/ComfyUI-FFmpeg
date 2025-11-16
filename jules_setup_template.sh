#!/bin/bash
# Jules Environment Setup Script Template

# This script is a template to help you create a setup script for your Jules
# environment. You can customize it to install the packages and tools
# required for your project.

# --- Exit on Error ---
# The 'set -e' command ensures that the script will exit immediately if a
# command fails. This is a good practice for setup scripts to prevent
# unexpected behavior.
set -e

echo "--- Starting Environment Setup ---"

# --- Package Installation ---
# Add your package installation commands here.
# It's a good practice to update the package list before installing new packages.
#
# Example for Debian/Ubuntu-based systems:
# echo "Updating package list..."
# sudo apt-get update -y
#
# echo "Installing required packages..."
# sudo apt-get install -y <package-name-1> <package-name-2>

# Example for Python packages using pip:
# echo "Installing Python packages..."
# pip install -r requirements.txt

# Example for Node.js packages using npm:
# echo "Installing Node.js packages..."
# npm install

# --- Version Verification ---
# After installation, it's a good idea to verify that the correct versions
# of your tools are installed.
#
# Example:
# echo "--- Verifying Tool Versions ---"
# echo "Python version:"
# python3 --version
#
# echo "Node.js version:"
# node --version
#
# echo "Java version:"
# java -version

echo "--- Environment setup complete! ---"
