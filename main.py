import json
import os
import requests
from pathlib import Path

# Pfad zur Workflow-Datei
WORKFLOW_PATH = Path(__file__).with_name("Shortie_Video_erstellung.json")

# ComfyUI endpoint
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188/prompt")


def _load_workflow() -> dict:
    """Workflow aus JSON laden."""
    with WORKFLOW_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def download_image(url: str, out_path: Path):
    """Bild über URL herunterladen und speichern."""
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    out_path.write_bytes(r.content)


def generate_video(prompt: str, image_url: str, duration: int = 6, negative: str = "") -> str:
    """Image-to-Video mit SVD-XT, gesteuert durch Text-Prompt."""

    # Workflow laden
    wf = _load_workflow()

    # ----------------------------------------
    # 1. Bild herunterladen & speichern
    # ----------------------------------------
    input_dir = Path("/workspace/input")
    input_dir.mkdir(parents=True, exist_ok=True)

    image_path = input_dir / "image.png"
    download_image(image_url, image_path)

    # Node 2 (VHS_LoadImagePath) → Bildpfad
    wf["nodes"][2]["widgets_values"]["image"] = str(image_path)

    # ----------------------------------------
    # 2. Prompt einsetzen
    # ----------------------------------------
    # Node 3: positive prompt
    wf["nodes"][3]["widgets_values"][0] = prompt

    # Node 4: negative prompt
    wf["nodes"][4]["widgets_values"][0] = negative

    # ----------------------------------------
    # 3. Dauer → Frames (18 FPS)
    # ----------------------------------------
    frames = int(duration * 18)  # 6 sek * 18 fps
    wf["nodes"][5]["widgets_values"][2] = frames

    # ----------------------------------------
    # 4. ComfyUI Request senden
    # ----------------------------------------
    payload = {"prompt": wf}

    response = requests.post(COMFY_URL, json=payload, timeout=600)

    if response.status_code != 200:
        raise RuntimeError(
            f"ComfyUI Error {response.status_code}: {response.text}"
        )

    # ----------------------------------------
    # 5. Output-Video finden
    # ----------------------------------------
    output_dir = Path("/workspace/ComfyUI/output")
    output_files = sorted(
        output_dir.glob("*.mp4"),
        key=lambda p: p.stat().st_mtime
    )

    if not output_files:
        raise RuntimeError("Kein Video im Output gefunden!")

    return str(output_files[-1])
