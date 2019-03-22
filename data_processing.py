import mido
import copy
import os
import numpy as np
'''
ERRATA
Data Strip 
	Time Signauture 4/4
	number of tracks (contains melody )

Reduce the number of vector indices
	Find max and min notes
	map them to the array
	map them back to their normal values

transpose to C major
'''


def process_data(data_choice):

	def transpose(key):
		"""returns the transpose offset given a key"""
		
		key_arr_major_sharp = ["C" , "C#", "D", "D#", "E", "F", "F#", "G" ,"G#", "A" , "A#", "B"]
		key_arr_major_flat = ["C" , "Db","D", "Eb", "E", "F", "Gb", "G" ,"Ab", "A" , "Bb", "B"]
		key_arr_minor_sharp = ["A" , "A#", "B","C" , "C#","D", "D#", "E", "F", "F#", "G" ,"G#"]
		
		
		if len(key) != 1:
			if key[1] == "#":
				return key_arr_major_sharp.index(key)
			if key[1] == "b":
				return key_arr_major_flat.index(key)
			if key[1] == "m":
				return key_arr_minor_sharp.index(key[0])	
		else:
			return key_arr_major_sharp.index(key)
	
	def process_files(dir_name):
		path = "data/Nottingham/"
		files = os.listdir(path + dir_name + "/")
		processed_midi_files = []
		
		# constants
		MIN_NOTE_ = 48
		MAX_NOTE_ = 88
		MAX_TIME_ = 960
		one_hot_arr = [0 for i in range(MAX_NOTE_ - MIN_NOTE_ + 1)]
		transpose_offset = 0

		for file in files:
			midi_load = mido.MidiFile(path + dir_name + "/" + file)

			if len(midi_load.tracks) < 3:
				continue

			time_signature = midi_load.tracks[0][2].numerator
			key_signature = midi_load.tracks[0][1].key

			if time_signature != 4:
				continue

			if key_signature != "C":
				transpose_offset = transpose(key_signature)

			for msg in midi_load.tracks[1]:
				if msg.type == "note_off":
					note_value = msg.note - transpose_offset
					time_value = msg.time
					processed_midi_files.append((note_value,time_value))

		return processed_midi_files

	

	
	MIN_NOTE_ = 48
	MAX_NOTE_ = 89

	
	

	if data_choice == "note":
		train_data_note = [data[0] - MIN_NOTE_ for data in process_files("train")]
		test_data_note = [data[0] - MIN_NOTE_ for data in process_files("test")]
		valid_data_note = [data[0] - MIN_NOTE_ for data in process_files("valid")]
		train_set_note = set(train_data_note)
		valid_data_note = [data for data in valid_data_note if data in train_set_note]
		test_data_note = [data  for data in test_data_note if data in train_set_note]
		num_notes = MAX_NOTE_
		return train_data_note,test_data_note,valid_data_note,num_notes,MIN_NOTE_

	elif data_choice == "time":
		train_data_time = [data[1] for data in process_files("train")]
		test_data_time = [data[1] for data in process_files("test")]
		valid_data_time = [data[1] for data in process_files("valid")]
		train_set_time = set(train_data_time)
		valid_data_time = [data for data in valid_data_time if data in train_set_time]
		test_data_time = [data for data in test_data_time if data in train_set_time]
		time_to_id = dict(zip(set(train_data_time), range(len(set(train_data_time)))))
		num_times = max(time_to_id.values()) + 1 
		
		train_data_time = [time_to_id[time] for time in train_data_time] 
		valid_data_time = [time_to_id[time] for time in valid_data_time]
		test_data_time = [time_to_id[time] for time in test_data_time]   
		id_to_time = reverse_time(time_to_id)
		return train_data_time,test_data_time,valid_data_time,num_times,id_to_time
	else:
		return Exception

	


def reverse_melody(note_arr,MIN_NOTE_):
	return [note + MIN_NOTE_ for note in note_arr]

def reverse_time(time_to_id):
	id_to_time = dict(zip(time_to_id.values(), time_to_id.keys()))
	return id_to_time

def write_midi(note_arr, time_arr):
	output_file = mido.MidiFile()
	output_track = mido.MidiTrack()

	for i,note in enumerate(note_arr):
		on = mido.Message('note_on', note=note, velocity=64, time=1)
		off = mido.Message('note_off', note=note, velocity=0, time=time_arr[i])
		output_track.append(on)
		output_track.append(off)
	
	output_file.tracks.append(output_track)
	output_file.save("test_output.mid")







if __name__ == "__main__":
	train_data_time,test_data_time,valid_data_time,num_times,id_to_time = process_data("time")

	print(train_data_time[20:30])
	print(id_to_time)
	print(max(test_data_time))



	
	











				











