#http://127.0.0.1:5000/text?input=%22monkey%22
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from web import query_example
import sys


url = "https://ai.serverboi.org"

text = sys.argv[1]
option_payload = {
    "prompt": text,
    "steps": 50,
    "sd_model_checkpoint": "analog-diffusion-1.0.ckpt [9ca13f02]",
    "CLIP_stop_at_last_layers": 2
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=option_payload)

r = response.json()



for i in r['images']:

    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('static/output.png', pnginfo=pnginfo)
# Set the base64 data as the "image" parameter in the POST request
data = {
    "image": i
}

    # Send the POST request to the Flask application
response = requests.post(url='http://localhost:5000/image', data=data)