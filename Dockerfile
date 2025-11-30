FROM python:3.10-slim

# ffmpeg fürs Video-Zeug
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Code ins Image kopieren
COPY . .

# Python-Libs installieren
RUN pip install --no-cache-dir -r requirements.txt

# Einstiegspunkt: unser RunPod-Handler
CMD ["python", "serverless_handler.py"]
