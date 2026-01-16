import os
import base64
import imghdr
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image
from helpers.prompt import SYSTEM_PROMPT

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

GEMINI_MODEL = "gemini-2.5-flash-lite"
CF_MODEL = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
CF_API_HOST = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run"

client = genai.Client(api_key=GEMINI_API_KEY)

generation_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    system_instruction=SYSTEM_PROMPT,
)

def get_response(conversation):
    try:
        chat = client.chats.create(
            model=GEMINI_MODEL,
            config=generation_config,
            history=conversation[:-1]
        )
        response = chat.send_message(conversation[-1]["parts"][0])
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
        if image.mode == "RGBA":
            image = image.convert("RGB")

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt, image],
            config=generation_config
        )
        return response.text if response and hasattr(response, "text") else "Failed to generate a response."
    except Exception as e:
        print(f"Error in recognize_image: {e}")
        return None

def get_image(prompt):
    try:
        if not CF_API_TOKEN or not CF_ACCOUNT_ID:
            raise ValueError("Missing Cloudflare credentials.")

        response = requests.post(
            f"{CF_API_HOST}/{CF_MODEL}",
            headers={
                "Authorization": f"Bearer {CF_API_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "prompt": prompt,
                "width": 1024,
                "height": 1024,
                "num_steps": 20,
                "guidance": 7.5,
            },
        )
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error in get_image: {e}")
        return None

def edit_image(image_bytes, prompt):
    try:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "prompt": prompt,
            "image": [image_b64],
            "strength": 0.35,
            "guidance": 7.5,
            "num_steps": 20
        }
        response = requests.post(
            f"{CF_API_HOST}/{CF_MODEL}",
            headers={
                "Authorization": f"Bearer {CF_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error in edit_image: {e}")
        return None