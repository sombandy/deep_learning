#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : July 23, 2016

import json
import os
import numpy as np
import random
import cPickle as pickle

from scipy import misc, ndimage

def paste_badge(img, bdg):
    bh, bw = bdg.shape[0], bdg.shape[1]
    if img.shape[0] <= bh or img.shape[1] <= bw:
        print "Badge is bigger than the image"
        return None

    y = img.shape[0] - bh
    y = random.randint(max(0, y - 50), y)

    x = img.shape[1] - bw
    x = random.randint(0, x)

    img[y:y+bh, ][:, x:x+bw] = bdg
    return img

def get_jpg_files(file_dir):
    jpg_files = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith('.jpg'):
                jpg_files.append(os.path.join(root, file))
    return jpg_files

def load_badges(bdg_files):
    badges = []
    for f in bdg_files:
        b = ndimage.imread(f)
        badges.append(b)
    return badges

def get_image_label(config, img_file, img_h, img_w, channel, badges):
    img = ndimage.imread(img_file)

    if (len(img.shape) != 3 or img.shape[2] != channel):
        print "Number of channel is less", img.shape
        return None, None

    img = misc.imresize(img, size=(img_h, img_w))

    label = 0
    if random.random() <= config["positive_class"]:
        label = np.random.randint(len(badges)) + 1
        img = paste_badge(img, badges[label - 1])

    return img, label

def get_dataset(config):
    jpg_files = get_jpg_files(config["img_dir"])
    bdg_files = get_jpg_files(config["badge_dir"])

    print "Number of images", len(jpg_files)
    print "Number of badges", len(bdg_files)

    if len(jpg_files) <= 0 or len(bdg_files) <= 0:
        print "Not enough images or badges"
        return None, None

    badges = load_badges(bdg_files)
    file_idx = np.random.permutation(len(jpg_files))

    labels = []
    max_images = config["max_images"]
    img_w = config["img_width"]
    img_h = config["img_height"]
    channel = config["channel"]

    labels = np.ndarray(max_images, dtype=np.int32)
    dataset = np.ndarray(shape=(max_images, img_h, img_w, channel),
                         dtype=np.float32)

    i = 0
    for f in file_idx:
        if i >= max_images or i >= len(jpg_files):
            break

        img_file = jpg_files[f]
        img, label = get_image_label(config, img_file, img_h, img_w,
                                     channel, badges)

        if img is not None:
            dataset[i, :, :, :] = img
            labels[i] = label
            i += 1

    return dataset, labels

def create_pickle(config_file, pickle_file):
    config = None
    with open(config_file) as f:
        config = json.load(f)

    dataset, labels = get_dataset(config)
    if dataset is None or labels is None:
        print "No data set is created"
        return

    n = labels.shape[0]
    test_size = int(n * config["test_size"])
    valid_size = int(n * config["valid_size"])

    valid_labels = labels[:valid_size]
    valid_dataset = dataset[:valid_size,]

    idx = valid_size
    test_labels = labels[idx : idx + test_size]
    test_dataset = dataset[idx : idx + test_size,]

    idx += test_size
    train_labels = labels[idx :]
    train_dataset = dataset[idx:, ]

    try:
        f = open(pickle_file, 'wb')
        save = {
            'train_dataset': train_dataset,
            'train_labels': train_labels,
            'valid_dataset': valid_dataset,
            'valid_labels': valid_labels,
            'test_dataset': test_dataset,
            'test_labels': test_labels,
            }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise

if __name__ == '__main__':
    create_pickle('config.json', 'badged_images.pickle')
