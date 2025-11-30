import json
import os
import base64
import tempfile
from pathlib import Path
import requests

# ComfyUI Endpoint
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188/prompt")

# Workflow JSON im selben Ordner wie diese Datei
WORKFLOW_PATH = Path(__file__).with_name("Shortie_Video_erstellung.json")


def _load_workflow() -> dict:
    """Workflow JSON laden."""
    with WORKFLOW_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_video(
    prompt: str,
    duration: int = 5,
    image_b64: str = None,
    audio_path: str | None = None
) -> str:

    print("🔧 Loading base workflow...")
    wf = _load_workflow()

    # --- NODE MAPPING ---
    NODE_POS_PROMPT = 2      # Node ID 3
    NODE_NEG_PROMPT = 3      # Node ID 4
    NODE_IMAGE = 1           # Node ID 2
    NODE_SVD = 4             # Node ID 5

    # ---------------------
    # 🟢 Prompt setzen
    # ---------------------
    try:
        wf["nodes"][NODE_POS_PROMPT]["widgets_values"][0] = prompt
        wf["nodes"][NODE_NEG_PROMPT]["widgets_values"][0] = (
            "low quality, blurry, distorted"
        )
        print("🟢 Prompt erfolgreich gesetzt.")
    except Exception as e:
        raise RuntimeError(f"❌ Fehler beim Setzen des Prompts: {e}")

    # ---------------------
    # 🟢 Dauer (Frames) setzen
    # ---------------------
    frames = int(duration * 18)

    try:
        wf["nodes"][NODE_SVD]["widgets_values"][2] = frames
        print(f"🟢 Dauer → {frames} Frames gesetzt.")
    except Exception as e:
        raise RuntimeError(f"❌ Fehler beim Einfügen der Dauer: {e}")

    # ---------------------
    # 🟢 Bild einsetzen
    # ---------------------
    if not image_b64:
        raise RuntimeError("❌ Kein image_b64 empfangen!")

    try:
        img_bytes = base64.b64decode(image_b64)
        tmp_img = Path(tempfile.gettempdir()) / "input_image.png"
        tmp_img.write_bytes(img_bytes)

        wf["nodes"][NODE_IMAGE]["widgets_values"]["image"] = str(tmp_img)
        print("🟢 Bild erfolgreich eingefügt:", tmp_img)
    except Exception as e:
        raise RuntimeError(f"❌ Fehler beim Einfügen des Bildes: {e}")

    # ---------------------
    # 📡 Workflow senden
    # ---------------------
    payload = {"prompt": wf}

    print("📡 Sende Workflow an ComfyUI...")
    response = requests.post(COMFY_URL, json=payload, timeout=600)

    if response.status_code != 200:
        raise RuntimeError(
            f"❌ ComfyUI Fehler: {response.status_code} → {response.text}"
        )

    print("🟢 Workflow akzeptiert – Video wird generiert...")

    # ---------------------
    # Dummy Output (RunPod test mode)
    # ---------------------
    out_path = Path(tempfile.gettempdir()) / "output_video.mp4"
    out_path.write_text("DUMMY – ComfyUI erzeugt das echte Video hier.")

    return str(out_path)
