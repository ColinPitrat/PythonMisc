#!/usr/bin/python
# -*- coding: utf8 -*-"

import mnist
import neuralnet

if __name__ == "__main__":
    sample_size = 20
    labels = mnist.read_labels("data/t10k-labels-idx1-ubyte")[0:sample_size]
    images = mnist.read_images("data/t10k-images-idx3-ubyte")[0:sample_size]
    nn = neuralnet.NeuralNet(784, [20, 20, 10])
    for i in range(0, sample_size):
        print("This is a %d" % labels[i])
        print(mnist.image_to_string(images[i]))
        mnist.image_to_png(images[i], '%d.png'%i)
        inp = [p for line in images[i] for p in line]
        print(nn.evaluate(inp))
