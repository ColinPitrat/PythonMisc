all: get_data
	python main.py

get_data: mnist_data fashion_mnist_data

mnist_data: data/mnist data/mnist/train-images-idx3-ubyte data/mnist/train-labels-idx1-ubyte data/mnist/t10k-images-idx3-ubyte data/mnist/t10k-labels-idx1-ubyte
fashion_mnist_data: data data/fashion_mnist/train-images-idx3-ubyte data/fashion_mnist/train-labels-idx1-ubyte data/fashion_mnist/t10k-images-idx3-ubyte data/fashion_mnist/t10k-labels-idx1-ubyte

data: data/mnist data/fashion_mnist
  
data/mnist:
	mkdir -p data/mnist/

data/fashion_mnist:
	mkdir -p data/fashion_mnist/

data/mnist/train-images-idx3-ubyte:
	cd data/mnist && wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz && gunzip train-images-idx3-ubyte.gz

data/mnist/train-labels-idx1-ubyte:
	cd data/mnist && wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz && gunzip train-labels-idx1-ubyte.gz

data/mnist/t10k-images-idx3-ubyte:
	cd data/mnist && wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz && gunzip t10k-images-idx3-ubyte.gz

data/mnist/t10k-labels-idx1-ubyte:
	cd data/mnist && wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz && gunzip t10k-labels-idx1-ubyte.gz

data/fashion_mnist/train-images-idx3-ubyte:
	cd data/fashion_mnist && wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz && gunzip train-images-idx3-ubyte.gz

data/fashion_mnist/train-labels-idx1-ubyte:
	cd data/fashion_mnist && wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-labels-idx1-ubyte.gz && gunzip train-labels-idx1-ubyte.gz

data/fashion_mnist/t10k-images-idx3-ubyte:
	cd data/fashion_mnist && wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-images-idx3-ubyte.gz && gunzip t10k-images-idx3-ubyte.gz

data/fashion_mnist/t10k-labels-idx1-ubyte:
	cd data/fashion_mnist && wget http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/t10k-labels-idx1-ubyte.gz && gunzip t10k-labels-idx1-ubyte.gz

