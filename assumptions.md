## ASSUMPTIONS & SIMPLIFICATIONS:
## 1) We only look at the melody and disregard the harmony
## 2) First track in the poly-track midi file is always the melody
## 3) After every note-on, there is a note-off for the same note
## 4) We find min and max note and constrain our notes within that range
## 5) There is no rest between notes, there is always a note playing