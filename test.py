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
from batch_generator import KerasBatchGenerator
import random


os.environ['KMP_DUPLICATE_LIB_OK']='True'
train_data, test_data, valid_data, num_notes = process_data()
num_steps = 10
batch_size = 30


data_path = "model_data"
model = load_model(data_path + "/model-40.hdf5")
example_test_generator = KerasBatchGenerator(test_data, num_steps, 1, num_notes,
                                                 skip_step=1)
dummy_iters = random.randint(40,100)
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






