from flask import Flask, request, render_template, jsonify
import subprocess
import base64
import io
from PIL import Image
import os
from flask import send_from_directory

app = Flask(__name__,)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/image', methods=['POST'])
def process_image():
    # Get the base64 data from the "image" parameter
    image_data = request.form['image']

    # Decode the base64 data and open it as an image
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

@app.route('/')
def index():
    # Open the image file and read it into memory
    with open('static/output.png', 'rb') as f:
        image_data = f.read()
    # Encode the image data as a base64 string
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # Render the index.html template and pass the image data as a parameter
    with open('prompt.txt', 'r') as f:
        lines = []
        for line in f:
            lines.append(line)
        return render_template('index.html', image=image_base64, prompt=line)

@app.route('/text')
def query_example():
    # if key doesn't exist, returns None
    text = request.args.get('input')
    f = open('prompt.txt', 'w')
    f.write(text)
    f.close()
    subprocess.run(["python", "sd.py", text])
    # Open the image file and read it into memory
    with open('static/output.png', 'rb') as f:
        image_data = f.read()
    # Encode the image data as a base64 string
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # Render the index.html template and pass the image data as a parameter
    image=image_base64
    return jsonify({'image-base64': image })



if __name__ == '__main__':
  app.run()