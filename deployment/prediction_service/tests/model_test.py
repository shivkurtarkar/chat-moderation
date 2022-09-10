import os
import model

class ModelMock:
    def __init__(self, value):
        self.value = value
    def predict(self, X):
        n = len(X)
        return [self.value]*n

def test_predict():
    pass
def test_labmda_handler():
    pass