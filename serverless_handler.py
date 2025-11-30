import runpod
import json
import base64
from main import generate_video  # <- dein main.py Funktions-Einstiegspunkt

def handler(event):
    """
    RunPod serverless handler.
    Expected event format:
    {
        "prompt": "your prompt",
        "duration": 5,
        "audio": "base64encoded_mp3" (optional)
    }
    """

    print("🔄 Incoming event:", event)

    prompt = event.get("prompt", None)
    duration = event.get("duration", 5)
    audio = event.get("audio", None)

    if prompt is None:
        return {"error": "Missing prompt"}

    # Falls Audio Base64 geliefert wurde
    audio_path = None
    if audio:
        audio_path = "/tmp/input_audio.mp3"
        with open(audio_path, "wb") as f:
            f.write(base64.b64decode(audio))

    print("🎬 Starting video generation...")
    output_path = generate_video(prompt, duration, audio_path)

    print("📤 Encoding output video...")
    with open(output_path, "rb") as f:
        video_data = base64.b64encode(f.read()).decode("utf-8")

    return {
        "status": "success",
        "video_base64": video_data
    }


runpod.serverless.start({"handler": handler})
