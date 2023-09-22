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

"""
prompt is text input received by user
completion is request to send to openai api
"""
def get_response(prompt):
    
    if "prompt" in prompt.lower(): # system message for prompts
        system_message = "You provide prompts for an image generation ai. When a message starts with 'prompt', generate a creative and specific prompt for creating an image in 40 words or less. \
                    example1 - user: prompt draw Daenerys Targaryen. \
                    Your response: photorealistic 4K rendering of Daenerys Targaryen from Game of Thrones. Include intricate hair braids, flowing dragon-themed clothing, and vibrant fire effects to capture her iconic look. \
                    example2 - user: prompt draw a 4090 GPU. \
                    Your response: anime, unrealistic rendering of a futuristic 4090 GPU. intricate circuitry, cooling fans, and sleek metallic surfaces to capture its cutting-edge technology. \
                    example3 - user: prompt draw Hermaeus Mora trying to pick up a cup of coffee with his tentacles but spilling it on the books in Apocrypha. \
                    Your response: lifelike rendering of Hermaeus Mora, the Daedric Prince of Knowledge, attempting to grasp a cup of coffee with his tentacles, only to spill it on the ancient books in Apocrypha. chaos and intricacy, lots of details, volumetric lighting."

    else:
        system_message = "You are a helpful assistant. You love to help people." # default system message

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{system_message}"},
                {"role": "user", "content": f"{prompt}"}
            ],
            temperature = 1.0, # how deterministic is the response, 0.0 to 2.0 (high to low)
        )
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

    return completion.choices[0].message
