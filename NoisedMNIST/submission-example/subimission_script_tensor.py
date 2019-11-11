# -*- coding: utf-8 -*-

import requests
from pathlib import Path
from typing import Union

import numpy as np

#from sklearn.pipeline import Pipeline
#from sklearn.datasets import fetch_openml
#from sklearn.preprocessing import StandardScaler
#from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
#from sklearn.neural_network import MLPClassifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
#from sklearn.base import BaseEstimator, TransformerMixin
#from sklearn.metrics import confusion_matrix, classification_report

import tensorflow as tf
from tensorflow import keras


import matplotlib.pyplot as plt
#from sklearn.linear_model import LogisticRegression


DATASET_URL = ('https://firebasestorage.googleapis.com/v0/b/hackeps-2019.'
                'appspot.com/o/noised-MNIST.npz?alt=media&token=4cee641b-9e31'
                '-42c4-b9c8-e771d2eecbad')


def download_file(url: str, 
                    file_path: Union[str, Path]):
    r = requests.get(DATASET_URL, allow_redirects=True)
    Path(file_path).open('wb').write(r.content)


def train(x: np.ndarray, 
            y: np.ndarray):    
    model = keras.Sequential([
        #keras.layers.Input((28,28,1)),
        #keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Conv2D(64, kernel_size=(3, 3), input_shape=(28, 28, 1), activation='relu', padding='same'),
        #keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding='same'),
        keras.layers.Dense(16*16, activation='relu'),
        keras.layers.Dense(14*14, activation='relu'),
        keras.layers.Dense(12*12, activation='relu'),
        keras.layers.Dense(10*10, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
    model.fit(x, y, epochs=15, batch_size=128)
    return model


def create_submission_file(preds: np.ndarray, 
                             base_path: Union[str, Path] = '.'):
    preds = preds.flatten().astype(str)
    preds = '\n'.join(preds)
    fname = Path(base_path)/'submission.txt'
    fname.open('w').write(preds)

def shape(x):
    return x.reshape((x.shape[0], 28, 28, 1))

fname = 'noised-MNIST.npz'
extra_fname = 'noised-MNIST-EXTRA.npz'
if not Path(fname).is_file():
    download_file(DATASET_URL, fname)

# Download the sumission data
data = np.load(fname)
x, y, x_submission = data.values()
x = shape(x)
x_submission = shape(x_submission)
x_extra, y_extra = np.load(extra_fname).values()
x_extra = shape(x_extra)
x_train, x_test, y_train, y_test = train_test_split(x_extra, y_extra, test_size=.40, random_state=42)

# Train the model with whole data provided in the noised MNIST data
model = train(x_train, y_train)

# Inference on the x_submission data
test_loss, test_acc = model.evaluate(x_test,  y_test, verbose=2)

print('WAIT', test_loss, test_acc)
input('W')

# Remember to commit and push this file
# create_submission_file(y_pred)


#TODO: Fix this:
def plot_confusion_matrix(y_true, y_pred,
                            cmap=plt.cm.Blues):

    title = 'Confusion matrix'
    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            title=title,
            ylabel='True label',
            xlabel='Predicted label')


print(classification_report(y_test, y_pred))
print('Testing with', len(y_test))
plot_confusion_matrix(y_test, y_pred)
plt.show()