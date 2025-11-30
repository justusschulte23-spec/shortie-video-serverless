FROM runpod/comfyui:latest

# Copy workflow and code
COPY Shortie_Video_erstellung.json /workspace/Shortie_Video_erstellung.json
COPY main.py /workspace/main.py
COPY serverless_handler.py /workspace/serverless_handler.py
COPY requirements.txt /workspace/requirements.txt

# Install packages
RUN pip install --upgrade pip && \
    pip install -r /workspace/requirements.txt

# Expose ComfyUI port
EXPOSE 8188

# Start ComfyUI AND serverless handler
CMD bash -lc "
    echo '🚀 Starting ComfyUI...' &&
    python3 /ComfyUI/main.py --listen --port 8188 --disable-auto-launch &
    sleep 5 &&
    echo '🔥 Starting serverless handler...' &&
    python3 /workspace/serverless_handler.py
"
