#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : June  6, 2016

import tensorflow as tf
import tf_nn_base as nb

class OneHiddenLayerNN(nb.TFNNBase):
    """Neural Network with on hidden layer

    Neural Network with on hidden layer of relu units
    """
    def __init__(self, num_hidden_units=1024, l2=1e-3, keep_prob=1.0):
        self.num_hidden_units = num_hidden_units
        super(OneHiddenLayerNN, self).__init__(l2, keep_prob)

    def feed_forward(self, tf_dataset):
        layer1_output = tf.nn.relu(
            tf.matmul(tf_dataset, self.weights1) + self.biases1)
        layer2_output = tf.nn.softmax(
            tf.matmul(layer1_output, self.weights2) + self.biases2)
        return layer2_output

    def get_logits(self, tf_dataset):
        layer1_output = tf.nn.relu(
            tf.matmul(tf_dataset, self.dropout_weights1) + self.biases1)
        return tf.matmul(layer1_output, self.dropout_weights2) + self.biases2

    def l2_loss(self):
        return tf.nn.l2_loss(self.weights1) + tf.nn.l2_loss(self.weights2)

    def init_nn(self, num_features, num_labels, batch_sizes):
        # Layer1 parameters
        self.weights1 = tf.Variable(
            tf.truncated_normal([num_features, self.num_hidden_units]))
        self.biases1 = tf.Variable(tf.zeros([self.num_hidden_units]))

        # Layer2 parameters
        self.weights2 = tf.Variable(
            tf.truncated_normal([self.num_hidden_units, num_labels]))
        self.biases2 = tf.Variable(tf.zeros([num_labels]))

        if self.keep_prob < 0.99:
            self.dropout_weights1 = tf.nn.dropout(self.weights1, self.keep_prob)
            self.dropout_weights2 = tf.nn.dropout(self.weights2, self.keep_prob)
        else:
            self.dropout_weights1 = self.weights1
            self.dropout_weights2 = self.weights2

        self.train_output = self.feed_forward(self.train_dataset)
