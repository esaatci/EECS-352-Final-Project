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
import pickle
import matplotlib.pyplot as plt


os.environ['KMP_DUPLICATE_LIB_OK']='True'

data_path = "model_time_data"


# Load the data
def train_time():
	train_data, test_data, valid_data, num_times,id_to_time = process_data("time")

	num_steps = 10
	batch_size = 5

	train_data_generator = KerasBatchGenerator(train_data, num_steps, batch_size, num_times,
	                                           skip_step=num_steps)
	valid_data_generator = KerasBatchGenerator(valid_data, num_steps, batch_size, num_times,
	                                           skip_step=num_steps)

	hidden_size = num_times
	use_dropout=True
	model = Sequential()
	model.add(Embedding(num_times, hidden_size, input_length=num_steps))
	model.add(LSTM(hidden_size, return_sequences=True))
	model.add(LSTM(hidden_size, return_sequences=True))

	if use_dropout:
	    model.add(Dropout(0.5))
	model.add(TimeDistributed(Dense(num_times)))
	model.add(Activation('softmax'))

	optimizer = Adam()
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

	print(model.summary())

	checkpointer = ModelCheckpoint(filepath=data_path + '/model-{epoch:02d}.hdf5', verbose=1)
	num_epochs = 50

	history_time = model.fit_generator(train_data_generator.generate(), len(train_data)//(batch_size*num_steps), num_epochs,
	                    validation_data=valid_data_generator.generate(),
	                    validation_steps=len(valid_data)//(batch_size*num_steps), callbacks=[checkpointer])

	model.save(data_path + "/" + "note_final_model.hdf5")

	return history_time


if __name__ == "__main__":
	history = train_time()
	with open('./train_time', 'wb') as file_pi:
		pickle.dump(history.history, file_pi)


	


