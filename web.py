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

    # Read the lines from the file 'prompt.txt' and join them into a single string
    with open('prompt.txt', 'r') as f:
        prompt = ''.join(f.readlines())

    # Render the index.html template and pass the image data and prompt string as parameters
    return render_template('index.html', image=image_base64, prompt=prompt)

@app.route('/text')
def query_example():
    # Set a default value for the 'image_base64' variable
    image_base64 = ''
    # Get the value of the 'input' query parameter
    text = request.args.get('input')
    if text:
        # Write the value of 'input' to the file 'prompt.txt'
        with open('prompt.txt', 'w') as f:
            f.write(text)
        # Run the sd.py script with the value of 'input' as an argument
        subprocess.run(["python", "sd.py", text])
        # Open the image file and read it into memory
        with open('static/output.png', 'rb') as f:
            image_data = f.read()
        # Encode the image data as a base64 string
        image_base64 = base64.b64encode(image_data).decode('utf-8')
    else:
        # Handle the case where the 'input' query parameter is not provided
        # (e.g. return an error message, set a default value, etc.)
        pass


    # Render the index.html template and pass the image data as a parameter
    image=image_base64
    return jsonify({'image-base64': image })



if __name__ == '__main__':
  app.run()
