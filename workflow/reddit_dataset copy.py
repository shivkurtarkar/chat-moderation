import pandas as pd

def get_dataset(name, columns):
    DATASET_DIR='../../data/reddit'    
    
    df_cols = ["prev_idx", "body", "score", "parent_id", "id", "created_date", "retrieved_date", "removed"]

    dataset_filename = f'{DATASET_DIR}/{name}'
    dataset = pd.read_csv(
        dataset_filename,
        names=df_cols,
        skiprows=1,
        encoding='ISO-8859-1'
    )
    x = dataset[columns]
    y = dataset['removed']
    return x, y


import tensorflow as tf

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
    
def text_preprocessor(tokenizer, raw_data):
    # Encode training data sentenses into sequences
    train_sequences = tokenizer.texts_to_sequences(raw_data)
    embeded_data = tf.keras.preprocessing.sequence.pad_sequences(train_sequences, 
        padding='post', truncating='post', maxlen=255)
    return embeded_data

if __name__ == '__main__':
    train_dataset = 'reddit_200k_train.csv'
    test_dataset = 'reddit_200k_test.csv'
    TEXT_COLUMN = "body"

    columns = [ "body", "score", "created_date"]
    X_train, y_train = get_dataset(train_dataset, columns)
    print(X_train)
    X_test, y_test = get_dataset(test_dataset, columns)
    print(X_test)

    tokenizer = get_trained_tokenizer(X_train[TEXT_COLUMN])
    
    X_train_embedding = text_preprocessor(tokenizer, X_train[TEXT_COLUMN])
    X_test_embedding = text_preprocessor(tokenizer, X_test[TEXT_COLUMN])

    print(X_test_embedding)
