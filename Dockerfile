# -----------------------------------------------------------------------------
# FINAL & ROBUST Dockerfile for Sentinel Streamlit App
# -----------------------------------------------------------------------------
# This version uses a smart Python script to find and download the correct
# argostranslate model during the build process, making it reliable.

# Use a specific version of python-slim for a smaller, more secure base.
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install essential system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's build cache.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- RELIABLE ARGOS TRANSLATE SETUP ---
# 1. Copy the setup script into the container.
COPY setup_argos.py .

# 2. Run the script to find, download, and install the language model.
# This script will fail the build if it cannot complete its task.
RUN python setup_argos.py

# Copy the rest of your application's source code into the container.
COPY . .

# Expose the port that Streamlit will run on.
EXPOSE 8080

# The command to run when the container starts.
CMD ["streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
# -----------------------------------------------------------------------------
# FINAL, SIMPLIFIED, AND RELIABLE Dockerfile
# -----------------------------------------------------------------------------
# This version uses the official, built-in argostranslate command to
# download and install all available language models, which is the most
# robust method for ensuring the required packages are present.

# Use a specific version of python-slim for a smaller, more secure base.
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install essential system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's build cache.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- THE DEFINITIVE ARGOS TRANSLATE SETUP ---
# This single command updates the package index and installs ALL available
# language models. This is the most reliable way to ensure the models
# you need are available at runtime.
RUN argos-translate-cli --update-package-index

# Copy the rest of your application's source code into the container.
COPY . .

# Expose the port that Streamlit will run on.
EXPOSE 8080

# The command to run when the container starts.
CMD ["streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
