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


def pick_random_note_in_key(note):
	'''
	takes the tonal, returns the index of a random note in the notes_in_key array
	'''
	note_index = (int(np.random.rand() * 1000) % 8)
	return note_index



# initialize start note and construct key
start_note = int(np.random.rand() * 32) + 44
notes_in_key = construct_key_from_random_note(start_note, "minor")
#print(notes_in_minor_key)
time = 479

#meta messages such as tempo, track name, instrument, etc...
output_track1.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))


for _ in range(128):
	note_value = notes_in_key[pick_random_note_in_key(start_note)]
	if _ % 8 == 0:
		note_value = notes_in_key[0]
	randomize = int(np.random.rand())
	if randomize > 0.7:
		time_ = (int(np.random.randn() * 1000)  % 8 )
	elif randomize <= 0.7:
		time_ = (int(np.random.randn() * 1000)  % 6 )
	time_ = max(int(time_) * 120- 1, 119)
	on = mido.Message('note_on', note=note_value, velocity=64, time=1)
	off = mido.Message('note_off', note=note_value, velocity=0, time=time_)

	output_track1.append(on)
	output_track1.append(off)




print("INKEY MIDI REPRESENTATION")
print("=========================================================================")
print(output_track1)
print("=========================================================================")



output_file.tracks.append(output_track1)

output_file.save("inKey-output5.mid")

print("reconstruted track")
print("=========================================================================")
# Prints the reconstruted track
for i, track in enumerate(output_file.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)








