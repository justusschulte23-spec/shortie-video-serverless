#!/bin/bash

echo "🚀 Starte ComfyUI..."

# ComfyUI Ordner automatisch erzeugen falls nicht vorhanden
mkdir -p /workspace/ComfyUI
cd /workspace/ComfyUI

# ComfyUI klonen wenn nicht existiert
if [ ! -d "/workspace/ComfyUI/.git" ]; then
    git clone https://github.com/comfyanonymous/ComfyUI.git /workspace/ComfyUI
fi

# Start ComfyUI auf Port 8188
python3 main.py --listen --port 8188 &

echo "⏳ Warte, bis ComfyUI startet..."
sleep 5

echo "🎬 Starte Python-Server (RunPod Handler)..."
python3 /app/serverless_handler.py
