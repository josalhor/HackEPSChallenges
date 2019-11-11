# -*- coding: utf-8 -*-

import requests
from pathlib import Path
from typing import Union

import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import confusion_matrix, classification_report

import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


DATASET_URL = ('https://firebasestorage.googleapis.com/v0/b/hackeps-2019.'
				'appspot.com/o/noised-MNIST.npz?alt=media&token=4cee641b-9e31'
				'-42c4-b9c8-e771d2eecbad')


def download_file(url: str, 
					file_path: Union[str, Path]):
	r = requests.get(DATASET_URL, allow_redirects=True)
	Path(file_path).open('wb').write(r.content)


def train(x: np.ndarray, 
			y: np.ndarray) -> LogisticRegression:
	#lr = LogisticRegression(multi_class='auto', 
	#						solver='liblinear',
	#						max_iter=500,
	#						verbose=2)
	#lr = RandomForestClassifier(n_estimators=1000,
	#							max_features=50,
	#							max_depth=None,
	#							random_state=42,
	#							verbose=2)
	lr = MLPClassifier(hidden_layer_sizes=(220, 170, 140, 100))
	#lr = KNeighborsClassifier(	n_neighbors=25,
	#							weights='distance',
	#							n_jobs=-1)
	#lr = AdaBoostClassifier(base_estimator=KNeighborsClassifier(n_neighbors=25, weights='distance')
							#n_estimators=100,
							#learning_rate=0.8
	#						)
	#lr = GaussianNB()
	lr.fit(x, y)
	return lr


def create_submission_file(preds: np.ndarray, 
							 base_path: Union[str, Path] = '.'):
	preds = preds.flatten().astype(str)
	preds = '\n'.join(preds)
	fname = Path(base_path)/'submission.txt'
	fname.open('w').write(preds)

fname = 'noised-MNIST.npz'

if not Path(fname).is_file():
	download_file(DATASET_URL, fname)

# Download the sumission data
data = np.load(fname)
x, y, x_submission = data.values()

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.40, random_state=42)

# Train the model with whole data provided in the noised MNIST data
model = train(x_train, y_train)

# Inference on the x_submission data
#y_pred = model.predict(x_submission)
y_pred = model.predict(x_test)

# Remember to commit and push this file
#create_submission_file(y_pred)

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