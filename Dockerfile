# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install system dependencies and Intel RealSense SDK
RUN apt-get update && apt-get install -y \
    gnupg2 \
    cmake \
    pkg-config \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff5-dev \
    libdc1394-22-dev \
    libv4l-dev \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Add Intel RealSense repository
RUN apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
RUN echo "deb https://librealsense.intel.com/Debian/apt-repo bionic main" >> /etc/apt/sources.list

# Install Intel RealSense SDK
RUN apt-get update && apt-get install -y \
    librealsense2-dkms \
    librealsense2-utils \
    librealsense2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run the script when the container launches
CMD ["python", "record_realsense.py"]
