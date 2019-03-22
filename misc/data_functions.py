from __future__ import print_function
import collections
import os
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Embedding, Dropout, TimeDistributed
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
import numpy as np
import argparse

"""To run this code, you'll need to first download and extract the text dataset
    from here: http://www.fit.vutbr.cz/~imikolov/rnnlm/simple-examples.tgz. Change the
    data_path variable below to your local exraction path"""

os.environ['KMP_DUPLICATE_LIB_OK']='True'
data_path = "/Users/ardagenc/Desktop/eecs352/adventures-in-ml-code/simple-examples/data_modified"

# parser = argparse.ArgumentParser()
# parser.add_argument('run_opt', type=int, default=1, help='An integer: 1 to train, 2 to test')
# parser.add_argument('--data_path', type=str, default=data_path, help='The full path of the training data')
# args = parser.parse_args()
# if args.data_path:
#     data_path = args.data_path


def read_words(filename):
    with tf.gfile.GFile(filename, "r") as f:
        return f.read().replace("\n", "<eos>").split()


def build_vocab(filename):
    data = read_words(filename)
    print("data", data[0])
    counter = collections.Counter(data)
    print("counter", counter[0])
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    # print(count_pairs)
    words, _ = list(zip(*count_pairs))

    word_to_id = dict(zip(words, range(len(words))))

    return word_to_id


def file_to_word_ids(filename, word_to_id):
    data = read_words(filename)
    return [word_to_id[word] for word in data if word in word_to_id]


if __name__ == "__main__":
    test_file = "ptb.valid.txt"
    word_to_id = build_vocab(test_file)

