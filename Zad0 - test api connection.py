# Author: Joanna Koła
# Date: 2024-11-04
# Version: 1.0
# Description: This script tests ability to connect with API provided by course creator


import requests

# URL to fetch data from
data_url = "https://poligon.aidevs.pl/dane.txt"

# URL to send data to
verify_url = "https://poligon.aidevs.pl/verify"

# Fetch data from the URL
response = requests.get(data_url, verify=False)
data = response.text

# Convert data to a list of strings
data_list = data.splitlines()

# Send data to the verify endpoint
response = requests.post(verify_url, json={
    "task": "POLIGON",
    "apikey": "7eabd929-6873-4a9d-8315-d25502254148",
    "answer": data_list
}, verify=False)

# Print the response from the server
print(response.text)