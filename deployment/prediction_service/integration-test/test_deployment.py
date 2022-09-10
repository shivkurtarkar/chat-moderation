import requests
import uuid

host='http://localhost'
# host='http://172.18.0.2'
port=8000
message_id = str(uuid.uuid4())
message_body =[ 'fuck you bitch', 'hi there, how are you?']
message =  { 
    'Records': [{
            'body': message_body[0],
            'message_id': message_id
        },{
            'body': message_body[1],
            'message_id': message_id
        }
    ]
}

url = f'{host}:{port}/predict'
print(f'URL: {url}')
response = requests.post(url, json=message)
print(response.json())