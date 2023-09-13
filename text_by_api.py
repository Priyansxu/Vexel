import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# default system message
system_message = "You are a helpful assistant."

# prompt is text input received by user
prompt = ""
# code to receive text from bot_controller.py
# prompt = //input from bot_controller.py

# completion is request to send to openai api
def get_response(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{system_message}"},
            {"role": "user", "content": f"{prompt}"}
        ],
        temperature = 1.0,
    )
    return completion.choices[0].message
