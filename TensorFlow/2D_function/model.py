#!/usr/bin/python
# -*- coding: utf8 -*-"

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import datetime
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_model():
  model = keras.Sequential([
    layers.Dense(2, activation='relu', input_shape=[2]),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(1),
  ])

  optimizer = keras.optimizers.RMSprop(0.001)

  model.compile(
          loss='mse',
          optimizer=optimizer,
          metrics=['mae', 'mse'])

  return model

def generate_data(N):
  xs = [(x-N/2)/N for y in range(N+1) for x in range(N+1)]
  ys = [(y-N/2)/N for y in range(N+1) for x in range(N+1)]
  inputs = zip(xs, ys)
  return pd.DataFrame({
    'X': xs,
    'Y': ys,
    'Output': [math.sin(2.0*math.pi*x)*math.sin(2.0*math.pi*y) for (x, y) in inputs],
  })

def chunks(l, size):
  return np.array([l[i:i+size] for i in range(0, len(l), size)])

def test_model(model, test, destfile=None):
  test['Predicted'] = model.predict(test[['X','Y']])
  fig = plt.figure(figsize=(20, 10))
  ax = fig.add_subplot(111, projection='3d')
  xs, ys, zs, zs2 = test['X'].values, test['Y'].values, test['Output'].values, test['Predicted'].values
  N = int(math.sqrt(len(xs)))
  ax.plot_wireframe(chunks(xs, N), chunks(ys, N), chunks(zs, N), color='b')
  ax.plot_wireframe(chunks(xs, N), chunks(ys, N), chunks(zs2, N), color='r')
  if destfile:
    plt.savefig(destfile)
  else:
    plt.show()
  plt.close()

class Progress(keras.callbacks.Callback):
  def __init__(self, model, test):
    self._model = model
    self._test = test
    self._runname = datetime.datetime.now().isoformat()
    if not os.path.exists("results"):
        os.mkdir("results")
    os.mkdir("results/%s" % self._runname)

  def svg_file(self, epoch):
    return "results/%s/%06d.svg" % (self._runname, epoch)

  def on_epoch_end(self, epoch, logs):
    if epoch % 10 == 0:
      print('')
    print('.', end='')
    test_model(self._model, self._test, destfile=self.svg_file(epoch+1))

  def plot_history(self, history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print(hist)
    hist.plot(x='epoch', y=['mean_absolute_error', 'val_mean_absolute_error'], figsize=(20, 10))
    #plt.show()
    plt.savefig("results/%s/history.svg" % self._runname)
    plt.close()

def main():
  model = build_model()
  print(model.summary())

  # These are all prime numbers
  train = generate_data(101)
  validation = generate_data(19)
  test = generate_data(53)

  progress = Progress(model, test)
  test_model(model, test, destfile=progress.svg_file(0))

  train_labels = train.pop('Output')
  validation_labels = validation.pop('Output')
  print("train: %s" % train['X'])
  print("train_labels: %s" % train_labels)
  history = model.fit(
    train, train_labels,
    shuffle=True,
    epochs=1000,
    #validation_split=0.2,
    validation_data=(validation, validation_labels),
    verbose=False,
    callbacks=[progress])

  progress.plot_history(history)
  test_model(model, test)


if __name__ == '__main__':
  main()
