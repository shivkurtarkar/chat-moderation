from reddit_dataset import RedditDataset

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def get_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(80000, 16))
    model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

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


class RedditClassifier:
    def __init__(self, transformer, model):
        self.transformer = transformer
        self.model = model        

    def predict(self, X):
        features = self.transformer.transform(X)
        predictions = self.model.predict(features)
        return predictions    

    
# def text_preprocessor(tokenizer, raw_data):
#     # Encode training data sentenses into sequences
#     train_sequences = tokenizer.texts_to_sequences(raw_data)
#     embeded_data = tf.keras.preprocessing.sequence.pad_sequences(train_sequences, 
#         padding='post', truncating='post', maxlen=255)
#     return embeded_data

def model_evalute(model, data, labels):
    loss, accuracy = model.evaluate(data, labels)
    
    # print(f"Training accuracy: {accuracy:.4f}, loss: {loss}")
    # loss, accuracy = model.evaluate(X_test_embedding, y_test)
    # print(f"Training accuracy: {accuracy:.4f}, loss: {loss}")

    probabilities = model.predict(data)
    pred = probabilities > 0.5
    print(classification_report(labels, pred))
    confusion_matrix(labels, pred)

    fpr, tpr, _ = roc_curve(labels, probabilities)
    plt.plot(fpr, tpr)
    plt.plot([0,1],[0,1], 'k--')
    auc = roc_auc_score(labels, pred)
    print(f"accuracy: {accuracy:.4f}, loss: {loss}")
    print("AUC: ", auc)
    return {
        'accuracy': accuracy,
        'loss': loss,
        'fpr': fpr,
        'tpr': tpr,
        'auc': auc,
    }

if __name__ == '__main__':    
    train_dataset = 'reddit_200k_train.csv'
    test_dataset = 'reddit_200k_test.csv'
    DATASET_DIR='../../data/reddit'    

    train_dataset = RedditDataset(DATASET_DIR, train_dataset)
    X_train = train_dataset.get_data()
    y_train = train_dataset.get_labels()
    print(len(X_train))
    test_dataset = RedditDataset(DATASET_DIR, test_dataset)
    X_test = test_dataset.get_data()
    y_test = test_dataset.get_labels()
    print(len(X_test))

    tokenizer = get_trained_tokenizer(X_train)    
    transformer = TokenizerTransformer(tokenizer, 
        next_transformer=PreprocessingTransformer()
    )

    X_train_embedding = transformer.transform(X_train)
    X_test_embedding = transformer.transform(X_test)
    
    # Training
    model = get_model()
    print(model.summary())
    history = model.fit(
        X_train_embedding, y_train,
        epochs=2,
        batch_size=10000,
        verbose=1,
        validation_data=(X_test_embedding, y_test),
        callbacks=[]
    )
    
    # MODEL_SAVE_DIR='../../models/tf_nsfw_text_classifer'

    # # serialize model to JSON
    # def save_model(tokenizer, model, MODEL_SAVE_DIR):
    #     model_json = model.to_json()
    #     with open(f'{MODEL_SAVE_DIR}/keras-model-w2v.json', 'w') as json_file:
    #         json_file.write(model_json)        
    #     # serialize weight to HDF5
    #     model.save(f'{MODEL_SAVE_DIR}/models/keras-model-w2v.h5')
    #     print('saved model to disk')

    #     # In[27]:
    #     import pickle
    #     with open(f'{MODEL_SAVE_DIR}/tokenizer.pickle', 'wb') as handle:
    #         pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print('evaluating ... ')
    scores = model_evalute(model, X_test_embedding, y_test)
    print(scores)

    ## inference
    reddit_classifier = RedditClassifier(transformer, model)
    data = [['f*ck off bitch']]
    prediction = reddit_classifier.predict(data)
    print(prediction)