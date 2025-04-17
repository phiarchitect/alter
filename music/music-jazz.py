import harmonic_resonance.midiator as pm

PROJECT = "ARC_Jazz"
title = "Puzzle Swing"
bpm = 130
bpM = 4
root = pm.N.F3
key = "F"

part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
M = part.measure_ticks()

piano = part.add_piano()
bass = part.add_bass()
vibes = part.add_vibes()
ride = pm.Percussion(part, pm.P.ride_cymbal_1)
hihat = pm.Percussion(part, pm.P.closed_hi_hat)

chords = [
    ('IIm7', 2, pm.C.minor_7),
    ('V7', 5, pm.C.dominant_7),
    ('IM7', 1, pm.C.major_7),
    ('VIm7', 6, pm.C.minor_7)
]

progression = pm.progressions.build_progression(pm.Scale(root, scale_type=pm.S.major), chords)

melody = [0, 4, 5, 7, 9, 7, 5, 4, 2, 0, -1, 0]

for loop in range(4):
    part.set_marker(f"Chorus {loop + 1}", 0)
    
    for chord_idx, (chord_name, chord_notes) in enumerate(progression):
        part.set_marker(f"{chord_name}", 0)
        
        for m in range(2):
            part.set_marker(f"", M)
            
            # Walking bass
            for beat in range(4):
                note = chord_notes[beat % len(chord_notes)] - 12
                bass.set_note(note, M // 4, velocity=min(90 + loop * 5, 127))
            
            # Syncopated piano chords
            if m == 0:
                piano.set_notes(chord_notes, M // 2, offset=M // 4, velocity=min(70 + loop * 5, 127))
                piano.set_notes(chord_notes, M // 4, offset=3 * M // 4, velocity=min(60 + loop * 5, 127))
                piano.set_rest(M // 4)
            else:
                piano.set_notes(chord_notes, M // 2, velocity=min(70 + loop * 5, 127))
                piano.set_notes(chord_notes, M // 2, offset=M // 2, velocity=min(65 + loop * 5, 127))
            
            # Melody on vibes
            for i, note in enumerate(melody[m * 6: (m + 1) * 6]):
                vibes.set_note(root + note, M // 6, velocity=min(80 + loop * 5, 127))
            
            # Ride cymbal pattern
            ride_pattern = "5-3-5-3-5-3-5-3-"
            ride.add_pattern(ride_pattern, M // 8, velocity_mod=min(loop * 2, 10))
            
            # Hi-hat on 2 and 4
            hihat.set_rest(M // 2)
            hihat.set_hit(M // 4, velocity=min(70 + loop * 5, 127))
            hihat.set_rest(M // 2)
            hihat.set_hit(M // 4, velocity=min(70 + loop * 5, 127))

        # Volume swells
        for instrument in [piano, vibes]:
            instrument.set_volume(64, 0)
            instrument.ramp_volume_up(M // 2)
            instrument.ramp_volume_down(3 * M // 2)

# Add a final jazzy chord
final_chord = pm.get_chord_notes(root, pm.C.major_6)
part.set_marker("Final", 0)
piano.set_notes(final_chord, 2 * M, velocity=100)
vibes.set_notes([note + 12 for note in final_chord], 2 * M, velocity=90)
bass.set_note(root - 12, 2 * M, velocity=100)
ride.set_hit(2 * M, velocity=90)

for instrument in [piano, vibes, bass]:
    instrument.ramp_volume_down(2 * M)

part.save()
part.play()
