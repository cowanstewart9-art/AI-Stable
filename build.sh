#!/bin/bash
set -e

echo "=== AI Manager Build Script ==="

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install it."
    exit 1
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install kivy buildozer Cython

echo "Running tests..."
# We will create a test runner later, for now just a placeholder
python3 -m unittest discover tests

echo "Build environment ready."
echo "To build the Android APK, connect your phone or set up the environment completely and run:"
echo "buildozer android debug"
echo ""
echo "Note: Building for Android requires the Android SDK/NDK which buildozer will attempt to download."
echo "Ensure you have necessary system dependencies installed (e.g., openjdk-17-jdk, unzip, etc. on Linux)."
