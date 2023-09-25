import os
import openai
import aiohttp
from PIL import Image
import random
import math

"""
load environment variables from .env file
"""
from dotenv import load_dotenv
load_dotenv()

"""
access openai api environment variable
"""
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_edit(edit_image, edit_mask, text=" "):
    try:
        response = openai.Image.create_edit(
            image=open(f"{edit_image}", "rb"),
            mask=open(f"{edit_mask}", "rb"),
            prompt=f"{text}",
            n=1,
            size="1024x1024"
        )

    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)

    return response['data'][0]['url']

"""
helper functions to convert images to RGBA, transparent, and <= 4MB for openai api editing
"""
def convert_image_to_rgba(filename):
    img = Image.open(filename)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img.save("img_rgba.png")
    img.close()

"""
creates one transparent circle in the center of image
"""
def make_image_transparent(filename, circle_radius=300):
    img = Image.open(filename)
    datas = img.getdata()
    width, height = img.size
    new_data = []
    
    # find the center of the image
    cx, cy = width // 2, height // 2
    
    for y in range(height):
        for x in range(width):
            data = datas[y * width + x]
            
            # check if (x, y) is inside the circle
            inside_circle = math.sqrt((x - cx)**2 + (y - cy)**2) <= circle_radius
            
            if inside_circle:
                new_data.append((data[0], data[1], data[2], 0)) 
            else:
                new_data.append(data)

    img.putdata(new_data)
    img.save("img_transparent.png")
    img.close()

'''
"""
creates transparent circles randomly over image
"""
def make_image_transparent(filename, num_circles=3, min_radius=300, max_radius=300):
    img = Image.open(filename)
    datas = img.getdata()
    width, height = img.size
    new_data = []
    
    # generate random circles
    circles = [(random.randint(0, width), random.randint(0, height), random.randint(min_radius, max_radius)) for _ in range(num_circles)]

    for y in range(height):
        for x in range(width):
            data = datas[y * width + x]
            
            # check if (x, y) is inside any of the circles
            inside_circle = False
            for cx, cy, r in circles:
                if math.sqrt((x - cx)**2 + (y - cy)**2) <= r:
                    inside_circle = True
                    break
            
            if inside_circle:
                new_data.append((data[0], data[1], data[2], 0))
            else:
                new_data.append(data)
                
    img.putdata(new_data)
    img.save("img_transparent.png")
    img.close()
'''

'''
"""
creates transparent squares in the corners of the image based on corner_size
"""
def make_image_transparent(filename, corner_size=450):
    img = Image.open(filename)
    img = img.convert('RGBA')
    datas = img.getdata()
    width, height = img.size
    new_data = []
    for y in range(height):
        for x in range(width):
            data = datas[y * width + x]
            if (x < corner_size and y < corner_size) or (x < corner_size and y >= height - corner_size) or (x >= width - corner_size and y < corner_size) or (x >= width - corner_size and y >= height - corner_size):
                new_data.append((data[0], data[1], data[2], 0))
            else:
                new_data.append(data)
    img.putdata(new_data)
    img.save("img_transparent.png")
    img.close()
'''
    
'''
"""
creates transparent circles in range 200-256
"""
def make_image_transparent(filename):
    with Image.open(filename) as img:
        data = img.getdata()
        new_data = []
        for item in data:
            if item[0] in list (range(200, 256)):
                new_data.append((item[0], item[1], item[2], 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        img.save(filename)
'''

def resize_image(filename, base_width=1024):
    img = Image.open(filename)
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), Image.LANCZOS)
    img.save("img_resized.png")
    img.close()

def check_and_resize_image(filename):
    max_size = 4 * 1024 * 1024  # 4MB
    resize_image(filename)  # First resize the image
    file_size = os.path.getsize("img_resized.png")  # check the file size

    # if still over the limit, resize again or use more aggressive settings
    while file_size > max_size:
        resize_image("img_resized.png")  # resize again
        file_size = os.path.getsize("img_resized.png")  # check file size again

    img = Image.open("img_resized.png")
    img.save("img_resized.png")
    img.close()

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                image_data = await resp.read()
                return image_data
            else:
                print(f"Failed to download image: status code {resp.status}")
                return None