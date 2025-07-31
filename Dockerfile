# -----------------------------------------------------------------------------
# FINAL, FOOLPROOF Dockerfile
# -----------------------------------------------------------------------------
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "-m", "streamlit", "run", "main_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
