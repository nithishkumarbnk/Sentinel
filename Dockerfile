# -----------------------------------------------------------------------------
# Dockerfile for Sentinel Streamlit App
# -----------------------------------------------------------------------------

# Stage 1: Base Image with Python
# Use a specific version of python-slim for a smaller, more secure base.
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install essential system dependencies required by the Python libraries.
# - ffmpeg: For video/audio processing with moviepy.
# - git: Sometimes needed for installing packages directly from repositories.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's build cache.
# This step will only be re-run if requirements.txt changes.
COPY requirements.txt .

# Install Python dependencies from the requirements file.
# --no-cache-dir reduces the final image size.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Argos Translate setup script into the container.
# This script contains the corrected code to download language packs.
COPY setup_argos.py .

# Run the setup script to download and install the required language models.
RUN python setup_argos.py

# Copy the rest of your application's source code into the container.
# This includes main_app.py and any other modules.
COPY . .

# Expose the port that Streamlit will run on.
# Render's default port is 10000, but we can use 8080 as specified.
EXPOSE 8080

# The command to run when the container starts.
# This starts the Streamlit application.
CMD ["streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
