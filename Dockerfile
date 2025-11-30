FROM python:3.10-slim

# ffmpeg für Video-Zeug
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Alles ins Image kopieren (inkl. JSON!)
COPY . /app/

# Python-Libs installieren
RUN pip install --no-cache-dir -r requirements.txt

# Einstiegspunkt: unser RunPod-Handler
CMD ["python", "serverless_handler.py"]
