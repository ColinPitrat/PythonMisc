#!/usr/bin/python
# -*- coding: utf8 -*-"

import mnist
import neuralnet
import random
import sys

def play_a_bit(labels, images, nn):
    sample_size = 20
    nb_images = len(images)
    for i in range(0, sample_size):
        k = random.randint(0, nb_images-1)
        #mnist.image_to_png(images[k], '%d.png'%i)
        print(mnist.image_to_string(images[k]))
        print("This is a %d recognized as a %s" % (labels[k], nn.predict(images[k].pixels, for_training=False)))
        print(nn.evaluate(images[k].pixels, for_training=False))

TRAIN_LABELS="data/train-labels-idx1-ubyte"
TRAIN_IMAGES="data/train-images-idx3-ubyte"
TEST_LABELS="data/t10k-labels-idx1-ubyte"
TEST_IMAGES="data/t10k-images-idx3-ubyte"

# It takes ~10s to test 1000 images
def fast_evaluate_network(nn, test_examples, test_labels):
    nb_tests = 1000
    correct = 0
    for i in range(nb_tests):
        #k = random.randint(0, len(test_examples)-1)
        k = i%len(test_examples)
        result = nn.predict(test_examples[k], for_training=False)
        if result == test_labels[k]:
            correct += 1
    return correct*1.0/nb_tests

def evaluate_network(nn, test_examples, test_labels):
    correct = 0
    nb_tests = 0
    for label, example in zip(test_labels, test_examples):
        result = nn.predict(example, for_training=False)
        if result == label:
            correct += 1
        nb_tests += 1
    return correct*1.0/nb_tests

def load_data(labels_file, images_file, limit):
    labels = mnist.read_labels(labels_file, limit)
    images = mnist.read_images(images_file, limit)
    examples = [i.pixels for i in images]
    return labels, images, examples

def load_params(filename):
    """Load config file with the following format:

    output_file
    layers (comma separated ints, starting from first hidden layer and including the end layer)
    activation
    nb_epochs, rounds_per_epoch, samples_per_round
    learning_rate (single float or 40 comma separated floats)
    """
    result = {}
    result['limit'] = None
    with open(filename, "r") as f:
        result['output_file'] = f.readline().strip()
        result['layers'] = [int(x) for x in f.readline().strip().split(',')]
        assert result['layers'][-1] == 10
        result['activation'] = f.readline().strip()
        assert result['activation'] in neuralnet.activations
        ne, rpe, spr = [int(x) for x in f.readline().strip().split(',')]
        result['nb_epochs'] = ne
        result['rounds_per_epoch'] = rpe
        result['samples_per_round'] = spr
        lr = [float(x) for x in f.readline().strip().split(',')]
        if len(lr) == 1:
            lr = lr * ne
        assert len(lr) == ne
        result['learning_rates'] = lr
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Syntaxe: %s <config file>" % sys.argv[0])
        sys.exit(-1)

    params = load_params(sys.argv[1])

    limit = params['limit']
    train_labels, train_images, train_examples = load_data(TRAIN_LABELS, TRAIN_IMAGES, limit)
    test_labels, test_images, test_examples = load_data(TEST_LABELS, TEST_IMAGES, limit)

    layers = params['layers']
    output_file = params['output_file']

    nn = neuralnet.NeuralNet(784, layers, neuralnet.Sigmoid())
    #nn.load("network.txt")
    #play_a_bit(train_labels, train_images, nn)

    nb_epochs = params['nb_epochs']
    training_rounds = params['rounds_per_epoch']
    samples_per_round = params['samples_per_round']
    learning_rates = params['learning_rates']

    # Each loop takes ~1000s ~= 16m
    for epoch in range(0, nb_epochs):
        learning_rate = learning_rates[epoch]
        score = evaluate_network(nn, test_examples, test_labels)
        print("Epoch %s, Score before: %s, Learning rate: %s" % (epoch, score, learning_rate))
        nn.train(training_rounds, samples_per_round, learning_rate, train_examples, train_labels)
        nn.save(output_file)
        #play_a_bit(train_labels, train_images, nn)
        #learning_rate *= 0.99
