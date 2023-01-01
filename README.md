# sd-b64-api (stable-diffusion-base64-api)

Flask API written to send back a json response containing txt2img base64 output through URL query using [ai.serverboi.org](https://ai.serverboi.org) and AUTOMATIC111's [stable-diffusion-webUI text2img API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API).

Setup dependencies:

```
pip3 install -r requirements.txt
```

Run web.py for a development environment for testing. Don't use the development server for production! See [Deploying](#deploying).

```
python .\web.py
```

Send url query:

```
http://127.0.0.1:5000/text?input=%22monkey%20with%20a%20hat%22
```

Response is sent as json titled: `image-b64` containing the base64 encoded data. Heres an example of a simple python program to accept this data and decode it into an image:

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

`prompt.txt` will be written as the user input from the url query on the flask backend:
```
"monkey with a hat"
```
## Deploying

This can be easily deployed with docker and gunicorn by running the following build command in the source directory to build an image:

```
docker build -t sd-b64-api .
```

Then run the built image:

```
docker run -p 5000:5000 -it sd-b64-api
```
## Load balancing / scaling

Since one instance can take multiple seconds for each request, we can do a hack to assign clients to containers sequentially (one after the other).

To start the the Flask app with load balancing, run the following command in the source directory:

```
docker-compose up
```
You can scale the number of Flask app instances by using docker-compose. For example, to start 3 instances of the app, you can run the following command:

```
docker-compose up --scale app=3
```

This will start 3 instances of the "app" service, which will be automatically registered. When the load balancer receives an incoming request, it selects an available instance of the service to handle the request based on the round-robin algorithm. This means that the load balancer will select the first available instance for the first request, the second available instance for the second request, and so on.
It creates a container for each of the defined services: "app" and "nginx". The "app" service starts multiple instances of the Flask app, and the "nginx" service starts a simple NGINX load balancer.
