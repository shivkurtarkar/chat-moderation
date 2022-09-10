"""
Model prediction
"""
import os
import pickle

import mlflow

from transformers import TokenizerTransformer, PreprocessingTransformer
from reddit_classifier import RedditClassifier

# from mlflow.tracking import MlflowClient
# from mlflow.entities import ViewType


def get_model_location(run_id, experiment_id):
    """Gets model file location"""
    model_location = os.getenv('MODEL_LOCATION', None)
    print(f'model_location : {model_location}')
    if model_location is not None:
        return f'{model_location}/{run_id}/artifacts'
    model_bucket = os.getenv('MODEL_BUCKET', 'mlflow')
    model_location = f's3://{model_bucket}/{experiment_id}/{run_id}/artifacts'
    return model_location


def load_pickle(filename):
    """Load pickle file"""
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


MODEL_ARTIFACT_PATH = 'model'
TOKENIZER_ARTIFACT_PATH = 'preprocess/tokenizer/tokenizer.pkl'


def load_model(run_id, experiment_id):
    """Load model"""

    print("env---")
    print(f"model_path              : {MODEL_ARTIFACT_PATH}")
    print(f"tokenizer_path          : {TOKENIZER_ARTIFACT_PATH}")
    print(f"RUN_ID		            : {run_id} ")
    print(f"EXPERIMENT_ID	        : {experiment_id} ")
    print()
    print(f"MLFLOW_TRACKING_URI		: {os.getenv('MLFLOW_TRACKING_URI')} ")
    print(f"MLFLOW_S3_ENDPOINT_URL	: {os.getenv('MLFLOW_S3_ENDPOINT_URL')} ")
    print(f"AWS_ACCESS_KEY_ID		: {os.getenv('AWS_ACCESS_KEY_ID')} ")
    print(f"AWS_SECRET_ACCESS_KEY	: {os.getenv('AWS_SECRET_ACCESS_KEY')} ")
    print(f"MLFLOW_S3_IGNORE_TLS	: {os.getenv('MLFLOW_S3_IGNORE_TLS')} ")
    print()

    print("downloading artifacts..")
    model_dir_path = get_model_location(run_id, experiment_id)

    logged_model = f'{model_dir_path}/{MODEL_ARTIFACT_PATH}'
    print(f'logged_model: {logged_model}')
    logged_tokenizer = f'{model_dir_path}/{TOKENIZER_ARTIFACT_PATH}'
    print(f'logged_tokenizer: {logged_tokenizer}')
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    tokenizer_path = mlflow.artifacts.download_artifacts(logged_tokenizer)
    loaded_tokenizer = load_pickle(tokenizer_path)
    print("successfully downloaded artifacts")
    transformer = TokenizerTransformer(
        loaded_tokenizer, next_transformer=PreprocessingTransformer()
    )
    reddit_classifier = RedditClassifier(transformer, loaded_model)
    return reddit_classifier


class ModelService:
    """Model Service wrapper"""

    def __init__(self, model, model_version=None, callbacks=None):
        """Model service init"""
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, message):
        """Prepare feature function"""
        features = [message]
        return features

    def predict(self, features):
        """Model prediction function"""
        preds = self.model.predict(features)
        preds = preds.tolist()
        return float(preds[0][0])

    def handler(self, events):
        """Prediction Service hanler"""
        prediction_events = []
        for record in events['Records']:
            message_body = record['body']
            message_id = record['message_id']
            features = self.prepare_features(message_body)
            pred = self.predict(features)
            prediction_event = {
                'model': 'chat-moderation-model',
                'version': self.model_version,
                'prediction': {
                    'moderate_message': pred,
                    'message_id': message_id,
                },
            }
            for callback in self.callbacks:
                callback(prediction_event)
            prediction_events.append(prediction_event)
        return {'predictions': prediction_events}


def init(experiment_id: int, run_id: str, test_run: bool):
    """Prediction service init"""
    model = load_model(run_id, experiment_id)
    callbacks = []
    if not test_run:
        pass
        # save message in db
        # trigger monitoring service
    model_service = ModelService(
        model=model, model_version=run_id, callbacks=callbacks
    )
    return model_service
