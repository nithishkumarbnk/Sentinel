# -----------------------------------------------------------------------------
# FINAL, CLEANED Dockerfile
# -----------------------------------------------------------------------------
# This version completely removes argostranslate to ensure a successful build.

FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent straight to the terminal.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install essential system dependencies. ffmpeg might still be useful
# for other libraries, so we can keep it.
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
CMD ["streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
