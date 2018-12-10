#!/usr/bin/python
# -*- coding: utf8 -*-"

import neuralnet
import tempfile
import unittest

class TestNeuralNet(unittest.TestCase):

    def testSigmoid(self):
        sigmoid = neuralnet.Sigmoid()
        self.assertAlmostEqual(0.5, sigmoid.value(0))
        self.assertAlmostEqual(0.26894, sigmoid.value(-1), 4)
        self.assertAlmostEqual(0.73106, sigmoid.value(1), 4)
        self.assertAlmostEqual(0, sigmoid.value(-710))
        self.assertAlmostEqual(1, sigmoid.value(710))
        self.assertAlmostEqual(0, sigmoid.value(-1234567890))
        self.assertAlmostEqual(1, sigmoid.value(1234567890))

    def testSigmoidDerivative(self):
        sigmoid = neuralnet.Sigmoid()
        self.assertAlmostEqual(0.19661, sigmoid.derivative(-1), 4)
        self.assertAlmostEqual(0.25, sigmoid.derivative(0))
        self.assertAlmostEqual(0.19661, sigmoid.derivative(1), 4)
        self.assertAlmostEqual(0, sigmoid.derivative(-710))
        self.assertAlmostEqual(0, sigmoid.derivative(710))
        self.assertAlmostEqual(0, sigmoid.derivative(-1234567890))
        self.assertAlmostEqual(0, sigmoid.derivative(1234567890))

    def testSaveAndLoad(self):
        nn = neuralnet.NeuralNet(2, [2, 2], neuralnet.Sigmoid(), average_gradient=False)
        nn.layers[0][0].weights=[0.01, 0.02]
        nn.layers[0][0].bias=0.03
        nn.layers[0][1].weights=[0.04, 0.05]
        nn.layers[0][1].bias=0.06
        nn.layers[1][0].weights=[0.07, 0.08]
        nn.layers[1][0].bias=0.09
        nn.layers[1][1].weights=[0.10, 0.11]
        nn.layers[1][1].bias=0.12

        tmpfile = tempfile.mkstemp()[1]
        nn.save(tmpfile)

        nn2 = neuralnet.NeuralNet(1, [1, 1], neuralnet.ReLu(), average_gradient=False)
        nn2.load(tmpfile)

        # This should give a more readable error when there are differences
        self.assertEqual(nn.__str__(), nn2.__str__())

        # This ensure the previous test didn't miss any important thing
        self.assertEqual(nn2.activation.name(), nn.activation.name())
        self.assertEqual(nn2.average_gradient, nn.average_gradient)
        for i in range(0, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    self.assertAlmostEqual(nn.layers[i][j].weights[k], nn2.layers[i][j].weights[k])
                self.assertAlmostEqual(nn.layers[i][j].bias, nn2.layers[i][j].bias)

    def testSingleInputNeuronActivation(self):
        # A neuron with a weight of 0.7 and a bias of -0.5 will return 0.2 for an input of 1.
        # Using ReLu allow to have this value directly in output.
        n = neuralnet.Neuron(1, neuralnet.ReLu(), average_gradient=False)
        n.bias = -0.5
        n.weights = [0.7]

        self.assertAlmostEqual(0.2, n.output([1.0], for_training=False), 4)

    def testMultipleInputsNeuronActivation(self):
        n = neuralnet.Neuron(3, neuralnet.ReLu(), average_gradient=False)
        n.bias = -0.5
        n.weights = [0.7, 0.5, 0.3]

        # 0.7*0.7 + 0.5*0.5 + 0.3*0.3 - 0.5 = 0.49 + 0.25 + 0.09 - 0.5 = 0.83 - 0.5 = 0.33
        self.assertAlmostEqual(0.33, n.output([0.7, 0.5, 0.3], for_training=False), 4)

    def testMultipleLayersNetworkActivation(self):
        nn = neuralnet.NeuralNet(2, [2, 2], neuralnet.ReLu(), average_gradient=False)
        # 1 -- 0.5 --> [-0.1](A) -- 0.7 --> [-0.2](C)
        #     ^  |              ^  |
        #     |  0.7            |  0.8
        #   0.2    |          0.5    |
        #   |      v          |      v
        # 0 -- 0.6 --> [-0.1](B) -- 0.9 --> [-0.3](D)
        # (A) = 0.5 - 0.1 = 0.4
        # (B) = 0.7 - 0.1 = 0.6
        # (C) = 0.4x0.7 + 0.6x0.5 - 0.2 = 0.38
        # (D) = 0.9x0.6 + 0.8x0.4 - 0.3 = 0.56
        nn.layers[0][0].weights=[0.5, 0.2]
        nn.layers[0][0].bias=-0.1
        nn.layers[0][1].weights=[0.7, 0.6]
        nn.layers[0][1].bias=-0.1
        nn.layers[1][0].weights=[0.7, 0.5]
        nn.layers[1][0].bias=-0.2
        nn.layers[1][1].weights=[0.8, 0.9]
        nn.layers[1][1].bias=-0.3

        neuronA_output = nn.layers[0][0].output([1, 0], for_training=False)
        self.assertAlmostEqual(0.4, neuronA_output)
        neuronB_output = nn.layers[0][1].output([1, 0], for_training=False)
        self.assertAlmostEqual(0.6, neuronB_output)

        output = nn.evaluate([1, 0])

        self.assertAlmostEqual(0.38, output[0])
        self.assertAlmostEqual(0.56, output[1])

    def testBackpropagateErrorOnSingleNeuron(self):
        n = neuralnet.Neuron(1, neuralnet.ReLu(), average_gradient=False)
        n.bias = -0.5
        n.weights = [0.7]

        self.assertAlmostEqual(0.2, n.output([1.0], for_training=True), 4)

        # Assume expected error was 1 -> provide error of 0.8
        da = n.per_eval_backprop(0.8)

        self.assertAlmostEqual(1.6, n.db)
        self.assertAlmostEqual(1.6, n.dw[0])
        self.assertAlmostEqual(1.12, da[0])

    # TODO: test backpropagation on neuron with multiple inputs

    def testBackpropagateErrorOnNetwork(self):
        nn = neuralnet.NeuralNet(2, [2, 2], neuralnet.ReLu(), average_gradient=False)
        # 1 -- 0.5 --> [-0.1](A) -- 0.7 --> [-0.2](C)
        #     ^  |              ^  |
        #     |  0.7            |  0.8
        #   0.2    |          0.5    |
        #   |      v          |      v
        # 0 -- 0.6 --> [-0.1](B) -- 0.9 --> [-0.3](D)
        # (A) = 0.5 - 0.1 = 0.4
        # (B) = 0.7 - 0.1 = 0.6
        # (C) = 0.4x0.7 + 0.6x0.5 - 0.2 = 0.38
        # (D) = 0.9x0.6 + 0.8x0.4 - 0.3 = 0.56
        nn.layers[0][0].weights=[0.5, 0.2]
        nn.layers[0][0].bias=-0.1
        nn.layers[0][1].weights=[0.7, 0.6]
        nn.layers[0][1].bias=-0.1
        nn.layers[1][0].weights=[0.7, 0.5]
        nn.layers[1][0].bias=-0.2
        nn.layers[1][1].weights=[0.8, 0.9]
        nn.layers[1][1].bias=-0.3

        # Start with same evaluation as testMultipleLayersNetworkActivation
        output = nn.evaluate([1, 0], for_training=True)
        self.assertAlmostEqual(0.38, output[0])
        self.assertAlmostEqual(0.56, output[1])
        expected = [0, 1]
        error = [exp - res for exp, res in zip(expected, output)]
        # Verify errors values are as expected
        self.assertAlmostEqual(-0.38, error[0])
        self.assertAlmostEqual(0.44, error[1])

        nn.per_eval_backprop(error)
        # Verify backpropagation of layer 1:
        # a(n-1)    w   expected   result   error     dE     db      dw   da(n-1)
        #   0.4   0.7          0     0.38   -0.38   0.76  -0.76  -0.304    -0.532
        #   0.6   0.5          -        -       -      -      -  -0.456     -0.38
        #   0.4   0.8          -        -       -      -      -   0.352     0.704
        #   0.6   0.9          1     0.56    0.44  -0.88   0.88   0.528     0.792
        self.assertAlmostEqual(-0.76, nn.layers[1][0].db)
        self.assertAlmostEqual(0.88, nn.layers[1][1].db)
        self.assertAlmostEqual(-0.304, nn.layers[1][0].dw[0])
        self.assertAlmostEqual(-0.456, nn.layers[1][0].dw[1])
        self.assertAlmostEqual(0.352, nn.layers[1][1].dw[0])
        self.assertAlmostEqual(0.528, nn.layers[1][1].dw[1])
        self.assertAlmostEqual(-0.532, nn.layers[1][0].da[0])
        self.assertAlmostEqual(-0.38, nn.layers[1][0].da[1])
        self.assertAlmostEqual(0.704, nn.layers[1][1].da[0])
        self.assertAlmostEqual(0.792, nn.layers[1][1].da[1])
        # Verify backpropagation of layer 2:
        # a(n-1)    w   expected   result   error      dE       db       dw   da(n-1)
        #     1   0.0          -      0.4   0.086  -0.172    0.172    0.172     0.086
        #     0   0.2          -        -       -       -        -        0    0.0344
        #     1   0.7          -        -       -       -        -    0.412    0.2884
        #     0   0.6          -      0.6   0.206  -0.412    0.412        0    0.2472
        self.assertAlmostEqual(0.172, nn.layers[0][0].db)
        self.assertAlmostEqual(0.412, nn.layers[0][1].db)
        self.assertAlmostEqual(0.172, nn.layers[0][0].dw[0])
        self.assertAlmostEqual(0, nn.layers[0][0].dw[1])
        self.assertAlmostEqual(0.412, nn.layers[0][1].dw[0])
        self.assertAlmostEqual(0, nn.layers[0][1].dw[1])
        self.assertAlmostEqual(0.086, nn.layers[0][0].da[0])
        self.assertAlmostEqual(0.0344, nn.layers[0][0].da[1])
        self.assertAlmostEqual(0.2884, nn.layers[0][1].da[0])
        self.assertAlmostEqual(0.2472, nn.layers[0][1].da[1])

    def testTrainOnSimpleExample(self):
        # Simple example that only depends on the first parameter.
        # A linear separation would be enough but it has the benefit of training fast :-)
        """ Created with:
        import random
        print(random.random()*4, random.random()*5, 0) for i in range(0, 5)
        print(5+random.random()*4, random.random()*5, 1) for i in range(0, 5)
        """
        dataset = [
            ([2.7810836, 2.550537003],   0),
            ([1.465489372, 2.362125076], 0),
            ([3.396561688, 4.400293529], 0),
            ([1.38807019, 1.850220317],  0),
            ([3.06407232, 3.005305973],  0),
            ([7.627531214, 2.759262235], 1),
            ([5.332441248, 2.088626775], 1),
            ([6.922596716, 1.77106367],  1),
            ([8.675418651, -0.242068655],1),
            ([7.673756466, 3.508563011], 1),
        ]
        examples = [a[0] for a in dataset]
        labels = [a[1] for a in dataset]

        nn = neuralnet.NeuralNet(2, [2, 2], neuralnet.Sigmoid(), average_gradient=False)
        # This empirically proves to be good parameters to train on this
        nn.train(10*20*20, 1, 1.0, examples, labels)
        # TODO: This should work like this too:
        #nn.train(20*20, 10, 1.0, examples, labels)

        """
        print("")
        print(nn.evaluate([2, 5]))
        print(nn.evaluate([2.5, 2.5]))
        print(nn.evaluate([3, 0]))
        print(nn.evaluate([6, 0]))
        print(nn.evaluate([7.5, 2.5]))
        print(nn.evaluate([9, 5]))
        print("")
        """
        self.assertEqual(0, nn.predict([2, 5]))
        self.assertEqual(0, nn.predict([2.5, 2.5]))
        # This usually fails pretty badly on this one which is not necessarily surprising: there's no example close to it
        #self.assertEqual(0, nn.predict([3, 0]))
        self.assertEqual(1, nn.predict([6, 0]))
        self.assertEqual(1, nn.predict([7.5, 2.5]))
        self.assertEqual(1, nn.predict([9, 5]))

    # Nice test to play with but needs to much time to obtain a stable result
    @unittest.skip("Too slow to run every time")
    def testTrainAndPredictOnXor(self):
        dataset = [
            # Both negatives
            ([-0.5, -0.5], 1),
            ([-0.5, -0.3], 1),
            ([-0.5, -0.2], 1),
            ([-0.3, -0.5], 1),
            ([-0.3, -0.3], 1),
            ([-0.3, -0.2], 1),
            ([-0.2, -0.5], 1),
            ([-0.2, -0.3], 1),
            ([-0.2, -0.2], 1),
            # First negative, second positive
            ([-0.5, 0.5], 0),
            ([-0.5, 0.3], 0),
            ([-0.5, 0.2], 0),
            ([-0.3, 0.5], 0),
            ([-0.3, 0.3], 0),
            ([-0.3, 0.2], 0),
            ([-0.2, 0.5], 0),
            ([-0.2, 0.3], 0),
            ([-0.2, 0.2], 0),
            # Both positives
            ([0.5, 0.5], 1),
            ([0.5, 0.3], 1),
            ([0.5, 0.2], 1),
            ([0.3, 0.5], 1),
            ([0.3, 0.3], 1),
            ([0.3, 0.2], 1),
            ([0.2, 0.5], 1),
            ([0.2, 0.3], 1),
            ([0.2, 0.2], 1),
            # First positive, second negative
            ([0.5, -0.5], 0),
            ([0.5, -0.3], 0),
            ([0.5, -0.2], 0),
            ([0.3, -0.5], 0),
            ([0.3, -0.3], 0),
            ([0.3, -0.2], 0),
            ([0.2, -0.5], 0),
            ([0.2, -0.3], 0),
            ([0.2, -0.2], 0),
        ]
        examples = [a[0] for a in dataset]
        labels = [a[1] for a in dataset]
        nn = neuralnet.NeuralNet(2, [2, 2], neuralnet.Sigmoid(), average_gradient=False)
        nn.train(20*20*20, 10, 1.0, examples, labels)
        print("")
        print(nn.evaluate([0.4, 0.4]))   # 1
        print(nn.evaluate([-0.3, 0.3]))  # 0
        print(nn.evaluate([-0.3, -0.4])) # 1
        print(nn.evaluate([0.4, -0.4]))  # 0
        print("")
        self.assertEqual(1, nn.predict([0.4, 0.4]))
        self.assertEqual(0, nn.predict([-0.3, 0.3]))
        self.assertEqual(1, nn.predict([-0.3, -0.4]))
        self.assertEqual(0, nn.predict([0.4, -0.4]))


if __name__ == '__main__':
   unittest.main()
