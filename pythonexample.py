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
