# sd-b64-api (stable-diffusion-base64-api)

Flask API written to send back a json response containing txt2img base64 output through URL query

Setup dependencies:

pip3 install -r requirements.txt

Run web.py for a development environment for testing. Don't use the development server for production!

python .\web.py

Send url query:

http://127.0.0.1:5000/text?input=%22monkey%20with%20a%20hat%22

Response is sent as json 'b64-image' containing the base64 encoded data. Heres an example of a python program to accept this data and decode it into an image:

```python
import base64
import requests

# Set the URL for the API endpoint
url = "http://127.0.0.1:5000/text?input=%22monkey%20with%20a%20hat%22"

# Send the request to the API and store the response
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the JSON data from the response
    data = response.json()

    # Decode the data using base64
    decoded_data = base64.b64decode(data['image-base64'])

    # Save the decoded data to a file with a .png extension
    with open("output.png", "wb") as f:
        f.write(decoded_data)
else:
    print("Request failed with status code:", response.status_code)
```

The point of this is to allow requests to be sent from many different langugages. Here is the above example but written as a bash script instead:

```bash
# Set the URL for the API endpoint
url="http://127.0.0.1:5000/text?input=%22monkey%20with%20a%20hat%22"

# Send the request to the API and store the response in a variable
response=$(curl -s "$url")

# Check if the request was successful
if [[ $response =~ ^\{.*\}$ ]]; then
    # Extract the image-base64 field from the response
    data=$(echo "$response" | grep -o '"image-base64":[^,]*' | cut -d ':' -f 2- | tr -d '"')

    # Decode the data using base64
    decoded_data=$(echo "$data" | base64 -d)

    # Write the decoded data to a file
    echo "$decoded_data" > output.png
else
    # Print the response if the request was unsuccessful
    echo "$response"
fi

```

Both example programs will output the image file 'output.png' if the request to the Flask API is received:

![program outputs the image](/static/output.png "decoded base64 image from url query")
