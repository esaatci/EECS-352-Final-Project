import mido
import numpy as np 

output_file = mido.MidiFile()
output_track1 = mido.MidiTrack()
output_track2 = mido.MidiTrack() 

# <meta message set_tempo tempo=500000 time=0>
# <meta message key_signature key='E' time=0>
# <meta message time_signature numerator=4 denominator=4 clocks_per_click=48 notated_32nd_notes_per_beat=8 time=0>
# <meta message track_name name='Falling About' time=0>
# <meta message end_of_track time=61465>
# output_track.append(mido.Message("set_tempo", set_tempo))



def construct_key_from_random_note(note, mode = "minor"):
	tonal = note
	major_second = note + 2
	major_third = note + 4
	perfect_four = note + 5
	perfect_fifth = note + 7 
	major_sixth = note + 9
	major_seventh =  note + 11
	perfect_octave = note + 12
	notes_in_key = [tonal, major_second, major_third, perfect_four, perfect_fifth, major_sixth, major_seventh, perfect_octave]
	if mode == "major":
		#everything stays as above
		pass
	elif mode == "minor":
		# diminished third, sixth, and seventh
		notes_in_key[2] = notes_in_key[2] - 1
		notes_in_key[5] = notes_in_key[5] - 1
		notes_in_key[6] = notes_in_key[6] - 1

	else:
		# I can print error message here instead
		print("you have entered an invalid mode, major key was constructed")

	return notes_in_key 

def construct_chords_in_key(note, mode= "minor"):
	if mode== "major":
		tonic_1 = np.asarray([note, note+4, note+7]) #major
		supertonic_2 = np.asarray([note + 2, note + 5, note+9]) #minor
		mediant_3 = supertonic_2 + 2 #minor
		subdominant_4 = tonic_1 + 5 #major
		dominant_5 = tonic_1 + 7 #major
		submediant_6 = supertonic_2 + 7 #minor
		leading_note_7 = np.asarray([note + 11, note + 14, note + 17]) #diminished

	if mode == "minor":
		tonic_1 = np.asarray([note, note+3, note+7]) #minor
		supertonic_2 = np.asarray([note + 2, note + 5, note+8]) #diminished
		mediant_3 = np.asarray([note+3, note+7, note+10]) #major
		subdominant_4 = tonic_1 + 5 #minor
		dominant_5 = tonic_1 + 7 #minor
		submediant_6 = mediant_3 + 5 #major
		leading_note_7 = mediant_3 + 7 #major



	chords_in_key = [tonic_1, supertonic_2, mediant_3, subdominant_4, dominant_5, submediant_6, leading_note_7]
	return chords_in_key




def pick_random_note_in_key(note):
	'''
	takes the tonal, returns the index of a random note in the notes_in_key array
	'''
	note_index = (int(np.random.rand() * 1000) % 8)
	return note_index

def pick_random_chord_in_key(note):
	'''
	takes the tonal, returns the index of a random chord in the chords_in_key array
	'''
	chord_index = (int(np.random.rand() * 1000) % 7)
	return chord_index



# initialize start note and construct key
start_note = int(np.random.rand() * 32) + 44
notes_in_key = construct_key_from_random_note(start_note, "minor")
#print(notes_in_minor_key)
time = 479

#meta messages such as tempo, track name, instrument, etc...
output_track1.append(mido.MetaMessage('set_tempo', tempo=600000, time=0))
output_track1.append(mido.MetaMessage('set_tempo', tempo=600000, time=0))


for _ in range(64):
	note_value = notes_in_key[pick_random_note_in_key(start_note)]
	randomize = np.random.randn()
	if randomize > 0.6:
		# add some kind of randomization here
		pass
	if _ % 8 == 0:
		note_value = notes_in_key[0]
	time_ = (int(np.random.randn() * 1000)  % 9 )
	time_ = max(int(time_) * 120- 1, 119)
	velocity_ = int((np.random.randn() * 1000) % 26) + 100
	on = mido.Message('note_on', note=note_value, velocity=velocity_, time=1)
	off = mido.Message('note_off', note=note_value, velocity=0, time=time_)

	output_track1.append(on)
	output_track1.append(off)


chords_in_key = construct_chords_in_key(start_note-12, "minor") #lower harmony
chord_length = 1919 #fixed chord length for now
velocity_ = 100 #fixed chord velocity for now
for _ in range(16):
	chord_value = chords_in_key[pick_random_chord_in_key(start_note)]
	if _ % 8 == 0:
		chord_value = chords_in_key[0]
	note1 = chord_value[0]
	note2 = chord_value[1]
	note3 = chord_value[2]
	on1 = mido.Message('note_on', note=note1, velocity=velocity_, time=1)
	on2 = mido.Message('note_on', note=note2, velocity=velocity_, time=0)
	on3 = mido.Message('note_on', note=note3, velocity=velocity_, time=0)
	off1 = mido.Message('note_off', note=note1, velocity=0, time=chord_length)
	off2 = mido.Message('note_off', note=note2, velocity=0, time= 0)
	off3 = mido.Message('note_off', note=note3, velocity=0, time= 0)

	output_track2.append(on1)
	output_track2.append(on2)
	output_track2.append(on3)
	output_track2.append(off1)
	output_track2.append(off2)
	output_track2.append(off3)

	

'''
random_notes = (np.random.rand(64) * 41) + 40
random_notes = [int(random_notes[i]) for i in range(len(random_notes))]
print(random_notes)
time = 479
for note in random_notes:
	note_value = note
	time_ = (int(np.random.randn() * 1000)  % 17 )
	time_ = max(int(time_) * 60- 1, 119)
	print(time_)
	velocity_ = int((np.random.randn() * 1000) % 26) + 100
	on = mido.Message('note_on', note=note_value, velocity=velocity_, time=1)
	off = mido.Message('note_off', note=note_value, velocity=0, time=time_)
	
	output_track1.append(on)
	output_track1.append(off)

for i,note in enumerate(random_notes):
	note = random_notes[i % 9]
	note_value = note - 24
	time_ = (int(np.random.randn() * 1000) % 17 )
	time_ = max(int(time_) * 60- 1, 239)
	print(time_)
	on = mido.Message('note_on', note=note_value, velocity=120, time=1)
	off = mido.Message('note_off', note=note_value, velocity=0, time=time_)
	
	output_track2.append(on)
	output_track2.append(off)
'''


print("ARDA'S SONG'S MIDI REPRESENTATION")
print("=========================================================================")
print(output_track1)
print(output_track2)
print("=========================================================================")



output_file.tracks.append(output_track1)
output_file.tracks.append(output_track2)

output_file.save("arda-test.mid")

print("reconstruted track")
print("=========================================================================")
# Prints the reconstruted track
for i, track in enumerate(output_file.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)








