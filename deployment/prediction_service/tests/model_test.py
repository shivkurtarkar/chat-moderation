import numpy as np

import model


class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return np.array([([self.value] * n)])


def test_feature():
    input_text = 'This is a test message'
    expected_feature = [input_text]
    model_service = model.ModelService(None)
    actual_feature = model_service.prepare_features(input_text)
    assert actual_feature == expected_feature


def test_predict():
    feature = ['This is a test message']
    expected_prediction = 0.9
    model_mock = ModelMock(expected_prediction)
    model_service = model.ModelService(model_mock)
    actual_prediction = model_service.predict(feature)
    assert actual_prediction == expected_prediction


def test_labmda_handler():
    pred = 0.9
    model_version = 'test123'
    model_mock = ModelMock(pred)
    model_service = model.ModelService(model_mock, model_version)
    message_id = 'test_id_123'
    message_body = 'hi there, how are you?'
    message = {'Records': [{'body': message_body, 'message_id': message_id}]}
    expected_prediction = {
        'predictions': [
            {
                'model': 'chat-moderation-model',
                'version': model_version,
                'prediction': {
                    'moderate_message': pred,
                    'message_id': 'test_id_123',
                },
            }
        ]
    }
    actual_response = model_service.handler(message)
    assert actual_response == expected_prediction
