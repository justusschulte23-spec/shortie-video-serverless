import json
import requests
import base64
import os

# Loads the workflow JSON from file
def load_workflow():
    with open("Shortie_Video_erstellung.json", "r", encoding="utf-8") as f:
        return json.load(f)

# RunPod handler
def handler(event, context):
    try:
        workflow = load_workflow()

        # Insert user inputs if provided
        if "input_image" in event:
            # Expect base64 input image
            workflow["nodes"][0]["inputs"]["image"] = event["input_image"]

        return {
            "statusCode": 200,
            "body": workflow
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }
