# -----------------------------------------------------------------------------
# FINAL, CORRECTED, AND RELIABLE Dockerfile
# -----------------------------------------------------------------------------
# This version fixes the final "command not found" error by adding the
# Python scripts directory to the system's PATH.

# Use a specific version of python-slim for a smaller, more secure base.
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- THE CRUCIAL FIX ---
# Add the directory where pip installs command-line scripts to the system's PATH.
# This ensures that commands like "argos-translate-cli" can be found.
ENV PATH="/root/.local/bin:${PATH}"

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
# This command will now work because the system can find "argos-translate-cli".
# It updates the package index and installs ALL available language models.
RUN argos-translate-cli --update-package-index

# Copy the rest of your application's source code into the container.
COPY . .

# Expose the port that Streamlit will run on.
EXPOSE 8080

# The command to run when the container starts.
CMD ["streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
