import base64
import json
import requests
import runpod

from main import generate_video


def handler(event: dict) -> dict:
    """
    RunPod serverless Handler.
    """

    print("📥 Incoming event:", event)

    payload = event.get("input", event)

    prompt = payload.get("prompt")
    duration = int(payload.get("duration", 5))
    image_url = payload.get("image_url")
    audio_b64 = payload.get("audio")

    if not prompt:
        return {"status": "error", "error": "Missing 'prompt' in input"}

    if not image_url:
        return {"status": "error", "error": "Missing 'image_url' in input"}

    # ---------------------------
    # 📌 Schritt 1: Bild von URL laden
    # ---------------------------
    try:
        print("🖼 Downloading image from:", image_url)
        img_data = requests.get(image_url).content
        image_b64 = base64.b64encode(img_data).decode("utf-8")
    except Exception as e:
        return {"status": "error", "error": f"Failed to download image: {e}"}

    # ---------------------------
    # 📌 Schritt 2: Audio speichern (falls vorhanden)
    # ---------------------------
    audio_path = None
    if audio_b64:
        try:
            audio_bytes = base64.b64decode(audio_b64)
            audio_path = "/tmp/input_audio.mp3"
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)
        except Exception as e:
            return {"status": "error", "error": f"Invalid audio base64: {e}"}

    # ---------------------------
    # 📌 Schritt 3: Video generieren
    # ---------------------------
    print("🎬 Starting video generation ...")
    output_path = generate_video(prompt, duration, image_b64, audio_path)

    # ---------------------------
    # 📌 Schritt 4: Video zurückgeben
    # ---------------------------
    print("✅ Video ready, encoding to base64")

    with open(output_path, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode("utf-8")

    return {
        "status": "success",
        "video_base64": video_b64
    }


runpod.serverless.start({"handler": handler})
