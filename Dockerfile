# Dockerfile for building the AI Manager APK
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=buildozer
ENV HOME_DIR=/home/$USER
ENV WORK_DIR=$HOME_DIR/app

# Install system dependencies
# Needs: python3, pip, git, zip, unzip, openjdk-17-jdk, autoconf, libtool, pkg-config, zlib1g-dev, libncurses5-dev, libncursesw5-dev, libtinfo5, cmake, libffi-dev, libssl-dev
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    libltdl-dev \
    cython3 \
    sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -d $HOME_DIR $USER && \
    echo "$USER ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USER
WORKDIR $WORK_DIR

# Install Buildozer and Kivy
RUN pip3 install --upgrade pip
RUN pip3 install --user buildozer kivy Cython

# Add local bin to PATH
ENV PATH=$HOME_DIR/.local/bin:$PATH

# Copy project files
COPY --chown=$USER:$USER . .

# Initialize buildozer (this might fail if spec exists, which it does, so we skip init)
# RUN buildozer init

# Command to run when container starts
# We don't run the build automatically by default to allow the user to debug,
# but we can set it as a command.
CMD ["buildozer", "android", "debug"]
