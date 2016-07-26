#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : July 24, 2016

import cPickle as pickle
import numpy as np
import sys

def main():
    if len(sys.argv) < 2:
        print "Usage: analyze_dataset pickle_file"
        return

    datasets = None
    with open(sys.argv[1]) as f:
        datasets = pickle.load(f)

    if datasets is None:
        return

    data_types = ["train", "valid", "test"]

    print "Sizes:"
    for t in data_types:
        print t, datasets[t + "_labels"].shape[0]

    print "Class labels:"
    for t in data_types:
        print t, np.bincount(datasets[t + "_labels"])

if __name__ == "__main__":
    main()
