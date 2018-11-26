#!/usr/bin/python
# -*- coding: utf8 -*-"

import mnist
import neuralnet
import random

def play_a_bit(labels, images, nn):
    sample_size = 20
    nb_images = len(images)
    for i in range(0, sample_size):
        k = random.randint(0, nb_images-1)
        #mnist.image_to_png(images[k], '%d.png'%i)
        print(mnist.image_to_string(images[k]))
        print("This is a %d recognized as a %s" % (labels[k], nn.predict(images[k].pixels)))
        print(nn.evaluate(images[k].pixels))

TRAIN_LABELS="data/train-labels-idx1-ubyte"
TRAIN_IMAGES="data/train-images-idx3-ubyte"
TEST_LABELS="data/t10k-labels-idx1-ubyte"
TEST_IMAGES="data/t10k-images-idx3-ubyte"

# It takes ~10s to test 1000 images
def evaluate_network(nn, test_examples, test_labels):
    nb_tests = 100
    correct = 0
    for i in range(nb_tests):
        k = random.randint(0, len(test_examples)-1)
        #k = i%len(test_examples)
        result = nn.predict(test_examples[k])
        if result == test_labels[k]:
            correct += 1
    return correct*1.0/nb_tests

def load_data(labels_file, images_file, limit):
    labels = mnist.read_labels(labels_file, limit)
    images = mnist.read_images(images_file, limit)
    examples = [i.pixels for i in images]
    return labels, images, examples

if __name__ == "__main__":
    limit = None
    train_labels, train_images, train_examples = load_data(TRAIN_LABELS, TRAIN_IMAGES, limit)
    test_labels, test_images, test_examples = load_data(TEST_LABELS, TEST_IMAGES, limit)

    nn = neuralnet.NeuralNet(784, [20, 20, 10], neuralnet.Sigmoid())
    nn.load("network.txt")
    play_a_bit(train_labels, train_images, nn)

    training_rounds = 200
    samples_per_round = 50
    learning_rate = 1

    # Each loop takes ~1000s ~= 16m
    for t in range(0, 400):
        score = evaluate_network(nn, test_examples, test_labels)
        print("Round %s, Score before: %s, Learning rate: %s" % (t, score, learning_rate))
        nn.train(training_rounds, samples_per_round, learning_rate, train_examples, train_labels)
        nn.save("network.txt")
        #play_a_bit(train_labels, train_images, nn)
        learning_rate *= 0.99
