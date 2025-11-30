import json
import os
import base64
import tempfile
from pathlib import Path
import requests

# ComfyUI endpoint (in RunPod im Container läuft ComfyUI auf localhost)
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188/prompt")

# Workflow-Datei im selben Ordner
WORKFLOW_PATH = Path(__file__).with_name("Shortie_Video_erstellung.json")


def _load_workflow() -> dict:
    """Workflow aus JSON laden."""
    with WORKFLOW_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_video(
    prompt: str,
    duration: int = 5,
    image_b64: str = None,
    audio_path: str | None = None
) -> str:
    """
    Baut den Workflow, setzt Prompt + Bild + Dauer.
    Schickt an ComfyUI und gibt Pfad zur erzeugten Datei zurück.
    """

    print("🔧 Loading base workflow...")
    wf = _load_workflow()

    # ⿡ Prompt einsetzen (SVD Conditioning → Node ID 17)
    try:
        wf["nodes"]["17"]["inputs"]["positive"] = prompt
        print("🟢 Prompt erfolgreich eingesetzt.")
    except Exception as e:
        raise RuntimeError(f"❌ Konnte Prompt nicht in Workflow einfügen: {e}")

    # ⿢ Dauer einfügen (FPS = 18 → Frames = Dauer * 18)
    frames = int(duration * 18)

    try:
        wf["nodes"]["17"]["inputs"]["video_frames"] = frames
        print(f"🟢 Dauer → {frames} Frames gesetzt.")
    except Exception as e:
        raise RuntimeError(f"❌ Konnte Dauer nicht einsetzen: {e}")

    # ⿣ Bild einsetzen
    if not image_b64:
        raise RuntimeError("❌ Kein image_b64 empfangen – n8n sendet kein Bild!")

    try:
        img_bytes = base64.b64decode(image_b64)
        tmp_img = Path(tempfile.gettempdir()) / "input_image.png"
        tmp_img.write_bytes(img_bytes)

        # In Workflow einfügen (Node 3 = VHS_LoadImagePath)
        wf["nodes"]["3"]["inputs"]["image"] = str(tmp_img)
        print("🟢 Bild wurde in Workflow gesetzt:", tmp_img)
    except Exception as e:
        raise RuntimeError(f"❌ Fehler beim Einsetzen des Bildes: {e}")

    # ⿤ Audio einfügen (falls vorhanden)
    if audio_path:
        print("🎵 Audio wird genutzt:", audio_path)

    # ⿥ Payload → ComfyUI schicken
    payload = {"prompt": wf}

    print("📡 Sende Workflow an ComfyUI...")
    try:
        response = requests.post(COMFY_URL, json=payload, timeout=600)
    except Exception as e:
        raise RuntimeError(f"❌ Fehler bei Request an ComfyUI: {e}")

    if response.status_code != 200:
        raise RuntimeError(f"❌ ComfyUI HTTP Error: {response.status_code} → {response.text}")

    print("🟢 ComfyUI hat den Workflow akzeptiert. Warte auf Output...")

    # ⿦ Dummy output erzeugen (weil wir nur Base64 testen)
    out_path = Path(tempfile.gettempdir()) / "output_video.mp4"
    out_path.write_text("DUMMY – hier würde ComfyUI das Video ablegen.")

    return str(out_path)
