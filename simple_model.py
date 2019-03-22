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
from data_processing import process_data,reverse_melody
import random


os.environ['KMP_DUPLICATE_LIB_OK']='True'
data_path = "model_data"

parser = argparse.ArgumentParser()
parser.add_argument('run_opt', type=int, default=1, help='An integer: 1 to train, 2 to generate music')
parser.add_argument('--data_path', type=str, default=data_path, help='The full path of the training data')
args = parser.parse_args()
if args.data_path:
    data_path = args.data_path

train_data, test_data, valid_data, num_notes = process_data()

train_set = set(train_data)

valid_data = [data for data in valid_data if data in train_set]
test_data = [data for data in test_data if data in train_set]

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

num_steps = 10
batch_size = 30
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
    dummy_iters = random.randint(40,100)

    example_test_generator = KerasBatchGenerator(test_data, num_steps, 1, num_notes,
                                                     skip_step=1)
    
    for i in range(dummy_iters):
        dummy = next(example_test_generator.generate())
    num_predict = 32
    note_arr = []
    for i in range(num_predict):
        data = next(example_test_generator.generate())
        len_data = len(data)
        rand_index = random.randint(0,len_data-1)
        prediction = model.predict(data[0])
        predict_note = np.argmax(prediction[:, num_steps - 1, :])
        note_arr.append(predict_note)

    reverse_melody(note_arr)






