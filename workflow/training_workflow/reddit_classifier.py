
class RedditClassifier:
    def __init__(self, transformer, model):
        self.transformer = transformer
        self.model = model        

    def predict(self, X):
        features = self.transformer.transform(X)
        predictions = self.model.predict(features)
        return predictions    
