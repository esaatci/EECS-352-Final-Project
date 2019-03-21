import mido
import copy



def transpose(key):
	key_arr = ["C","D","E","F","G","A","B"]
	pass

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


# name  of the file
file_name = "data/Nottingham/test/ashover_simple_chords_17.mid"

# open the file
mid = mido.MidiFile(file_name)

data_arr = []
note = [0 for i in range(100)]


			


for msg in mid.tracks[1]:
	if msg.type == "note_off":
		normalized_time = (msg.time + 1) / 960
		temp_note = copy.copy(note)
		temp_note[msg.note] = 1
		temp_note.append(normalized_time)
		data_arr.append(temp_note)


output_file = mido.MidiFile()
output_track = mido.MidiTrack()

# <meta message set_tempo tempo=500000 time=0>
# <meta message key_signature key='E' time=0>
# <meta message time_signature numerator=4 denominator=4 clocks_per_click=48 notated_32nd_notes_per_beat=8 time=0>
# <meta message track_name name='Falling About' time=0>
# <meta message end_of_track time=61465>

# output_track.append(mido.Message("set_tempo", set_tempo))

print("ENCODED DATA")
print("=========================================================================")
print(data_arr[1])
print("=========================================================================")

for data in data_arr:
	note_value = calculate_note(data)
	time = data[-1]
	denormalized_time = int(time * 960 - 1)
	on = mido.Message('note_on', note=note_value, velocity=64, time=1)
	off = mido.Message('note_off', note=note_value, velocity=0, time=denormalized_time)
	
	output_track.append(on)
	output_track.append(off)




output_file.tracks.append(output_track)

output_file.save("test.mid")


print("reconstruted track")
print("=========================================================================")
# Prints the reconstruted track
for i, track in enumerate(output_file.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)








