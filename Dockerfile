# Use an official Ubuntu as a parent image
#FROM ubuntu:latest
FROM python:3.9-slim

# Set environment variables to non-interactive (this avoids some prompts)
# ENV DEBIAN_FRONTEND noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev \
    curl \
    unzip

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python, pip and virtualenv
RUN pip install --upgrade pip && \
    pip install virtualenv && \
    virtualenv /venv

# Activate virtual environment and install requirements
COPY requirements.txt /requirements.txt
COPY setup.py /setup.py

RUN . /venv/bin/activate && \
    pip install --no-cache-dir -r /requirements.txt

CMD ["tail", "-f", "/dev/null"]
