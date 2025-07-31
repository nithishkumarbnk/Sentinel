# -----------------------------------------------------------------------------
# FINAL and CORRECTED Dockerfile - v3
# -----------------------------------------------------------------------------
# This version fixes the "streamlit: not found" error by adding the
# Python scripts directory to the system's PATH. This is the definitive
# solution for this type of runtime error.

FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- THE CRUCIAL FIX ---
# Add the directory where pip installs command-line scripts to the system's PATH.
# This ensures that commands like "streamlit" can be found at runtime.
ENV PATH="/root/.local/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# Install essential system dependencies.
# procps is needed for the pgrep command in our run.sh script.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker's build cache.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code into the container.
COPY . .

# Make the startup script executable
RUN chmod +x run.sh

# Expose the port that Streamlit will run on.
EXPOSE 8080

# The command to run when the container starts.
# This will now work because the system can find "streamlit".
CMD ["./run.sh"]
