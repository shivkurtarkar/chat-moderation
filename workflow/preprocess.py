from reddit_dataset import RedditDataset
from transformers import TokenizerTransformer, PreprocessingTransformer

import tensorflow as tf
import numpy as np
import argparse
import os
import pickle

def dump_pickle(obj, filename):
    with open(filename, 'wb') as f_out:
        return pickle.dump(obj, f_out)


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

def run(raw_data_path: str, dest_path: str, dataset:str = 'reddit'):

    train_dataset = RedditDataset(
        os.path.join(raw_data_path, f'{dataset}_train.csv')
    )
    X_train = train_dataset.get_data()
    y_train = train_dataset.get_labels()
    test_dataset = RedditDataset(
        os.path.join(raw_data_path, f'{dataset}_test.csv')
    )        
    X_test = test_dataset.get_data()
    y_test = test_dataset.get_labels()
    
    # train tokenizer
    # tokenizer = tf.keras.preprocessing.text.Tokenizer(
    #     num_words=80000,
    #     filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r',
    #     lower=True,
    #     split=' ',
    #     char_level=False,
    #     oov_token='<UNK>'
    # )
    # texts = X_train.to_list()
    # tokenizer.fit_on_texts(texts)        
    tokenizer = get_trained_tokenizer(X_train)


    transformer = TokenizerTransformer(
        tokenizer, 
        next_transformer=PreprocessingTransformer()
    )
    # preprocessing
    X_train_embedding = transformer.transform(X_train)
    X_test_embedding = transformer.transform(X_test)
    
    dump_pickle(tokenizer, os.path.join(dest_path, 'tokenizer.pkl'))
    dump_pickle((X_train_embedding, y_train), os.path.join(dest_path, 'train.pkl'))
    dump_pickle((X_test_embedding, y_test), os.path.join(dest_path, 'test.pkl'))
    

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--raw_data_path',
        help='the location where the raw data is saved'
    )
    parser.add_argument(
        '--dest_path',
        help='the location where the resulting files will be saved.'
    )
    parser.add_argument(
        '--dataset',
        help='reddit or reddit_200k',
        default='reddit'
    )
    args = parser.parse_args()
    run(args.raw_data_path, args.dest_path, args.dataset)