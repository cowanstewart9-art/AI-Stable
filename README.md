# AI Manager for Android

This is a Python-based Android application that acts as a manager for various AI functions. It includes structured logging, error handling (monitoring "bad exits"), and a mobile UI built with Kivy.

## Features

-   **AI Management**: Register and execute Python functions as AI modules.
-   **Error Monitoring**: Automatically catches and logs crashes ("bad exits") with full tracebacks, preventing the app from closing unexpectedly.
-   **History Logging**: Stores execution logs and error details in a local SQLite database (`ai_manager.db`).
-   **Mobile UI**: A simple interface to trigger AI functions and view logs on the device.

## Project Structure

-   `src/`: Source code.
    -   `main.py`: Entry point and UI.
    -   `manager.py`: Core logic for AI management.
    -   `logger.py`: Logging implementation.
-   `tests/`: Unit tests.
-   `buildozer.spec`: Configuration for Android build.
-   `Dockerfile`: Environment definition for automated building.
-   `build.sh`: Helper script for setup and building.

## How to Build (APK)

You can build the APK using Docker (recommended) or locally.

### Option 1: Docker (Automated)

This method requires Docker to be installed but handles all system dependencies for you.

1.  Run the build script:
    ```bash
    ./build.sh docker
    ```
2.  Once complete, the APK will be generated in the `bin/` directory.

### Option 2: Local Build

This method requires you to install system dependencies (Python, Java, Android SDK/NDK, etc.) on your machine.

1.  Setup the Python environment and install Python dependencies:
    ```bash
    ./build.sh local
    ```
2.  Run Buildozer:
    ```bash
    source venv/bin/activate
    buildozer android debug
    ```

## Development

To add new AI functions, use `manager.register_ai(name, function)` in `src/main.py`.

To run tests:
```bash
python3 -m unittest discover tests
```
