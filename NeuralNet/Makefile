all: get_data
	python neuralnet_test.py

get_data: data data/train-images-idx3-ubyte data/train-labels-idx1-ubyte data/t10k-images-idx3-ubyte data/t10k-labels-idx1-ubyte

data:
	mkdir -p data

data/train-images-idx3-ubyte:
	cd data && wget http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz && gunzip train-images-idx3-ubyte.gz

data/train-labels-idx1-ubyte:
	cd data && wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz && gunzip train-labels-idx1-ubyte.gz

data/t10k-images-idx3-ubyte:
	cd data && wget http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz && gunzip t10k-images-idx3-ubyte.gz

data/t10k-labels-idx1-ubyte:
	cd data && wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz && gunzip t10k-labels-idx1-ubyte.gz
