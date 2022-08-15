#!/usr/bin/env python
# coding: utf-8

# ### TODO: 
# - remove irrelevant lines
# - try baseline LR model
# - check how pre processing of other features allow to improve perf

# ## TODO:
# - train LR model
#     - hyper param optimize 
#     - confusion metrics
#     - AUC
#     - precision recall curve
# - visuzlize correct/ incorrect predictions
# - embedding visulization
# - dnn
#     - confusion metrics
#     - AUC
#     - precision recall curve

# In[1]:


get_ipython().system('pip install tensorflow numpy pandas sklearn livelossplot')
# In[ ]:
import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt

# In[3]:
from livelossplot import PlotLossesKeras


import os 
for dirname, _, filenames in os.walk('data'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[5]:
REDIT_200_TRAIN_DATASET = "../../data/reddit/reddit_200k_train.csv"
REDIT_200_TEST_DATASET = "../../data/reddit/reddit_200k_test.csv"


# In[6]:


df_cols = ["prev_idx", "body", "score", "parent_id", "id", "created_date", "retrieved_date", "removed"]

TEXT_COLUMN = "body"

df_200_train = pd.read_csv(REDIT_200_TRAIN_DATASET, 
                           names=df_cols,    
                           skiprows=1,
                           encoding="ISO-8859-1")
df_200_test = pd.read_csv(REDIT_200_TEST_DATASET, 
                           names=df_cols,    
                           skiprows=1,
                           encoding="ISO-8859-1")
df = pd.concat([df_200_train, df_200_test])
df = df.drop(["prev_idx", "parent_id", "id", "retrieved_date" ], axis=1)
df.head()
# raw_train_input = dataset['body']
# raw_train_output = dataset['REMOVED']


# In[7]:
x = df.drop("removed", axis=1)
y = df["removed"].values

X_train, X_test, y_train, y_test = train_test_split(
    x,y,
    stratify=y,
    random_state=42,
    test_size=0.1, shuffle=True)

# In[8]:
tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=80000,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r',
    lower=True,
    split=' ',
    char_level=False,
    oov_token='<UNK>'
)

tokenizer.fit_on_texts(X_train[TEXT_COLUMN])
# Get our training data word index
word_index = tokenizer.word_index


# In[9]:
def text_preprocessor(tokenizer, raw_data):
    # Encode training data sentenses into sequences
    train_sequences = tokenizer.texts_to_sequences(raw_data)
    embeded_data = tf.keras.preprocessing.sequence.pad_sequences(train_sequences, 
        padding='post', truncating='post', maxlen=255)
    return embeded_data    

X_train_embedding = text_preprocessor(tokenizer, X_train[TEXT_COLUMN])
X_test_embedding = text_preprocessor(tokenizer, X_test[TEXT_COLUMN])

# In[12]:
model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(80000, 16))
model.add(tf.keras.layers.GlobalAveragePooling1D())
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# In[13]:
model.summary()

# In[18]:
history = model.fit(X_train_embedding, y_train,
                    epochs=20,
                    batch_size=10000,
                    verbose=1,
                    validation_data=(X_test_embedding, y_test),
                    callbacks=[PlotLossesKeras()]
                   )


# In[25]:
MODEL_SAVE_DIR='../../models/tf_nsfw_text_classifer'

# serialize model to JSON
model_json = model.to_json()
with open(f'{MODEL_SAVE_DIR}/keras-model-w2v.json', 'w') as json_file:
    json_file.write(model_json)
    
# serialize weight to HDF5
model.save(f'{MODEL_SAVE_DIR}/models/keras-model-w2v.h5')
print('saved model to disk')


# In[27]:
import pickle
with open(f'{MODEL_SAVE_DIR}/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


loss, accuracy = model.evaluate(X_train_embedding, y_train)
print(f"Training accuracy: {accuracy:.4f}, loss: {loss}")
loss, accuracy = model.evaluate(X_test_embedding, y_test)
print(f"Training accuracy: {accuracy:.4f}, loss: {loss}")


# In[29]:
probabilities = model.predict(X_test_embedding)
pred = probabilities > 0.5
print(classification_report(y_test, pred))
confusion_matrix(y_test, pred)

fpr, tpr, _ = roc_curve(y_test, probabilities)
plt.plot(fpr, tpr)
plt.plot([0,1],[0,1], 'k--')
print("AUC: ", roc_auc_score(y_test, pred))



sample = ["fu*k you bitch"]
encode = text_preprocessor(tokenizer, sample)
result = model.predict(encode)
result