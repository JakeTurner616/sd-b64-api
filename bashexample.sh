#!/bin/bash
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
