import os
import base64
import requests

API_HOST = "https://api.stability.ai"
ENGINE_ID = "stable-diffusion-xl-1024-v1-0"
API_KEY = os.getenv("STABILITY_API_KEY")

if API_KEY is None:
    raise Exception("Missing Stability API key.")

def get_image(text):
    try:
        response = requests.post(
            f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "text_prompts": [{"text": text}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )
        response.raise_for_status()  
        data = response.json()
        
        # Extract and return the first image artifact
        image_data = data["artifacts"][0]["base64"]
        return base64.b64decode(image_data)
    
    except requests.RequestException as e:
        print("Request failed:", e)
        return None 