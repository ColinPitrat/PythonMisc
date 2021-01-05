The following initialization of weights and bias led to bad result no matter the activation function:

```
self.weights = [random.uniform(0, 1) for i in range(0, nb_inputs)]
self.bias = random.uniform(0, 1)
```

The following initialization of weights and bias led to good results with Sigmoid, medium results with TanH but still bad results with ReLu:

```
self.weights = [random.uniform(-1, 1) for i in range(0, nb_inputs)]
self.bias = random.uniform(-1, 1)
```

The following led to better result with ReLu, although still not great:

```
self.weights = [random.uniform(-1, 1)/math.sqrt(nb_inputs) for i in range(0, nb_inputs)]
self.bias = random.uniform(-1, 1)
```

From https://zhenye-na.github.io/2018/09/09/build-neural-network-with-mnist-from-scratch.html:
```
The outputs from a randomly initialized neuron has a variance that grows with the number of inputs. It turns out that we can normalize the variance of each neuron’s output to 1 by scaling its weight vector by the square root of its fan-in (i.e. its number of inputs). That is, the recommended heuristic is to initialize each neuron’s weight vector as: w = np.random.randn(n) / sqrt(n), where n is the number of its inputs. This ensures that all neurons in the network initially have approximately the same output distribution and empirically improves the rate of convergence.
```



Still, ReLu was capped at 0.34 (34%).
Thinking this would help too, I tried normalizing the input between [-1, 1] instead of [0, 1] but it actually stucked the network progression.
