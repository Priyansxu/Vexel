import os
import base64
import imghdr
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from io import BytesIO
from PIL import Image
from helpers.prompt import SYSTEM_PROMPT

load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

API_HOST = "https://api.stability.ai"
ENGINE_ID = "stable-diffusion-xl-1024-v1-0"

genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=SYSTEM_PROMPT,
)

def get_response(conversation):
    try:
        chat_session = model.start_chat(history=conversation)
        response = chat_session.send_message(conversation[-1]['parts'][0])
        return response.text if response and response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Error in get_response: {e}")
        return "Uhg my brain hurts, can you say that again?"

async def recognize_image(image_data, prompt):
    try:
        image_format = imghdr.what(None, image_data)
        if not image_format:
            return "Failed to determine image format."

        image = Image.open(BytesIO(image_data))
        response = model.generate_content([prompt, image])
        return response.text if response and hasattr(response, 'text') else "Failed to generate a response."
    except Exception as e:
        print(f"Error in recognize_image: {e}")
        return None

def get_image(text):
    try:
        if not STABILITY_API_KEY:
            raise ValueError("Missing Stability API key.")
        
        response = requests.post(
            f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {STABILITY_API_KEY}",
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
        image_data = response.json()["artifacts"][0]["base64"]
        return base64.b64decode(image_data)
    except Exception as e:
        print(f"Error in get_image: {e}")
        return None

def edit_image(image_bytes, prompt):
    try:
        response = requests.post(
            f"{API_HOST}/v1/generation/{ENGINE_ID}/image-to-image",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {STABILITY_API_KEY}",
            },
            files={
                "init_image": ('init_image.png', image_bytes, 'image/png'),
            },
            data={
                "image_strength": 0.35,
                "init_image_mode": "IMAGE_STRENGTH",
                "text_prompts[0][text]": prompt,
                "cfg_scale": 7,
                "samples": 1,
                "steps": 30,
            },
        )

        response.raise_for_status()
        image_data = response.json()["artifacts"][0]["base64"]
        return base64.b64decode(image_data)
    except Exception as e:
        print(f"Error in edit_image: {e}")
        return None