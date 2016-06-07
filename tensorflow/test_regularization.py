#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : June  7, 2016
import pprint
from six.moves import cPickle as pickle
import data_prep_notminst as dp
import logistic_regression as lr
import one_hidden_layer_nn as hnn

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

    train_dataset, train_labels = dp.reformat(train_dataset, train_labels)
    valid_dataset, valid_labels = dp.reformat(valid_dataset, valid_labels)
    test_dataset, test_labels = dp.reformat(test_dataset, test_labels)
    print('Training set', train_dataset.shape, train_labels.shape)
    print('Validation set', valid_dataset.shape, valid_labels.shape)
    print('Test set', test_dataset.shape, test_labels.shape)

    # Subsample the training data
    sample_size = 500
    small_train = train_dataset[:sample_size, ]
    small_labels = train_labels[:sample_size, ]

    results = {}
    test_model = hnn.OneHiddenLayerNN
    with test_model() as model:
        model.train(small_train, small_labels, valid_dataset, valid_labels)
        results["no_reg_train"] = model.evaluate(small_train, small_labels)
        results["no_reg_test"] = model.evaluate(test_dataset, test_labels)

    for l2 in [1e-1, 1e-2, 1e-3, 1e-4]:
        tag = "%0.0e_l2_reg_" % l2
        with test_model(l2=l2) as model:
            model.train(small_train, small_labels, valid_dataset, valid_labels)
            results[tag + "train"] = model.evaluate(
                small_train, small_labels)
            results[tag + "test"] = model.evaluate(
                test_dataset, test_labels)

    for kp in [0.9, 0.7, 0.5, 0.3]:
        tag = "%0.1f_kp_reg_" % kp
        with test_model(keep_prob = kp) as model:
            model.train(small_train, small_labels, valid_dataset, valid_labels)
            results[tag + "train"] = model.evaluate(
                small_train, small_labels)
            results[tag + "test"] = model.evaluate(
                test_dataset, test_labels)

    pprint.pprint(results)

if __name__ == '__main__':
    main()
