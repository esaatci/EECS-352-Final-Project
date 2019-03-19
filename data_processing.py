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


def process_data():

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

		

	def calculate_note(data):
		'''
		returns the index of the note in the array
		'''
		result = 0
		for i,note in enumerate(data):
			if note == 1:
				result = i
				break

		return result
	
	def process_files(dir_name):
		path = "data/Nottingham/"
		files = os.listdir(path + dir_name + "/")
		processed_midi_files = []
		
		# constants
		MIN_NOTE_ = 48
		MAX_NOTE_ = 88
		MAX_TIME_ = 960
		one_hot_arr = [0 for i in range(MAX_NOTE_ - MIN_NOTE_ + 1)]

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
					note_value = msg.note
					#note_index = note_value - MIN_NOTE_
					#normalized_note_duration = np.tanh((msg.time+1) / MAX_TIME_)
					#encoding = copy.copy(one_hot_arr)
					#encoding[note_index] = 1

					#processed_midi_files.append((encoding,normalized_note_duration))
					processed_midi_files.append(note_value)

			#processed_midi_files.append((one_hot_arr,0.0))

		return processed_midi_files

	train_data = process_files("train")
	test_data = process_files("test")
	valid_data = process_files("valid")
	MIN_NOTE_ = 48
	MAX_NOTE_ = 89
	num_notes = MAX_NOTE_

	return train_data, test_data, valid_data, num_notes

def reverse_melody(note_arr):
	output_file = mido.MidiFile()
	output_track = mido.MidiTrack()

	for note in note_arr:
		on = mido.Message('note_on', note=note, velocity=64, time=1)
		off = mido.Message('note_off', note=note, velocity=0, time=959)
		output_track.append(on)
		output_track.append(off)
	
	output_file.tracks.append(output_track)
	output_file.save("test_output.mid")






if __name__ == "__main__":
	train_data , test_data, valid_data = process_data()
	print("train_data", train_data[0])
	print('=======================')
	print()
	print("test_data",test_data[0])
	print('=======================')
	print()
	print("valid_data",valid_data[0])

	











				











