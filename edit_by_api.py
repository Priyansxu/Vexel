import os
import openai

"""
load environment variables from .env file
"""
from dotenv import load_dotenv
load_dotenv()

"""
access openai api environment variable
"""
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_edit(text, edit_image):
    try:
        response = openai.Image.create_edit(
            image=open(f"{edit_image}", "rb"),
            # mask=open("mask.png", "rb"),
            prompt=f"{text}",
            n=1,
            size="1024x1024"
        )

    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

    return response['data'][0]['url']

