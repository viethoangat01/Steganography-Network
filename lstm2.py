# -*- coding: utf-8 -*-
"""LSTM2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nSGY27pCX5EelTViW_bTdPeAC2yr7qXd
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from time import sleep

# %matplotlib inline

#Import the dataset
data_train=pd.read_csv('/content/drive/MyDrive/N12-Kĩ thuật giấu tin/CSV/4 patterns/4m9 records/.TRAIN_4_PATTERN_3.932.803.csv')
data_test=pd.read_csv('/content/drive/MyDrive/N12-Kĩ thuật giấu tin/CSV/4 patterns/4m9 records/.TEST_4_PATTERN_983.201.csv')
#ip.id max = 65535
#tcp.seq_raw max = 4124483354
X_train=data_train.iloc[:3932803,[1,2,3,4,5,6,7,8]].values
Y_train=data_train.iloc[:3932803,0].values

X_test=data_test.iloc[:983201,[1,2,3,4,5,6,7,8]].values
Y_test=data_test.iloc[:983201,0].values

from google.colab import drive
drive.mount('/content/drive')

X_train, Y_train, X_test, Y_test = list(map(lambda x: np.array(x, dtype=np.float64), [X_train, Y_train, X_test, Y_test]))
max_words = 3932804
max_len = 8
# tok = Tokenizer(num_words=max_words)
# tok.fit_on_texts(X_train)
# sequences = tok.texts_to_sequences(X_train)
#sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
sequences_matrix = X_train
Y_train = Y_train.reshape(-1, 1)
tcp_train = X_train[:, 2]
tcp_test = X_test[:, 2]
#Trộn train+test
tcp = np.concatenate([tcp_train, tcp_test])
#Sort tcp_test
tcp_set = list(set(tcp))
tcp_sort = list(np.sort(tcp_set))
len(tcp_set)
#Đánh index value tcp_train và tcp_test= index trong tcp+sort
result_train = []
result_test = []
for value in tcp_train:
  index = tcp_sort.index(value)
  result_train.append(index)

for value in tcp_test:
  index = tcp_sort.index(value)
  result_test.append(index)

result_train = np.array(result_train)
result_test = np.array(result_test)
X_train[:, 2] = result_train
X_test[:, 2] = result_test

def RNN():
    inputs = Input(name='inputs',shape=[max_len])
    layer = Embedding(max_words,50,input_length=max_len)(inputs)
    layer = LSTM(64)(layer)
    # layer = Merge([max_len, context_model], mode="dot", dot_axes=0)(layer)
    layer = Dense(256,name='FC1')(layer)
    layer = Activation('relu')(layer)
    layer = Dropout(0.5)(layer)
    layer = Dense(1,name='out_layer')(layer)
    layer = Activation('sigmoid')(layer)
    model = Model(inputs=inputs,outputs=layer)
    return model

model = RNN()
model.summary()
model.compile(loss='binary_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])

start = time.time()
model.fit(sequences_matrix,Y_train,batch_size=2048,epochs=10,
          validation_split=0.2)
end = time.time()

exe_time = end - start
print(exe_time)

start = time.time()
model.evaluate(X_test, Y_test)
end = time.time()
exe_time = end - start
print(exe_time)

# # Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, np.round(Y_predict))
print(cm)
rs=cm[0,0]+cm[1,1]
all=cm[0,0]+cm[0,1]+cm[1,0]+cm[1,1]
print(rs/all*100)
#TN FP
#FN TP

# confusion matrix to precision + recall
def cm2pr_binary(cm):
    p = cm[0,0]/np.sum(cm[:,0])
    r = cm[0,0]/np.sum(cm[0])
    return (p, r)
p,r = cm2pr_binary(cm)
print("precision = {0:.2f}, recall = {1:.2f}".format(p, r))
f1=2*(p*r)/(p+r)
print(f1)