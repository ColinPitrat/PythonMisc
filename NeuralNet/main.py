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
def fast_evaluate_network(nn, test_examples, test_labels, test_images):
    nb_tests = 1000
    correct = 0
    for i in range(nb_tests):
        #k = random.randint(0, len(test_examples)-1)
        k = i%len(test_examples)
        result = nn.predict(test_examples[k], for_training=False)
        if result == test_labels[k]:
            correct += 1
    return correct*1.0/nb_tests

def show_confusion(confusion):
    print("Confusion matrix:")
    print("Predicted / Real ->")
    print("|")
    print("v")
    # Header
    line = " "
    for j in range(len(confusion)):
      line += "\t%s" % j
    print(line)
    # Lines
    for i in range(len(confusion)):
      line = "%s" % i
      for j in range(len(confusion)):
        line += "\t%s" % confusion[i][j]
      print(line)

def evaluate_network(nn, test_examples, test_labels, test_images, verbose=False, confusion=None):
    correct = 0
    nb_tests = 0
    for label, example, image in zip(test_labels, test_examples, test_images):
        result = nn.predict(example, for_training=False)
        if result == label:
            correct += 1
        elif verbose:
            print("This is a %d recognized as a %s" % (label, result))
            print(mnist.image_to_string(image))
        if confusion:
            confusion[result][label] += 1
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
        avg = f.readline().strip()
        assert avg in ["True", "False"]
        result['average_gradient'] = (avg == "True")
        lr = [float(x) for x in f.readline().strip().split(',')]
        if len(lr) == 1:
            lr = lr * ne
        assert len(lr) == ne
        result['learning_rates'] = lr
    return result

def reverse_evaluate(filename):
    nn = neuralnet.NeuralNet(0, [], neuralnet.Sigmoid())
    nn.load(filename)
    inputs = len(nn.layers[-1])
    layers = [len(l) for l in reversed(nn.layers[:-1])]
    layers.append(len(nn.layers[0][0].weights))
    rev_nn = neuralnet.NeuralNet(inputs, layers, nn.activation)
    for li, l in enumerate(nn.layers):
        rl = rev_nn.layers[-li-1]
        for ni, n in enumerate(l):
            rn = rl[ni]
            rn.weights = [0] * len(n.weights)
            for wi, w in enumerate(n.weights):
                rn.weights[wi] = w
            rn.bias = -n.bias
    results = []
    for i in range(inputs):
        inp = [0] * inputs
        inp[i] = 1
        result = rev_nn.evaluate(inp, for_training=False)
        results.append(result)
    return results

def test_network(filename):
    test_labels, test_images, test_examples = load_data(TEST_LABELS, TEST_IMAGES, None)
    labels = set(test_labels)
    confusion = [[0] * len(labels) for i in range(len(labels))]
    nn = neuralnet.NeuralNet(784, [10], neuralnet.Sigmoid(), average_gradient=False)
    nn.load(filename)
    score = evaluate_network(nn, test_examples, test_labels, test_images, verbose=False, confusion=confusion)
    print("Score: %s" % score)
    show_confusion(confusion)

def train_network(filename):
    params = load_params(filename)
    limit = params['limit']

    train_labels, train_images, train_examples = load_data(TRAIN_LABELS, TRAIN_IMAGES, limit)
    test_labels, test_images, test_examples = load_data(TEST_LABELS, TEST_IMAGES, limit)

    layers = params['layers']
    output_file = params['output_file']
    average_gradient = params['average_gradient']
    activation = neuralnet.activations[params['activation']]

    nn = neuralnet.NeuralNet(784, layers, activation, average_gradient)
    # Uncomment to continue an already started training
    #nn.load(params['output_file'])

    nb_epochs = params['nb_epochs']
    training_rounds = params['rounds_per_epoch']
    samples_per_round = params['samples_per_round']
    learning_rates = params['learning_rates']

    # Each loop takes ~1000s ~= 16m
    for epoch in range(0, nb_epochs):
        learning_rate = learning_rates[epoch]
        score = evaluate_network(nn, test_examples, test_labels, test_images)
        print("Epoch %s, Score before: %s, Learning rate: %s" % (epoch, score, learning_rate))
        nn.train(training_rounds, samples_per_round, learning_rate, train_examples, train_labels)
        nn.save(output_file)

def usage(error):
    if error:
        print("ERROR: %s" % error)
        print("")
    print("Syntaxe: %s <action> <file>" % sys.argv[0])
    print("  where action can be 'train' or 'test'")
    print("  for 'train', file is a configuration file")
    print("  for 'test', file is a network file")
    sys.exit(-1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage("Invalid number of arguments")

    if sys.argv[1] == 'train':
        train_network(sys.argv[2])
    elif sys.argv[1] == 'test':
        test_network(sys.argv[2])
    elif sys.argv[1] == 'reverse':
        results = reverse_evaluate(sys.argv[2])
        nn = neuralnet.NeuralNet(0, [], neuralnet.Sigmoid())
        nn.load(sys.argv[2])
        for i, r in enumerate(results):
            print("")
            print("This is a typical %s:" % i)
            img = mnist.Img(28, 28, r)
            print(mnist.image_to_string(img))
            print("Recognized as a %s: %s" % (nn.predict(r, for_training=False), nn.evaluate(r, for_training=False)))
    else:
        usage("Unknown action '%s'" % sys.argv[1])
