import requests

# host='http://localhost'
host='http://172.18.0.2'
port=31424

message = {
    'body': 'fuck you bitch'
}

url = f'{host}:{port}/predict'
print(f'URL: {url}')
response = requests.post(url, json=message)
print(response.json())