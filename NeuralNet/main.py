#!/usr/bin/python
# -*- coding: utf8 -*-"

import mnist

if __name__ == "__main__":
    labels = mnist.read_labels("data/t10k-labels-idx1-ubyte")[0:10]
    images = mnist.read_images("data/t10k-images-idx3-ubyte")[0:10]
    for i in range(0, 10):
        print("This is a %d" % labels[i])
        print(mnist.image_to_string(images[i]))
        mnist.image_to_png(images[i], '%d.png'%i)
