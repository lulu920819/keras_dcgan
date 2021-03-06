'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function

import numpy as np

np.random.seed(1337)  # for reproducibility

from keras.utils import np_utils
from keras import backend as K

import gzip
# from six.moves import cPickle
import cPickle
import sys

def load_data(path='amazon_mnist.pkl.gz'):
	if path.endswith('.gz'):
		f = gzip.open(path, 'rb')
	else:
		f = open(path, 'rb')

	if sys.version_info < (3,):
		data = cPickle.load(f)
	else:
		data = cPickle.load(f, encoding='bytes')

	f.close()
	return  data



batch_size = 128
nb_classes = 10
nb_epoch = 12

# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)

# the data, shuffled and split between train and test sets
# (X_train, y_train), (X_test, y_test) = mnist.load_data()
path='amazon_mnist.pkl.gz'
(X_train, y_train), (X_test, y_test) = load_data(path)

if K.image_dim_ordering() == 'th':
    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

from kerasmodel.model_structure.example import *
model = creat_mnist(input_shape=input_shape,nb_classes=nb_classes,loadcurrent=False)


# optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True)
model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
