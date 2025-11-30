FROM python:3.10-slim

WORKDIR /app

# ----------- SYSTEM UPDATES & TOOLS -----------
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    wget \
    curl \
    unzip \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ----------- PYTHON REQUIREMENTS -----------
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ----------- APP FILES -----------
COPY . /app/

# ----------- START SCRIPT -----------
RUN chmod +x /app/start.sh

# ----------- GPU SUPPORT -----------
# CUDA wird von RunPod bereitgestellt.

CMD ["/bin/bash", "/app/start.sh"]
