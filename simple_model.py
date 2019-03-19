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
from data_processing import process_data

"""To run this code, you'll need to first download and extract the text dataset
    from here: http://www.fit.vutbr.cz/~imikolov/rnnlm/simple-examples.tgz. Change the
    data_path variable below to your local exraction path"""

os.environ['KMP_DUPLICATE_LIB_OK']='True'
data_path = "/Users/ardagenc/Desktop/eecs352/adventures-in-ml-code/simple-examples/data_modified"

parser = argparse.ArgumentParser()
parser.add_argument('run_opt', type=int, default=1, help='An integer: 1 to train, 2 to test')
parser.add_argument('--data_path', type=str, default=data_path, help='The full path of the training data')
args = parser.parse_args()
if args.data_path:
    data_path = args.data_path


# def read_words(filename):
'''reads text from file and returns an array of words '''
#     with tf.gfile.GFile(filename, "r") as f:
#         return f.read().replace("\n", "<eos>").split()


# def build_vocab(filename):
'''sorts words in decreasing frequency, returns a dictionary that assigns each word to a unique id based on how often it is used '''
#     data = read_words(filename)

#     counter = collections.Counter(data)
#     count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

#     words, _ = list(zip(*count_pairs))
#     word_to_id = dict(zip(words, range(len(words))))

#     return word_to_id


# def file_to_word_ids(filename, word_to_id):
'''returns a list of word ids for each word that is in our num_notes list'''
#     data = read_words(filename)
#     return [word_to_id[word] for word in data if word in word_to_id]


# def load_data():
''' loads training, testing, and validation data, creates a reverse dictionary that maps word id s to words'''
#     # get the data paths
#     train_path = os.path.join(data_path, "ptb.train.txt")
#     valid_path = os.path.join(data_path, "ptb.valid.txt")
#     test_path = os.path.join(data_path, "ptb.test.txt")

#     # build the complete num_notes, then convert text data to list of integers
#     word_to_id = build_vocab(train_path)
#     train_data = file_to_word_ids(train_path, word_to_id)
#     valid_data = file_to_word_ids(valid_path, word_to_id)
#     test_data = file_to_word_ids(test_path, word_to_id)
#     num_notes = len(word_to_id)
#     reversed_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))

#     print(train_data[:5])
#     print(word_to_id)
#     print(num_notes)
#     print(" ".join([reversed_dictionary[x] for x in train_data[:10]]))
#     return train_data, valid_data, test_data, num_notes, reversed_dictionary

# train_data, valid_data, test_data, num_notes, reversed_dictionary = load_data()

train_data, test_data, valid_data, num_notes = process_data()

class KerasBatchGenerator(object):

    def __init__(self, data, num_steps, batch_size, num_notes, skip_step=5):
        #train, test, or valid data, output of process_data()
        self.data = data
        #number of notes model will learn from, number of notes we will input at each step
        self.num_steps = num_steps
        #how many notes will each batch consist of? make each song a batch?
        self.batch_size = batch_size
        #number of unique notes used
        self.num_notes = num_notes
        # this will track the progress of the batches sequentially through the
        # data set - once the data reaches the end of the data set it will reset
        # back to zero
        self.current_idx = 0
        # skip_step is the number of words which will be skipped before the next
        # batch is skimmed from the data set
        self.skip_step = skip_step

    def generate(self):
        x = np.zeros((self.batch_size, self.num_steps))
        y = np.zeros((self.batch_size, self.num_steps, self.num_notes))
        while True:
            for i in range(self.batch_size):
                if self.current_idx + self.num_steps >= len(self.data):
                    # reset the index back to the start of the data set
                    self.current_idx = 0
                x[i, :] = self.data[self.current_idx:self.current_idx + self.num_steps]
                temp_y = self.data[self.current_idx + 1:self.current_idx + self.num_steps + 1]
                # convert all of temp_y into a one hot representation
                y[i, :, :] = to_categorical(temp_y, num_classes=self.num_notes)
                self.current_idx += self.skip_step
            yield x, y

num_steps = 30
batch_size = 20
train_data_generator = KerasBatchGenerator(train_data, num_steps, batch_size, num_notes,
                                           skip_step=num_steps)
valid_data_generator = KerasBatchGenerator(valid_data, num_steps, batch_size, num_notes,
                                           skip_step=num_steps)

hidden_size = num_notes
use_dropout=True
model = Sequential()
model.add(Embedding(num_notes, hidden_size, input_length=num_steps))
model.add(LSTM(hidden_size, return_sequences=True))
model.add(LSTM(hidden_size, return_sequences=True))
if use_dropout:
    model.add(Dropout(0.5))
model.add(TimeDistributed(Dense(num_notes)))
model.add(Activation('softmax'))

optimizer = Adam()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

print(model.summary())
checkpointer = ModelCheckpoint(filepath=data_path + '/model-{epoch:02d}.hdf5', verbose=1)
num_epochs = 50
if args.run_opt == 1:
    model.fit_generator(train_data_generator.generate(), len(train_data)//(batch_size*num_steps), num_epochs,
                        validation_data=valid_data_generator.generate(),
                        validation_steps=len(valid_data)//(batch_size*num_steps), callbacks=[checkpointer])
    model.save(data_path + "final_model.hdf5")
elif args.run_opt == 2:
    model = load_model(data_path + "/model-40.hdf5")
    dummy_iters = 40
    example_training_generator = KerasBatchGenerator(train_data, num_steps, 1, num_notes,
                                                     skip_step=1)
    print("Training data:")
    for i in range(dummy_iters):
        dummy = next(example_training_generator.generate())
    num_predict = 10
    true_print_out = "Actual words: "
    pred_print_out = "Predicted words: "
    for i in range(num_predict):
        data = next(example_training_generator.generate())
        prediction = model.predict(data[0])
        predict_word = np.argmax(prediction[:, num_steps-1, :])
        true_print_out += reversed_dictionary[train_data[num_steps + dummy_iters + i]] + " "
        pred_print_out += reversed_dictionary[predict_word] + " "
    print(true_print_out)
    print(pred_print_out)
    # test data set
    dummy_iters = 40
    example_test_generator = KerasBatchGenerator(test_data, num_steps, 1, num_notes,
                                                     skip_step=1)
    print("Test data:")
    for i in range(dummy_iters):
        dummy = next(example_test_generator.generate())
    num_predict = 10
    true_print_out = "Actual words: "
    pred_print_out = "Predicted words: "
    for i in range(num_predict):
        data = next(example_test_generator.generate())
        prediction = model.predict(data[0])
        predict_word = np.argmax(prediction[:, num_steps - 1, :])
        true_print_out += reversed_dictionary[test_data[num_steps + dummy_iters + i]] + " "
        pred_print_out += reversed_dictionary[predict_word] + " "
    print(true_print_out)
    print(pred_print_out)





