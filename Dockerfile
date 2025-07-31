# -----------------------------------------------------------------------------
# FINAL, FOOLPROOF Dockerfile
# -----------------------------------------------------------------------------
# This version makes zero assumptions about the environment. It uses the
# 'python -m' command, which is the most reliable way to run a package
# and bypasses all issues with PATH or script locations.

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

# Copy the rest of your application's source code into the container.
COPY . .

# Expose the port that Streamlit will run on.
EXPOSE 8080

# The command to run when the container starts.
# This is the most robust method: it tells Python to run the streamlit
# module directly, which does not depend on any system PATH variables.
CMD ["python", "-m", "streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
