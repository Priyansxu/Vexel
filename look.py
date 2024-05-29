import base64
import anthropic
import aiohttp
import imghdr

anthropic_client = anthropic.Anthropic()

async def recognize_image(image_data, prompt):
    try:
        if isinstance(image_data, str): 
            async with aiohttp.ClientSession() as session:
                async with session.get(image_data) as response:
                    if response.status == 200:
                        image_data = await response.read()

        image_format = imghdr.what(None, image_data)

        if image_format is None:
            return "Failed to determine image format"

        image_data_base64 = base64.b64encode(image_data).decode("utf-8")

        description = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": f"image/{image_format}",
                                "data": image_data_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        if description and description.content:
            return description.content[0].text
        else:
            return None

    except Exception as e:
        return None 