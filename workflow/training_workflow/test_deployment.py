import requests

message = {
    'body': 'fuck you bitch'
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=message)
print(response.json())