import matplotlib.pyplot as plt
import math
import copy
import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import numpy as np


def get_dataset(training=True):
	fashion_mnist = keras.datasets.fashion_mnist
	(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

	if training == False:
		return (test_images, test_labels)

	else:
		return (train_images, train_labels)

def print_stats(images, labels):
	images_len = len(images)
	images_dim = len(images[0])

	class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
	count = [0,0,0,0,0,0,0,0,0,0]

	for i in range(len(labels)):
   		count[labels[i]] += 1

	print(images_len)
	print(str(images_dim) + "x" + str(images_dim))
	
	for i in range(len(class_names)):
		print(str(i) + ". " + str(class_names[i]) + " - " + str(count[i]))

def view_image(image, label):
	plt.imshow(image, interpolation='nearest')
	plt.colorbar()
	plt.title(label)
	plt.show()

def build_model():
	model = keras.Sequential()
	model.add(Flatten())
	model.add(Dense(128))
	model.add(Activation('relu'))
	model.add(Dense(10))
	model.add(Activation('softmax'))
	model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model 

def train_model(model, images, labels, T):
	model.fit(images, labels, verbose = 0, epochs = T)

def train_model_ret(model, images, labels, T):
	model.fit(images, labels, verbose = 0, epochs = T)
	return model

def evaluate_model(model, images, labels, show_loss=True):
	test_loss, test_accuracy = model.evaluate(images, labels, verbose = 0)

	test_accuracy = float(100*test_accuracy)
	#test_loss = float(0.1 * test_loss)
	
	if show_loss == False: #only acc
		print("Accuracy: " + str(round(test_accuracy,2)) + "%")

	else:
		print("Lose: " + str(round(test_loss,2)))
		print("Accuracy: " + str(round(test_accuracy,2)) + "%")

def predict_label(model, images, index):
	class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
	pred = model.predict(images)[index]
	comp_pred = copy.deepcopy(pred)
	pred = np.sort(pred)[::-1]
	index = []

	for i in range(len(pred)):
		for j in range(len(pred)):
			if pred[i] == comp_pred[j]:
				index.append(j)
			if len(index) == 3:
				break

	print(class_names[index[0]] +": " + str(round(100*pred[0],2)) + "%")
	print(class_names[index[1]] +": " + str(round(100*pred[1],2)) + "%")
	print(class_names[index[2]] +": " + str(round(100*pred[2],2)) + "%")

