import mido
import copy
import os
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

	# load the path of the train_files
	train_files = os.listdir("data/Nottingham/train/")

	# array to store the loaded midi files
	processed_midi_files = []
	further_processing = []


	max_note = 0
	min_note = 1000
	note_set = set()
	notes = [48,50,52,53,55,57,59,60,62,64,65,67,69,71,72,74,76,77,79,81,83,84,86]
	one_hot_arr = [0 for i in range(41)]

	for file in train_files:
		midi_load = mido.MidiFile("data/Nottingham/train/" + "/" + file)
		temp_data_arr = []
		
		if len(midi_load.tracks) < 3:
			further_processing.append(midi_load)
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
				note_set.add(note_value)
				note_index = note_value - 48
				normalized_note_duration = float(msg.time + 1) / 960
				encoding = copy.copy(one_hot_arr)
				encoding[note_index] = 1

				processed_midi_files.append((encoding,normalized_note_duration))

		processed_midi_files.append((one_hot_arr,0.0))



	return processed_midi_files
	











				











