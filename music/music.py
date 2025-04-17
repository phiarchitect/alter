import harmonic_resonance.midiator as pm

PROJECT = "ARC_Soundscape"
title = "Contemplative Curiosity"
bpm = 60  # slower tempo for a more thoughtful feel
bpM = 4
root = pm.N.C3
key = "C"

part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
M = part.measure_ticks()

piano = part.add_piano()
synth_pad = part.add_strings()  # we'll use strings as a synth pad
bass = part.add_bass()

# Creating a simple chord progression
chords = [
    ("Cmaj7", [0, 4, 7, 11]),
    ("Am7", [-3, 0, 4, 7]),
    ("Fmaj7", [-5, -1, 2, 5]),
    ("G7", [-3, 0, 4, 7])
]

for loop in range(8):  # 8 repetitions of our chord progression
    for chord_name, chord in chords:
        part.set_marker(f"{chord_name}", 0)
        
        # Soft piano chords
        piano.set_notes([note + root for note in chord], M, velocity=40)
        
        # Gentle synth pad
        synth_pad.set_notes([note + root + 12 for note in chord], M * 4, velocity=30)
        synth_pad.ramp_volume_up(M * 2)
        synth_pad.ramp_volume_down(M * 2)
        
        # Subtle bass notes
        bass.set_note(root + chord[0] - 12, M, velocity=50)
        
        # Adding some soft arpeggios on piano
        for beat in range(4):
            for note in chord:
                #  piano.set_note(root + note + 12, M // 4, offset=beat * M // 4 + (note % 3) * M // 16, velocity=30)
                piano.set_note(root + note + 12, M // 4, velocity=30)

part.save()
part.convert()
part.play()
