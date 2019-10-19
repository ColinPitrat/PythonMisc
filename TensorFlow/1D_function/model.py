#!/usr/bin/python
# -*- coding: utf8 -*-"

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def build_model():
  # It is interesting to see what happens when changing the activation function:
  #  - all relu/sigmoid/tanh (output of untrained model looks like a relu/sigmoid/tanh)
  #  - mixed
  model = keras.Sequential([
    layers.Dense(1, activation='relu', input_shape=[1]),
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
  # It is interesting to compare:
  #  - non normalized (putting 2.0*math.pi here in inputs)
  #  - normalized (putting 2.0*math.pi below in Output only)
  #inputs = [2.0*math.pi*(x-N/2)/N for x in range(N+1)]
  inputs = [(x-N/2)/N for x in range(N+1)]
  return pd.DataFrame({
    'Input': inputs,
    'Output': [math.sin(3.0*math.pi*x) for x in inputs],
  #  'Output': [math.sin(x) for x in inputs],
  })

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 10 == 0:
      print('')
    print('.', end='')

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  print(hist)
  hist.plot(x='epoch', y=['mean_absolute_error', 'val_mean_absolute_error'])
  plt.show()

def test_model(model, test):
  test['Predicted'] = model.predict(test['Input'])
  test.plot(x='Input', y=['Output', 'Predicted'])
  # Plotting output only is interesting to see the effect of activation function
  # especially in combination with a large input range
  #test.plot(x='Input', y=['Predicted'])
  print(test)
  plt.show()

def main():
  model = build_model()
  print(model.summary())

  # These are all prime numbers
  #train = generate_data(100109)
  train = generate_data(10007)
  validation = generate_data(3019)
  validation = (validation['Input'], validation['Output'])
  test = generate_data(5003)
  #print(train)
  #train.plot(x='Input', y='Output')
  #plt.show()

  test_model(model, test)

  history = model.fit(
    train['Input'], train['Output'],
    shuffle=True,
    epochs=200, validation_data=validation,
    verbose=False, callbacks=[PrintDot()])

  plot_history(history)
  test_model(model, test)


if __name__ == '__main__':
  main()
