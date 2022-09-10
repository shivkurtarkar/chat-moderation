import os
from flask import Flask, request, jsonify
import model

RUN_ID=os.getenv('RUN_ID')

EXPERIMENT_ID = os.getenv('MLFLOW_EXPERIMENT_ID', '1')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

model_service = model.init(
    experiment_id=EXPERIMENT_ID,
    run_id=RUN_ID,
    test_run=TEST_RUN,
)

app = Flask('message-moderation')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    event = request.get_json()        
    result = model_service.handler(event)
    return jsonify(result)

if __name__ == '__main__':
    print("starting application")
    app.run(debug=True, host='0.0.0.0', port=9696)