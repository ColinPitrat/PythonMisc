#!/usr/bin/python
# -*- coding: utf8 -*-"

import math
import random

class LeakyReLu(object):

    def value(self, x):
        if x > 0:
            return x
        return 0.01*x

    def derivative(self, x):
        if x > 0:
            return 1
        return 0.01

    def name(self):
        return "LeakyReLu"

class ReLu(object):

    def value(self, x):
        if x > 0:
            return x
        return 0

    def derivative(self, x):
        if x > 0:
            return 1
        return 0

    def name(self):
        return "ReLu"

class Sigmoid(object):

    def value(self, x):
        try:
            # math.exp overflows after 709, replaces it with inf
            if x < -709:
                return 0
            e_x = math.exp(-x)
            return 1.0/(1+e_x)
        except:
            print("Sigmoid failing for x = %s" % x)
            raise

    def derivative(self, x):
        try:
            # math.exp overflows after 709, replaces it with inf
            if x < -709:
                return 0
            e_x = math.exp(-x)
            return e_x/(1+2*e_x+e_x*e_x)
        except:
            print("Sigmoid derivative failing for x = %s" % x)
            raise

    def name(self):
        return "Sigmoid"

class TanH(object):

    def value(self, x):
        return math.tanh(x)

    def derivative(self, x):
        th = math.tanh(x)
        return 1-th*th

    def name(self):
        return "TanH"


# TODO: Find a cleaner way to initialize the registry: metaclass or __init_subclass__
activations = {}
activations["Sigmoid"] = Sigmoid()
activations["LeakyReLu"] = LeakyReLu()
activations["ReLu"] = ReLu()
activations["TanH"] = TanH()


class Neuron(object):

    def __init__(self, nb_inputs, activation, average_gradient):
        self.nb_inputs = nb_inputs
        # TODO: support multiple initialization logics and try them in
        # combination with various other parameters, in particular activation
        # function
        # To support: [0, 1], [-1, 1], [-1, 1]/sqrt(N) ...
        self.weights = [random.uniform(-1, 1)/math.sqrt(nb_inputs) for i in range(0, nb_inputs)]
        self.bias = random.uniform(-1, 1)
        self.activation = activation
        self.average_gradient = average_gradient
        self.prepare_backprop()

    def __repr__(self):
        return "Neuron(b=%s, w=%s)" % (self.bias, self.weights[0:20])

    def __str__(self):
        return "Neuron(b=%s, w=%s)" % (self.bias, self.weights[0:20])

    def output(self, previous_layer_values, for_training):
        result = self.bias
        for i in range(0, self.nb_inputs):
            result += self.weights[i]*previous_layer_values[i]
        if for_training:
            # Save some info for per-eval backpropagation
            self.last_value = result
            self.inp = previous_layer_values
        return self.activation.value(result)

    def prepare_backprop(self):
        # Prepare some info for per-round backpropagation
        self.dw = [0]*len(self.weights)
        self.da = [0]*len(self.weights)
        self.db = 0
        self.nb_evals = 0

    def per_eval_backprop(self, error, learning_rate=1):
        self.nb_evals += 1
        delta = 2.0*error * self.activation.derivative(self.last_value)
        #print("Error:%s, Last value: %s, dsigma: %s, result: %s" % (error, self.last_value, self.activation.derivative(self.last_value), delta))
        self.db += delta*learning_rate
        for i in range(0, self.nb_inputs):
            self.dw[i] += delta*self.inp[i]*learning_rate
            self.da[i] += delta*self.weights[i]
        # Error contribution to be propagated to the previous layer
        return [self.da[i] for i in range(0, self.nb_inputs)]

    def per_round_backprop(self):
        denominator = 1
        if self.average_gradient:
            denominator = self.nb_evals
        self.bias += self.db / denominator
        for i in range(0, self.nb_inputs):
            self.weights[i] += self.dw[i] / denominator
        self.prepare_backprop()


class NeuralNet(object):

    def __init__(self, inputs_size, layers_sizes, activation, average_gradient=False):
        self.layers = []
        self.activation = activation
        self.average_gradient = average_gradient
        previous_size = inputs_size
        for size in layers_sizes:
            self.layers.append([Neuron(previous_size, activation, average_gradient) for i in range(0, size)])
            previous_size = size

    def evaluate(self, inputs, for_training=False):
        result = inputs
        for layer in self.layers:
            result = [neuron.output(result, for_training) for neuron in layer]
        return result

    def reverse_evaluate(self, inputs, for_training=False):
        result = inputs
        for layer in self.layers:
            result = [neuron.output(result, for_training) for neuron in layer]
        return result

    def per_eval_backprop(self, errors, learning_rate=1):
        result = errors
        for layer in reversed(self.layers):
            #print("Error from previous layer: %s" % result)
            #print("Layer: %s" % layer)
            new_result = None
            for r, neuron in zip(result, layer):
                contrib = neuron.per_eval_backprop(r, learning_rate)
                #print("Add contrib to error for previous layer: %s" % contrib)
                if new_result is None:
                    new_result = contrib
                else:
                    new_result = [nr + c for nr, c in zip(new_result, contrib)]
            l = len(layer)
            result = [nr/l for nr in new_result]

    def per_round_backprop(self):
        for layer in self.layers:
            for neuron in layer:
                neuron.per_round_backprop()

    def train(self, training_rounds, samples_per_round, learning_rate, examples, labels):
        nb_examples = len(examples)
        nb_classes = len(self.layers[-1])
        for i in range(0, training_rounds):
            error = 0
            for j in range(0, samples_per_round):
                # TODO: Understand ! Simply taking a random example seems to make the training much less efficient !
                #k = random.randint(0, nb_examples-1)
                k = (i*samples_per_round + j)%nb_examples
                result = self.evaluate(examples[k], for_training=True)
                expected = [0]*nb_classes
                expected[labels[k]] = 1
                #print("Result: %s" % result)
                #print("Expected: %s" % expected)
                errors = [e - r for r, e in zip(result, expected)]
                #print("Errors: %s" % errors)
                self.per_eval_backprop(errors, learning_rate)
                error += math.sqrt(sum([x*x for x in errors]))
            #print("Round %d: error=%s, learning_rate=%s" % (i, error/samples_per_round, learning_rate))
            self.per_round_backprop()

    def predict(self, example, for_training=False):
        scores = self.evaluate(example, for_training)
        return scores.index(max(scores))

    def load(self, filename):
        with open(filename, "r") as f:
            act = f.readline().strip()
            if act not in activations:
                raise RuntimeError("Unknown activation function '%s' in '%s'" % (act, filename))
            self.activation = activations[act]
            avg = f.readline().strip()
            if avg not in ["True", "False"]:
                raise RuntimeError("Expected boolean for average gradient, got '%s'" % avg)
            self.average_gradient = (avg == "True")
            layer_sizes = [int(x) for x in f.readline().split(',')]
            self.layers = []
            for l in layer_sizes:
                layer = []
                for i in range(l):
                    weights = [float(x) for x in f.readline().split(',')]
                    # TODO: Cleaner way to initialize neuron (e.g constructor with params taking either #inputs or list of weights)
                    neuron = Neuron(len(weights)-1, self.activation, self.average_gradient)
                    neuron.weights = weights[:-1]
                    neuron.bias = weights[-1]
                    neuron.prepare_backprop()
                    layer.append(neuron)
                self.layers.append(layer)

    def save(self, filename):
        with open(filename, "w") as f:
            f.write(self.activation.name() + "\n")
            f.write("%s\n" % self.average_gradient)
            f.write(",".join(["%s" % len(layer) for layer in self.layers]) + "\n")
            for layer in self.layers:
                for neuron in layer:
                    f.write(",".join(["%s" % weight for weight in neuron.weights]) + ",%s\n" % neuron.bias)

    def reverse(self):
        nb_inputs = len(self.layers[-1])
        layers = [len(l) for l in reversed(self.layers[:-1])]
        layers.append(len(nn.layers[0][0].weights))
        rev_nn = NeuralNet(nb_inputs, layers, self.activation)
        for li, l in enumerate(self.layers):
            rl = rev_nn.layers[-li-1]
            for ni, n in enumerate(l):
                rn = rl[ni]
                rn.weights = [0] * len(n.weights)
                for wi, w in enumerate(n.weights):
                    rn.weights[wi] = w
        return rev_nn

    def __str__(self):
        weights = ""
        for i, l in enumerate(self.layers):
            weights += "Layer %s: \n" % i
            for n in l:
                weights += "    [%s] - %s\n" % (",".join(["%s" % w for w in n.weights]), n.bias)
        return "[NeuralNet %s - activation:%s - avg gradient: %s layers:\n%s]" % (len(self.layers), self.activation.name(), self.average_gradient, weights)
