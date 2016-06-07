#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : June  6, 2016

import numpy as np
import tensorflow as tf

def accuracy(predictions, labels):
    return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
            / predictions.shape[0])

class TFNNBase(object):
    """ Base class for Neural Network
    """
    def __enter__(self):
        print "Creating Session"
        self.sess = tf.Session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print exc_type, exc_value, traceback
            return False

        print "Releasing Session"
        self.sess.close()

    def evaluate(self, dataset, labels):
        tf_predictions = self.feed_forward(dataset)
        predictions = tf_predictions.eval(session = self.sess)
        return accuracy(predictions, labels)

    def feed_forward(self, dataset):
        pass

    def l2_loss(self):
        return 0

    def loss(self, l2=1e-3):
        ce_loss = tf.nn.softmax_cross_entropy_with_logits(
            self.get_logits(self.train_dataset),
            self.train_labels
        )
        loss = ce_loss + l2 * self.l2_loss()
        return tf.reduce_mean(loss)

    def train(self, train_dataset, train_labels,
              valid_dataset = None, valid_labels=None, batch_size=128):
        num_features = train_dataset.shape[1]
        num_labels = train_labels.shape[1]

        # Training data place holders
        self.train_dataset = tf.placeholder(
            tf.float32, shape=(batch_size, num_features))
        self.train_labels = tf.placeholder(
            tf.float32,
            shape=(batch_size, num_labels)
        )

        # Construct the Nerual Network
        self.init_nn(num_features, num_labels, batch_size)

        # Set optimizer
        loss = self.loss()
        optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

        # Start the Session
        self.sess.run(tf.initialize_all_variables())

        if valid_dataset.size:
            valid_prediction = self.feed_forward(valid_dataset)

        num_steps = 2001
        for step in range(num_steps):
            # Pick an offset within the training data
            # Note: it assumes that the training data is randomized
            offset = (step * batch_size) % (train_labels.shape[0] - batch_size)

            # Generate a minibatch.
            batch_data = train_dataset[offset:(offset + batch_size), :]
            batch_labels = train_labels[offset:(offset + batch_size), :]

            feed_dict = {
                self.train_dataset : batch_data,
                self.train_labels : batch_labels
            }

            _, l, predictions = self.sess.run(
                [optimizer, loss, self.train_output],
                feed_dict=feed_dict
            )

            if (step % 500 == 0 and valid_dataset.size):
                print("Minibatch loss at step %d: %f" % (step, l))
                print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
                print("Validation accuracy: %.1f%%" % accuracy(
                        valid_prediction.eval(session=self.sess), valid_labels))
