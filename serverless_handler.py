import base64
import json

import runpod

from main import generate_video


def handler(event: dict) -> dict:
    """
    RunPod serverless Handler.

    Erwartetes Event-Format (so schickst du es in RunPod):
    {
      "input": {
        "prompt": "dein prompt",
        "duration": 5,
        "audio": "BASE64_MP3"   # optional
      }
    }
    """

    print("📥 Incoming event:", event)

    # Bei /run liegt alles unter "input"
    payload = event.get("input", event)

    prompt = payload.get("prompt")
    duration = int(payload.get("duration", 5))
    audio_b64 = payload.get("audio")

    if not prompt:
        return {"status": "error", "error": "Missing 'prompt' in input"}

    audio_path = None

    try:
        # Falls Audio mitgeschickt wird -> nach /tmp schreiben
        if audio_b64:
            try:
                audio_bytes = base64.b64decode(audio_b64)
            except Exception as e:
                return {"status": "error", "error": f"Invalid audio base64: {e}"}

            audio_path = "/tmp/input_audio.mp3"
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)

        print("🚀 Starting video generation ...")
        output_path = generate_video(prompt, duration, audio_path)

        print(f"✅ Video generated at {output_path}, encoding as base64 ...")
        with open(output_path, "rb") as f:
            video_b64 = base64.b64encode(f.read()).decode("utf-8")

        return {
            "status": "success",
            "video_base64": video_b64,
        }

    except Exception as e:
        # KEIN Crash – wir geben den Fehler nur raus
        print("❌ Error in handler:", e)
        return {
            "status": "error",
            "error": str(e),
        }


runpod.serverless.start({"handler": handler})
