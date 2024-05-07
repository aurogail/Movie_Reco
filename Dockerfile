# Use an official Ubuntu as a parent image
#FROM ubuntu:latest
FROM python:3.8-slim

# Set environment variables to non-interactive (this avoids some prompts)
ENV DEBIAN_FRONTEND noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev \
    curl \
    unzip

# Install rclone
RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip && \
    unzip rclone-current-linux-amd64.zip && \
    cd rclone-*-linux-amd64 && \
    cp rclone /usr/bin/ && \
    chown root:root /usr/bin/rclone && \
    chmod 755 /usr/bin/rclone && \
    rm -rf /var/lib/apt/lists/* rclone-*-linux-amd64 rclone-current-linux-amd64.zip

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# Install requirements
# COPY requirements.txt /requirements.txt
# RUN pip install --no-cache-dir -r /requirements.txt

# Define the entry point
ENTRYPOINT ["rclone"]

# Install Python, pip and virtualenv
RUN pip install --upgrade pip && \
    pip install virtualenv && \
    virtualenv /venv

# Activate virtual environment and install requirements
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

RUN . /venv/bin/activate && \
    pip install --no-cache-dir -r /requirements.txt