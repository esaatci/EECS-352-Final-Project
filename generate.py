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
from data_processing import *
from batch_generator import KerasBatchGenerator
import random


os.environ['KMP_DUPLICATE_LIB_OK']='True'
train_data_note,test_data_note,valid_data_note,num_notes,MIN_NOTE_ = process_data("note")
train_data_time,test_data_time,valid_data_time,num_times,id_to_time = process_data("time")

num_steps = 10
batch_size = 30

# Load note Values
note_data_path = "model_note_data"
model = load_model(note_data_path + "/model-10.hdf5")
example_note_generator = KerasBatchGenerator(test_data_note, num_steps, 1, num_notes,
                                                 skip_step=1)
# Load time Values
time_data_path = "model_time_data"
model = load_model(time_data_path + "/model-13.hdf5")
example_time_generator = KerasBatchGenerator(test_data_time, num_steps, 1, num_times,
                                                 skip_step=1)



dummy_iters = random.randint(40,100)
for i in range(dummy_iters):
    arda = next(example_note_generator.generate())
    efe = next(example_time_generator.generate())

num_predict = 32
note_arr = []
time_arr = []

for i in range(num_predict):
    data_note = next(example_note_generator.generate())
    prediction_note = model.predict(data_note[0])
    predict_note = np.argmax(prediction_note[:, num_steps - 1, :])
    note_arr.append(predict_note)

    data_time = next(example_time_generator.generate())
    prediction_time= model.predict(data_time[0])
    predict_time = np.argmax(prediction_time[:, num_steps - 1, :])
    time_arr.append(predict_time)



note_arr = reverse_melody(note_arr,MIN_NOTE_)
time_arr = [id_to_time[time_] for time_ in time_arr]

write_midi(note_arr,time_arr)






