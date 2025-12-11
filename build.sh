#!/bin/bash
set -e

echo "=== AI Manager Build Script ==="

FUNCTION=$1

usage() {
    echo "Usage: ./build.sh [local|docker]"
    echo "  local:  Setup python env and run tests (requires system deps for buildozer to run later)"
    echo "  docker: Build the APK using Docker (fully automated)"
    exit 1
}

if [ -z "$FUNCTION" ]; then
    usage
fi

if [ "$FUNCTION" == "local" ]; then
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
    python3 -m unittest discover tests

    echo "Build environment ready."
    echo "To build the Android APK locally, run:"
    echo "buildozer android debug"

elif [ "$FUNCTION" == "docker" ]; then
    echo "Building Docker image..."
    docker build -t ai-manager-builder .

    echo "Running Buildozer in Docker..."
    echo "The APK will be available in the 'bin' directory."

    # Run the container, mounting the current directory so the bin/ output is persisted
    # We mount as the current user to avoid permission issues if possible,
    # but the dockerfile uses 'buildozer' user.
    # Usually, buildozer inside docker writes to the internal directory.
    # We will mount the current directory to /home/buildozer/app

    docker run --rm -v "$(pwd):/home/buildozer/app" ai-manager-builder buildozer android debug

    echo "Build complete. Check the 'bin' directory for your APK."

else
    usage
fi
