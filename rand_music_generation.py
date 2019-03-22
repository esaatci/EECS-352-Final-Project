import mido
import numpy as np 

output_file = mido.MidiFile()
output_track1 = mido.MidiTrack()



# initialize start note 
start_note = int(np.random.rand() * 32) + 44

time = 479

#meta messages such as tempo, track name, instrument, etc...
output_track1.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))


for _ in range(128):
	note_value = int(np.random.rand()*41 + 48)
	time_ = (int(np.random.randn() * 1000)  % 8 )
	time_ = max(int(time_) * 120- 1, 119)
	on = mido.Message('note_on', note=note_value, velocity=64, time=1)
	off = mido.Message('note_off', note=note_value, velocity=0, time=time_)

	output_track1.append(on)
	output_track1.append(off)

	

print("RANDOM SONG MIDI REPRESENTATION")
print("=========================================================================")
print(output_track1)
print("=========================================================================")



output_file.tracks.append(output_track1)

output_file.save("random-output3.mid")

print("reconstruted track")
print("=========================================================================")
# Prints the reconstruted track
for i, track in enumerate(output_file.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)








