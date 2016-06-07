#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : June  6, 2016

"""
 This file contains the main function to test accuracy
 on the onMINST dataset
 (http://yaroslavvb.blogspot.com/2011/09/notmnist-dataset.html).

 You first need to first create the 'notMNIST.pickle' as shown in
 https://github.com/tensorflow/tensorflow/blob/r0.9/tensorflow/examples/udacity/1_notmnist.ipynb
"""
import numpy as np
import time
from six.moves import cPickle as pickle
import logistic_regression as lr
import one_hidden_layer_nn as hnn

IMAGE_SIZE = 28
NUM_LABELS = 10

def reformat(dataset, labels):
  dataset = dataset.reshape((-1, IMAGE_SIZE * IMAGE_SIZE)).astype(np.float32)
  # Map 2 to [0.0, 1.0, 0.0 ...], 3 to [0.0, 0.0, 1.0 ...]
  labels = (np.arange(NUM_LABELS) == labels[:,None]).astype(np.float32)
  return dataset, labels

def main():
    pickle_file = 'notMNIST.pickle'

    with open(pickle_file, 'rb') as f:
        save = pickle.load(f)
        train_dataset = save['train_dataset']
        train_labels = save['train_labels']
        valid_dataset = save['valid_dataset']
        valid_labels = save['valid_labels']
        test_dataset = save['test_dataset']
        test_labels = save['test_labels']
        del save  # hint to help gc free up memory
        print('Training set', train_dataset.shape, train_labels.shape)
        print('Validation set', valid_dataset.shape, valid_labels.shape)
        print('Test set', test_dataset.shape, test_labels.shape)

    train_dataset, train_labels = reformat(train_dataset, train_labels)
    valid_dataset, valid_labels = reformat(valid_dataset, valid_labels)
    test_dataset, test_labels = reformat(test_dataset, test_labels)
    print('Training set', train_dataset.shape, train_labels.shape)
    print('Validation set', valid_dataset.shape, valid_labels.shape)
    print('Test set', test_dataset.shape, test_labels.shape)


    lr_acc = 0
    hnn_acc = 0
    lr_time = 0
    hnn_time = 0
    with lr.LogisticRegression() as model:
        print "Training 1-unit LogisticRegression"
        start_time = time.time()
        model.train(train_dataset, train_labels, valid_dataset, valid_labels)
        lr_time = time.time() - start_time
        lr_acc = model.evaluate(test_dataset, test_labels)

    with hnn.OneHiddenLayerNN() as model:
        print "Training Nueral Network with 1 Hidden layer"
        start_time = time.time()
        model.train(train_dataset, train_labels, valid_dataset, valid_labels)
        hnn_time = time.time() - start_time
        hnn_acc = model.evaluate(test_dataset, test_labels)

    print "\n==== Training Time ===="
    print "LogisticRegression = %d sec" % lr_time
    print "NN with 1 hidden layer = %d sec" % hnn_time

    print "\n==== Accuracy on test data ===="
    print "LogisticRegression = %4.2f" % lr_acc
    print "NN with 1 hidden layer = %4.2f" % hnn_acc

if __name__ == '__main__':
    main()
