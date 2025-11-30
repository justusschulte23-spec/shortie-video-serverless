import json
import runpod

from main import generate_video


def handler(event: dict) -> dict:
    """
    RunPod Serverless Handler.
    Erwartetes Input-Format:

    {
        "input": {
            "prompt": "text prompt",
            "negative": "optional negative prompt",
            "duration": 6,
            "image_url": "https://..."
        }
    }
    """

    print("📩 Incoming event:", event)

    payload = event.get("input", {})

    # ------------------------------
    # Eingaben holen
    # ------------------------------
    prompt = payload.get("prompt")
    negative = payload.get("negative", "")
    duration = int(payload.get("duration", 6))
    image_url = payload.get("image_url")

    # Pflichtfelder prüfen
    if not prompt:
        return {"status": "error", "error": "Missing 'prompt' in input"}

    if not image_url:
        return {"status": "error", "error": "Missing 'image_url' in input"}

    try:
        print("🎬 Starting video generation ...")

        # Video generieren (URL statt Base64!)
        output_path = generate_video(
            prompt=prompt,
            image_url=image_url,
            duration=duration,
            negative=negative
        )

        print(f"🎉 Video generated at: {output_path}")

        return {
            "status": "success",
            "video_path": output_path
        }

    except Exception as e:
        print("❌ Error in handler:", e)
        return {
            "status": "error",
            "error": str(e),
        }


# RunPod handler starten
runpod.serverless.start({"handler": handler})
