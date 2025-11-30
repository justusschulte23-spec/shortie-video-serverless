import json
import os
import tempfile
from pathlib import Path

import requests

# Pfad zur Workflow-Datei (liegt im gleichen Ordner)
WORKFLOW_PATH = Path(__file__).with_name("Shortie_Video_erstellung.json")

# ComfyUI-Endpoint – später kannst du den per ENV überschreiben
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188/prompt")


def _load_workflow() -> dict:
    """Workflow aus JSON laden."""
    with WORKFLOW_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def generate_video(prompt: str, duration: int = 5, audio_path: str | None = None) -> str:
    """
    Spricht mit ComfyUI und gibt den Pfad zu einer Video-Datei zurück.

    Aktuell: Minimal-Variante, damit der Server stabil läuft.
    Du kannst später die Comfy-Antwort auswerten und wirklich ein Video bauen.
    """

    # Workflow laden und Prompt einsetzen
    wf = _load_workflow()

    # TODO: Node-IDs ggf. anpassen – hier Beispiel wie vorher
    try:
        wf["nodes"]["3"]["inputs"]["positive"] = prompt
    except Exception:
        # Wenn die Struktur nicht passt, crashen wir nicht,
        # sondern geben eine sinnvolle Fehlermeldung nach außen.
        raise RuntimeError("Konnte 'positive' Prompt nicht in Workflow einsetzen.")

    # Payload so bauen, wie ComfyUI es erwartet
    payload = {"prompt": wf}

    # Request an ComfyUI
    try:
        response = requests.post(COMFY_URL, json=payload, timeout=600)
    except Exception as e:
        raise RuntimeError(f"Fehler beim Request an ComfyUI: {e}")

    if response.status_code != 200:
        raise RuntimeError(
            f"ComfyUI HTTP {response.status_code}: {response.text[:200]}"
        )

    # TODO: Hier später die echte Antwort auswerten und Bilder/Video verarbeiten
    # Für jetzt erzeugen wir eine Dummy-Datei, damit der Handler sauber durchläuft.
    tmp_dir = Path(tempfile.gettempdir())
    out_path = tmp_dir / "dummy_video.txt"
    out_path.write_text("Hier würde dein Video liegen.", encoding="utf-8")

    return str(out_path)
