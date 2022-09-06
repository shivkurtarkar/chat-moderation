from flask import Flask, request, jsonify
from reddit_classifier import RedditClassifier
from transformers import TokenizerTransformer, PreprocessingTransformer
import pickle
import os

import mlflow
# from mlflow.tracking import MlflowClient
# from mlflow.entities import ViewType


def load_pickle(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)

RUN_ID=os.getenv('RUN_ID')
EXPERIMENT=os.getenv('EXPERIMENT')

MODEL_ARTIFACT_PATH='model'
TOKENIZER_ARTIFACT_PATH='preprocess/tokenizer/tokenizer.pkl'

print("env---")
print(f"model_path              : {MODEL_ARTIFACT_PATH}")
print(f"tokenizer_path          : {TOKENIZER_ARTIFACT_PATH}")
print(f"RUN_ID		            : {RUN_ID} ")
print(f"EXPERIMENT	            : {EXPERIMENT} ")
print()
print(f"MLFLOW_TRACKING_URI		: {os.getenv('MLFLOW_TRACKING_URI')} ")
print(f"MLFLOW_S3_ENDPOINT_URL	: {os.getenv('MLFLOW_S3_ENDPOINT_URL')} ")
print(f"AWS_ACCESS_KEY_ID		: {os.getenv('AWS_ACCESS_KEY_ID')} ")
print(f"AWS_SECRET_ACCESS_KEY	: {os.getenv('AWS_SECRET_ACCESS_KEY')} ")
print(f"MLFLOW_S3_IGNORE_TLS	: {os.getenv('MLFLOW_S3_IGNORE_TLS')} ")
print()
print(f"FLASK_APP	            : {os.getenv('FLASK_APP')} ")

# PREFIX='mlflow-artifacts:/1'
PREFIX='runs:'

print("downloading artifacts..")
# Load model as a PyFuncModel.
logged_model = f'{PREFIX}/{RUN_ID}/{MODEL_ARTIFACT_PATH}'
print(f'logged_model: {logged_model}')
loaded_model = mlflow.pyfunc.load_model(logged_model)

logged_tokenizer = f'{PREFIX}/{RUN_ID}/{TOKENIZER_ARTIFACT_PATH}'
print(f'logged_tokenizer: {logged_tokenizer}')
tokenizer_path = mlflow.artifacts.download_artifacts(logged_tokenizer)
loaded_tokenizer = load_pickle(tokenizer_path)

print("successfully downloaded artifacts")

transformer = TokenizerTransformer(
    loaded_tokenizer, 
    next_transformer=PreprocessingTransformer()
)
reddit_classifier = RedditClassifier(transformer, loaded_model)


app = Flask('message-moderation')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    message = request.get_json()
    
    body = message['body']
    
    pred = reddit_classifier.predict([body])
    pred = pred.tolist()[0]
    result = {
        'score': pred,
        'model_version': RUN_ID
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    print("starting application")
    app.run(debug=True, host='0.0.0.0', port=9696)