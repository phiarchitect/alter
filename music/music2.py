import harmonic_resonance.midiator as pm

PROJECT = "ARC_Soundscape"
title = "Evolving Patterns"
bpm = 90
bpM = 4
root = pm.N.F3
key = "F"

part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
M = part.measure_ticks()

piano = part.add_piano()
bass = part.add_bass()
strings = part.add_strings()
vibes = part.add_vibes()
choir = part.add_choir_swell()

standard = pm.Standard(part)
conga = pm.Conga(part)

# Custom chord progression
chords = [
    ("IM7", 1, pm.C.major_7),
    ("vi7", 6, pm.C.minor_7),
    ("IVdom9", 4, pm.C.dominant_9),
    ("V13", 5, pm.C.dominant_13),
]

progression = pm.progressions.build_progression(
    pm.Scale(root, scale_type=pm.S.major), chords
)

for loop in range(8):  # 8 repetitions of our chord progression
    part.set_marker(f"Section {loop + 1}", 0)

    for chord_name, chord_notes in progression:
        part.set_marker(f"{chord_name}", 0)

        for m in range(4):  # 4 measures per chord
            part.set_marker(f"", M)

            # Bass
            bass.set_note(chord_notes[0] - 12, M, velocity=min(70 + loop * 3, 127))

            # Piano
            if loop > 1:
                piano.set_notes(chord_notes, M, velocity=min(50 + loop * 5, 127))

            # Strings
            if loop > 3:
                strings.set_notes(chord_notes, M, velocity=min(40 + loop * 4, 127))

            # Vibes
            if loop > 5 and m % 2 == 0:
                vibes.set_notes(
                    [note + 12 for note in chord_notes],
                    M // 2,
                    velocity=min(60 + loop * 2, 127),
                )
                vibes.set_rest(M // 2)

            # Choir
            if loop > 2:
                choir.set_notes(chord_notes, M, velocity=min(30 + loop * 3, 127))

            # Percussion
            if loop > 0:
                if m == 3:
                    patterns = standard.patterns["funky_drummer"]
                else:
                    patterns = standard.patterns["billie_jean"]
                standard.set_patterns(patterns, M, velocity_mod=-10)

            if loop > 4:
                if m % 2 == 0:
                    patterns = conga.patterns["tumbao"]
                else:
                    patterns = conga.patterns["samba"]
                conga.set_patterns(patterns, M, velocity_mod=min(loop * 2, 10))

        # Volume changes
        for instrument in [piano, strings, bass, vibes, choir]:
            instrument.set_volume(64, 0)
            instrument.ramp_volume_up(2 * M)
            instrument.ramp_volume_down(2 * M)

part.save()
part.play()
part.convert()
