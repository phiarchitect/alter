import harmonic_resonance.midiator as pm

PROJECT = "ARC_Soundscape"
title = "Puzzle Solver's Journey"
bpm = 72
bpM = 4
root = pm.N.G3
key = "G"

part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
M = part.measure_ticks()

piano = part.add_piano()
bass = part.add_bass()
strings = part.add_strings()
vibes = part.add_vibes()
horns = part.add_horns()

standard = pm.Standard(part)

# Custom chord progression
chords = [
    ('I', 1, pm.C.major),
    ('V', 5, pm.C.major),
    ('vi', 6, pm.C.minor),
    ('IV', 4, pm.C.major)
]

progression = pm.progressions.build_progression(pm.Scale(root, scale_type=pm.S.major), chords)

# Define a simple melody (relative to the root note)
melody = [0, 2, 4, 2, 7, 5, 4, 2]

for loop in range(6):  # 6 repetitions of our progression
    part.set_marker(f"Section {loop + 1}", 0)
    
    for chord_idx, (chord_name, chord_notes) in enumerate(progression):
        part.set_marker(f"{chord_name}", 0)
        
        for m in range(2):  # 2 measures per chord
            part.set_marker(f"", M)
            
            # Bass
            bass.set_note(chord_notes[0] - 12, M, velocity=min(80 + loop * 5, 127))
            
            # Chords
            if loop > 0:
                piano.set_notes(chord_notes, M, velocity=min(60 + loop * 5, 127))
            
            # Strings pad
            if loop > 2:
                strings.set_notes(chord_notes, M, velocity=min(50 + loop * 5, 127))
            
            # Melody
            if loop > 1:
                melody_note = root + melody[(chord_idx * 2 + m) % len(melody)]
                if loop > 3:
                    vibes.set_note(melody_note, M // 2, velocity=min(70 + loop * 5, 127))
                    vibes.set_note(melody_note + 12, M // 2, velocity=min(70 + loop * 5, 127))
                else:
                    horns.set_note(melody_note, M, velocity=min(70 + loop * 5, 127))
            
            # Percussion
            if loop > 0:
                if m == 1:
                    patterns = standard.patterns["funky_drummer"]
                else:
                    patterns = standard.patterns["billie_jean"]
                standard.set_patterns(patterns, M, velocity_mod=min(-10 + loop * 2, 0))

        # Volume changes
        for instrument in [piano, strings, bass, vibes, horns]:
            instrument.set_volume(64, 0)
            instrument.ramp_volume_up(M)
            instrument.ramp_volume_down(M)

# Add a final resolving chord
final_chord = pm.get_chord_notes(root, pm.C.major_7)
part.set_marker("Final", 0)
for instrument in [piano, strings, bass, vibes, horns]:
    instrument.set_notes(final_chord, 2 * M, velocity=100)
    instrument.ramp_volume_down(2 * M)

part.save()
part.play()
part.convert()

