from reddit_dataset import RedditDataset

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import argparse
import os
import pickle

import mlflow
from mlflow.tracking import MlflowClient

def get_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(80000, 16))
    model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# def save_model(model, output_path):
#     # MODEL_SAVE_DIR='../../models/tf_nsfw_text_classifer'
#     # f'{MODEL_SAVE_DIR}/models/keras-model-w2v.h5')
#     model.save(output_path) 
    
# def load_model(model_path):
#     return keras.load_model(model_path)
  
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

def load_pickle(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)

def run(data_path, dataset, experiment='new_experiment'):
    mlflow.set_experiment(experiment)
    mlflow.tensorflow.autolog()

    # tokenizer = load_pickle(os.path.join(data_path, 'tokenizer.pkl'))
    tokenizer_path =os.path.join(data_path, 'tokenizer.pkl')
    X_train, y_train = load_pickle(os.path.join(data_path, 'train.pkl'))
    X_test, y_test = load_pickle(os.path.join(data_path, 'test.pkl'))
        
    # Training
    with mlflow.start_run():
        model = get_model()
        mlflow.log_param('dataset', dataset)
        mlflow.log_artifact(tokenizer_path, 'preprocess/tokenizer')
        print(model.summary())
        model.fit(
            X_train, y_train,
            epochs=20,
            batch_size=10000,
            verbose=1,
            validation_data=(X_test, y_test),
            callbacks=[]
        )


if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_path',
        default='./output'
    )
    parser.add_argument(
        '--dataset',
        default='reddit'
    )

    args = parser.parse_args()

    MLFLOW_TRACKING_URI = 'http://172.18.0.2:31989'
    # MLFLOW_TRACKING_URI ='http://0.0.0.0:5000'
    EXPERIMENT = 'text-moderation-model'
    run(args.data_path, args.dataset, EXPERIMENT)
    
    # print('evaluating ... ')
    # scores = model_evalute(model, X_test_embedding, y_test)
    # print(scores)

    # save_model(model, output_path) 
    ## inference
    # model = load_model()
    # tokenizer = load_tokenizer()

    # reddit_classifier = RedditClassifier(transformer, model)
    # data = [['f*ck off bitch']]
    # prediction = reddit_classifier.predict(data)
    # print(prediction)