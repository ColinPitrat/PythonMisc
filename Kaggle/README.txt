# Start Jupyter notebook

Use jupyter from the python venv:

```
~/python-venv/bin/jupyter notebook
```

Or to allow external connections:

```
~/python-venv/bin/jupyter notebook --ip 0.0.0.0
```

# Setup the virtual env

```
sudo apt-get install virtualenv python3-venv
virtualenv ~/python-venv
~/python-venv/bin/pip install jupyter kaggle matplotlib numpy opencv-python pandas scikit-learn tensorflow visualkeras

# Optional: to enter the venv and use python/pip without prefixing
source ~/python-venv/bin/activate
```

# Get the data

## Titanic

```
~/python-venv/bin/kaggle competitions download -c titanic
unzip titanic.zip
rm titanic.zip gender_submission.csv
```

## MNIST

```
~/python-venv/bin/kaggle competitions download -c digit-recognizer
unzip digit-recognizer.zip
rm sample_submission.csv digit-recognizer.zip 
```

## FashionMNIST

Download archive.zip from https://www.kaggle.com/datasets/zalando-research/fashionmnist/download?datasetVersionNumber=4

```
unzip archive.zip
mv fashion-mnist_test.csv test.csv
mv fashion-mnist_train.csv train.csv
rm t10k-images-idx3-ubyte t10k-labels-idx1-ubyte train-images-idx3-ubyte train-labels-idx1-ubyte
```

## DogsVsCats

```
~/python-venv/bin/kaggle competitions download -c dogs-vs-cats
unzip dogs-vs-cats.zip
rm sampleSubmission.csv
unzip test1.zip
unzip train.zip
rm test1.zip train.zip
```

## StanfordDogs

Download archive.zip from https://www.kaggle.com/datasets/jessicali9530/stanford-dogs-dataset/download?datasetVersionNumber=2

```
unzip archive.zip
rm archive.zip
python3 create_sets.py
```
