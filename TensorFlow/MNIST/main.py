#!/usr/bin/python
# -*- coding: utf8 -*-"

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import mnist


# MNIST files
TRAIN_LABELS="data/mnist/train-labels-idx1-ubyte"
TRAIN_IMAGES="data/mnist/train-images-idx3-ubyte"
TEST_LABELS="data/mnist/t10k-labels-idx1-ubyte"
TEST_IMAGES="data/mnist/t10k-images-idx3-ubyte"

# Fashion MNIST files
TRAIN_LABELS="data/fashion_mnist/train-labels-idx1-ubyte"
TRAIN_IMAGES="data/fashion_mnist/train-images-idx3-ubyte"
TEST_LABELS="data/fashion_mnist/t10k-labels-idx1-ubyte"
TEST_IMAGES="data/fashion_mnist/t10k-images-idx3-ubyte"


def build_model():
  model = keras.Sequential([
          layers.Dense(20, input_shape=(784,)),
          layers.Dense(20, activation='relu'),
          layers.Dense(10, activation='softmax')
  ])

  model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

  return model

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0:
      print('')
    elif epoch % 10 == 0:
      print(' ', end='')
    print('.', end='')
    sys.stdout.flush()

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  print(hist)
  hist.plot(x='epoch', y=['acc', 'val_acc'])
  plt.show()

def load_data(labels_file, images_file, limit=None):
    labels = np.array(mnist.read_labels(labels_file, limit))
    images = mnist.read_images(images_file, limit)
    examples = np.array([i.pixels for i in images])
    return examples, labels, images

def test_model(model, examples, labels):
  predicted = np.argmax(model.predict(examples), axis=1)
  test = pd.DataFrame({'Real': labels, 'Predicted': predicted})
  test['Count'] = [1]*len(test)
  test = test.groupby(['Real', 'Predicted']).count().reset_index()
  print(test.pivot(index='Real', columns='Predicted', values='Count'))
  test.plot.scatter(x='Real', y='Predicted', s=test['Count'])
  plt.show()

def main():
  model = build_model()
  print(model.summary())

  limit = None
  train_examples, train_labels, train_images = load_data(TRAIN_LABELS, TRAIN_IMAGES, limit)
  test_examples, test_labels, test_images = load_data(TEST_LABELS, TEST_IMAGES, limit)

  test_model(model, test_examples, test_labels)

  history = model.fit(
    train_examples, train_labels,
    shuffle=True,
    epochs=100,
    validation_split=0.2,
    verbose=False,
    callbacks=[PrintDot()])
  print('')

  plot_history(history)
  test_model(model, test_examples, test_labels)

if __name__ == '__main__':
  main()
