import pickle
import tensorflow as tf

class Transformer:
    def transform(self, X):
        pass
    def save(self, output_dir):
        pass

class Model:
    def predict(self, X):
        pass
    def save(self, output_dir):
        pass

def get_trained_tokenizer(texts):
        tokenizer = tf.keras.preprocessing.text.Tokenizer(
            num_words=80000,
            filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r',
            lower=True,
            split=' ',
            char_level=False,
            oov_token='<UNK>'
        )
        tokenizer.fit_on_texts(texts)
        return tokenizer

tokenizer = get_trained_tokenizer(texts)
tokenizer.save('')

tokenizer.

class TextTransformer(Transformer):
    def __init__(self):
        self.tokenizer = get_trained_tokenizer(texts)
    def transform(self, input_data):
        features = self.text_preprocessor(input_data)
        return features        
    def save(self, output_dir):
        with open(f'{output_dir}/tokenizer.pickle', 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def text_preprocessor(self, raw_data):
        # Encode training data sentenses into sequences
        train_sequences = self.tokenizer.texts_to_sequences(raw_data)
        embeded_data = tf.keras.preprocessing.sequence.pad_sequences(train_sequences, 
            padding='post', truncating='post', maxlen=255)
        return embeded_data


def get_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(80000, 16))
    model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model = get_model()
model.save(f'{output_dir}/keras-model-w2v.h5')
model = keras.model.load_model(f'{output_dir}/keras-model-w2v.h5')



class RedditClassifier(Model):
    def __init__(self, transformer, model):
        self.transformer = transformer
        self.model = model        

    def predict(self, X):
        features = self.transformer.transform(X)
        predictions = self.model.predict(features)
        return predictions    
