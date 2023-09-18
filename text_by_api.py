import os
import openai

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# access openai api environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# default system message
system_message = "You are a helpful assistant. You love to help people."

"""
prompt is text input received by user
completion is request to send to openai api
"""
def get_response(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{system_message}"},
                {"role": "user", "content": f"{prompt}"}
            ],
            temperature = 0.8,
        )
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

    return completion.choices[0].message
