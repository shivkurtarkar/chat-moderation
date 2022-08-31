import tensorflow as tf

class Transformer:
    def __init__(self, next_transformer=None):
        self._next_transformer = next_transformer
    def transform(self, data):
        features = self.do_transform(data)
        if self._next_transformer:
            features = self._next_transformer.transform(features)
        return features
    def do_transform(self, data):
        pass

class TokenizerTransformer(Transformer):
    def __init__(self, tokenizer, next_transformer=None):
        super(TokenizerTransformer, self).__init__(next_transformer)
        self.tokenizer = tokenizer
    def do_transform(self, data):
        features = self.tokenizer.texts_to_sequences(data)        
        return features

class PreprocessingTransformer(Transformer):
    def __init__(self, next_transformer=None):
        super(PreprocessingTransformer, self).__init__(next_transformer)
    def do_transform(self, data):
        embeded_data = tf.keras.preprocessing.sequence.pad_sequences(
            data, 
            padding='post', truncating='post', maxlen=255
        )
        return embeded_data
