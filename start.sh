#!/bin/bash

echo "🚀 Starting ComfyUI..."
python3 /ComfyUI/main.py --listen --port 8188 --disable-auto-launch &

echo "⏳ Waiting for ComfyUI to start..."
sleep 5

echo "🔥 Starting serverless handler..."
python3 /workspace/serverless_handler.py

