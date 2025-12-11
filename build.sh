#!/bin/bash
set -e

APP_NAME="gemini-helper"

echo "Started build process for $APP_NAME..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker could not be found. Please install Docker to build the image."
    exit 1
fi

echo "Building Docker image..."
docker build . -t $APP_NAME

echo "Build complete. Image tagged as '$APP_NAME'."
echo "To run locally: docker run --env-file .env $APP_NAME"
