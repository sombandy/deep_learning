#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : June  7, 2016
import numpy as np

IMAGE_SIZE = 28
NUM_LABELS = 10

def reformat(dataset, labels):
  dataset = dataset.reshape((-1, IMAGE_SIZE * IMAGE_SIZE)).astype(np.float32)
  # Map 2 to [0.0, 1.0, 0.0 ...], 3 to [0.0, 0.0, 1.0 ...]
  labels = (np.arange(NUM_LABELS) == labels[:,None]).astype(np.float32)
  return dataset, labels
