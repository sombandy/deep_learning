#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : June  6, 2016

import tensorflow as tf
import tf_nn_base as nb

class LogisticRegression(nb.TFNNBase):
    """Single Layer Nueral Network

    Logistic Regression is basically a single layer Neural Netowork with
    one output unit and Softmax activation function
    """
    def feed_forward(self, tf_dataset):
        return tf.nn.softmax(tf.matmul(tf_dataset, self.weights) + self.biases)

    def get_logits(self, tf_dataset):
        return (tf.matmul(tf_dataset, self.weights) + self.biases)

    def l2_loss(self):
        return tf.nn.l2_loss(self.weights)

    def init_nn(self, num_features, num_labels, batch_size):
        self.weights = tf.Variable(
            tf.truncated_normal([num_features, num_labels]))
        self.biases = tf.Variable(tf.zeros([num_labels]))

        self.train_output = self.feed_forward(self.train_dataset)
