from newsapi import NewsApiClient
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from instagrapi import Client
from instagrapi.types import Usertag,Location
import textwrap
import pandas as pd
import json
import requests


newsapi = NewsApiClient(api_key='Add your api key')
url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=$api_key"

response = requests.get(url)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the JSON data from the response
    data = response.json()

    # Process the data as needed
    print(data)
else:
    # Print an error message if the request was not successful
    print("Error:", response.status_code)

df = pd.json_normalize(data['articles'])
df

url = data["articles"][2]['urlToImage']

# Send a GET request to retrieve the image
response = requests.get(url)

image = Image.open(BytesIO(response.content))

new_width = 600
new_height = 900

# Resize the image
resized_image = image.resize((new_width, new_height))
d = ImageDraw.Draw(resized_image)
font = ImageFont.truetype("Roboto-Bold.ttf", 36)

# Set the text
text = data["articles"][2]['title'] 

# Set the text color
text_color = (0, 255, 255)  # White

# Set the maximum width for each line
max_width = 20

# Wrap the text into multiple lines
wrapped_text = textwrap.wrap(text, width=max_width)

# Calculate the total height required for the text
total_height = sum(font.getsize(line)[1] for line in wrapped_text)

# Calculate the starting position to center the text vertically
position_y = (resized_image.height - total_height) // 2

# Draw each line of text onto the image
for line in wrapped_text:
    line_width, line_height = font.getsize(line)
    position_x = (resized_image.width - line_width) // 2
    d.text((position_x, position_y), line, font=font, fill=text_color)
    position_y += line_height

resized_image.save("todaynews.jpg")

cl = Client()
cl.login("gettopnews","Add Your Password")

media = cl.photo_upload(caption=data["articles"][2]['description'], path = "todaynews.jpg")