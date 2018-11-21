import random

class Neuron(object):

    def __init__(self, nb_inputs):
        self.nb_inputs = nb_inputs
        self.weights = [random.uniform(-1, 1) for i in range(0, nb_inputs)]
        self.bias = random.uniform(-1, 1)

    # TODO: Add activation function (ReLu)
    def output(self, previous_layer_values):
        result = self.bias
        for i in range(0, self.nb_inputs):
            result += self.weights[i]*previous_layer_values[i]
        return result


class NeuralNet(object):

    def __init__(self, inputs_size, layers_sizes):
        self.layers = []
        previous_size = inputs_size
        for size in layers_sizes:
            self.layers.append([Neuron(previous_size) for i in range(0, size)])
            print("  %s neurons having %s inputs" % (size, previous_size))
            previous_size = size

    def evaluate(self, inputs):
        result = inputs
        for layer in self.layers:
            #print("  Calling with %s inputs on %s neurons" % (len(result), len(layer)))
            result = [neuron.output(result) for neuron in layer]
        return result
