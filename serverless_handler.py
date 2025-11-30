import json
import runpod

from main import generate_video


def handler(event: dict) -> dict:
    payload = event.get("input", {})

    prompt = payload.get("prompt")
    negative = payload.get("negative", "")
    duration = int(payload.get("duration", 6))
    image_url = payload.get("image_url")

    if not prompt:
        return {"status": "error", "error": "Missing 'prompt' in input"}

    if not image_url:
        return {"status": "error", "error": "Missing 'image_url' in input"}

    try:
        output_path = generate_video(
            prompt=prompt,
            image_url=image_url,
            duration=duration,
            negative=negative
        )

        return {
            "status": "success",
            "video_path": output_path
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


runpod.serverless.start({"handler": handler})
