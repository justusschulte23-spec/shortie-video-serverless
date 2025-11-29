import runpod
import json
import base64
import requests

# Load workflow once at cold start
with open("Shortie_Video_erstellung.json", "r", encoding="utf-8") as f:
    WORKFLOW = json.load(f)

COMFY_URL = "http://127.0.0.1:8188/prompt"   # internal ComfyUI endpoint

def build_workflow(event):
    """
    Insert user inputs into workflow before sending to ComfyUI.
    """
    wf = WORKFLOW.copy()

    if "input_image" in event:
        wf["nodes"]["0"]["inputs"]["image"] = event["input_image"]

    if "prompt" in event:
        wf["nodes"]["3"]["inputs"]["positive"] = event["prompt"]

    return wf


def handler(event):
    """
    This runs every time the serverless endpoint receives a job.
    """
    try:
        workflow_to_send = build_workflow(event)

        # Send workflow to ComfyUI
        response = requests.post(COMFY_URL, json=workflow_to_send)

        if response.status_code != 200:
            return {
                "statusCode": 500,
                "error": f"ComfyUI Error {response.status_code}: {response.text}"
            }

        result = response.json()

        return {
            "statusCode": 200,
            "result": result
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }


runpod.serverless.start({
    "handler": handler
})
