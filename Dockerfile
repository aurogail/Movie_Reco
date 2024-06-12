# Use an official Ubuntu as a parent image
#FROM ubuntu:latest
#FROM python:3.9-slim
FROM apache/airflow:2.9.1-python3.9

# Switch to root user to run apt-get
USER root

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev \
    curl \
    unzip

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Switch back to airflow user
USER airflow

# Set work directory
WORKDIR /opt/airflow

# Install Python, pip and virtualenv
#RUN pip install --upgrade pip
RUN pip install virtualenv

# Copy requirements file and install dependencies
COPY requirements.txt /opt/airflow/
COPY setup.py /opt/airflow/

# Create and activate a virtual environment in /opt/airflow/venv
RUN virtualenv /opt/airflow/venv && \
    /opt/airflow/venv/bin/pip install --no-cache-dir -r /opt/airflow/requirements.txt 

# RUN pip install --upgrade pip setuptools wheel \
#     && pip install --no-use-pep517 scikit-surprise

RUN pip install scikit-surprise

# Set environment variable for virtualenv
ENV PATH="/opt/airflow/venv/bin:$PATH"

# Activate virtual environment and install requirements
COPY requirements.txt /requirements.txt

CMD ["tail", "-f", "/dev/null"]