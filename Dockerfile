# Use Python slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all files to container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Ollama Setup ---
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama && \
    chmod +x /usr/bin/ollama

# --- Argos Translate Setup ---
RUN python -c "import argostranslate.package as p; p.update_package_index(); p.install_from_codes(['en', 'te'])"

# Expose the port Streamlit runs on
EXPOSE 7860

# Create and use a startup script
RUN echo '#!/bin/bash' > /start.sh && \
    echo 'ollama serve &' >> /start.sh && \
    echo 'sleep 5' >> /start.sh && \
    echo 'ollama pull llama3' >> /start.sh && \
    echo 'streamlit run main_app.py --server.port=7860 --server.address=0.0.0.0' >> /start.sh && \
    chmod +x /start.sh

# Run the app
CMD ["/start.sh"]
