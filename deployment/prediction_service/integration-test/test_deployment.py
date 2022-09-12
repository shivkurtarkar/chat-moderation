import uuid

import requests
from deepdiff import DeepDiff

host = 'http://localhost'
# host='http://172.18.0.2'
port = 8000
message_id = str(uuid.uuid4())
message_body = 'hi there, how are you?'
message = {'Records': [{'body': message_body, 'message_id': message_id}]}
url = f'{host}:{port}/predict'
# print(f'URL: {url}')
response = requests.post(url, json=message, timeout=5)
actual_response = response.json()
# print(actual_response)
pred = 0.4
model_version = '3cfafa786d1643719efc78e9f7251402'
expected_response = {
    'predictions': [
        {
            'model': 'chat-moderation-model',
            'version': model_version,
            'prediction': {'moderate_message': pred, 'message_id': message_id},
        }
    ]
}

diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print('diff---------')
print(diff)
assert 'type_changes' not in diff
assert 'values_changed' not in diff
