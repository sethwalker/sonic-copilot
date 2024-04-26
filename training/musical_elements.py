# Notes and pitches
notes = [
    f":{note}{accidental}{octave}"
    for note in ["c", "d", "e", "f", "g", "a", "b"]
    for accidental in ["", "s", "b"]
    for octave in range(3, 6)
]
chords = [
    f"chord(:{note}, :{chord_type})"
    for note in [note.lstrip(":") for note in notes]
    for chord_type in [
        "major",
        "minor",
        "dim",
        "aug",
        "7",
        "major7",
        "minor7",
        "dim7",
        "m7b5",
        "aug7",
        "9",
        "minor9",
        "sus2",
        "sus4",
    ]
]

# Durations and rests
durations = [0.25, 0.5, 1, 2]
rests = [0.5, 1, 2]

# Synths
synths = [
    ":beep",
    ":saw",
    ":tri",
    ":square",
    ":pulse",
    ":subpulse",
    ":fm",
    ":mod_fm",
    ":mod_saw",
    ":mod_dsaw",
    ":mod_sine",
    ":mod_beep",
    ":mod_tri",
    ":mod_pulse",
    ":tb303",
    ":supersaw",
    ":hoover",
    ":prophet",
    ":zawa",
    ":dark_ambience",
    ":growl",
    ":hollow",
    ":mono_player",
    ":piano",
    ":pluck",
    ":pretty_bell",
]

# Samples
samples = [
    ":loop_amen",
    ":loop_amen_full",
    ":loop_industrial",
    ":loop_compus",
    ":loop_tabla",
    ":loop_breakbeat",
    ":loop_electric",
    ":loop_mehackit1",
    ":loop_mehackit2",
    ":loop_perc1",
    ":loop_perc2",
    ":loop_weirdo",
    ":loop_safari",
    ":loop_tabla",
    ":loop_3d_printer",
    ":loop_drone_g_97",
    ":loop_electric",
    ":loop_mehackit1",
    ":loop_mehackit2",
    ":loop_mika",
    ":bd_haus",
    ":bd_zome",
    ":bd_boom",
    ":bd_klub",
    ":bd_fat",
    ":bd_tek",
    ":elec_blip",
    ":elec_blip2",
    ":elec_ping",
    ":elec_bell",
    ":elec_twang",
    ":perc_bell",
    ":perc_snap",
    ":perc_snap2",
    ":perc_swash",
    ":perc_till",
    ":drum_heavy_kick",
    ":drum_tom_mid_soft",
    ":drum_tom_mid_hard",
    ":drum_tom_lo_soft",
    ":drum_tom_lo_hard",
    ":drum_tom_hi_soft",
    ":drum_tom_hi_hard",
    ":drum_splash_soft",
    ":drum_splash_hard",
    ":drum_snare_soft",
    ":drum_snare_hard",
    ":drum_cymbal_soft",
    ":drum_cymbal_hard",
    ":drum_cymbal_open",
    ":drum_cymbal_closed",
    ":drum_cymbal_pedal",
    ":drum_bass_soft",
    ":drum_bass_hard",
]

# Effects and parameters
effects = [
    ("amp", (0.5, 1, 2)),
    ("pan", (-1, 0, 1)),
    ("reverb", (0.2, 0.5, 0.8)),
    ("delay", (0.5, 1)),
    ("cutoff", (60, 80, 100, 120)),
    ("res", (0.2, 0.4, 0.6)),
    ("attack", (0.01, 0.1, 0.5)),
    ("decay", (0.1, 0.5, 1)),
    ("sustain", (0.4, 0.6, 0.8)),
    ("release", (0.5, 1, 2)),
    ("mod_rate", (0.5, 1, 2)),
    ("mod_range", (12, 24, 36)),
]

# Envelopes
envelopes = [
    ("attack", (0.01, 0.1, 0.5)),
    ("decay", (0.1, 0.5, 1)),
    ("sustain", (0.4, 0.6, 0.8)),
    ("release", (0.5, 1, 2)),
]

# Rhythmic patterns
rhythms = [
    "[1, 1, 1, 1]",
    "[1, 0, 1, 0]",
    "[1, 0, 0, 0]",
    "[1, 1, 0, 1, 1, 0]",
    "(ring 1, 0, 0, 1, 0)",
    "(ring 1, 1, 0, 0, 1, 0)",
    "(ring 1, 0, 1, 0, 1, 1)",
    "(ring 1, 1, 1, 0, 0, 1, 0, 1)",
    "(ring 1, 0, 1, 1, 0, 1, 0)",
]

# Musical scales and modes
scales = [
    "scale(:c4, :major)",
    "scale(:a3, :minor)",
    "scale(:c4, :dorian)",
    "scale(:d4, :mixolydian)",
    "scale(:e4, :aeolian)",
    "scale(:f4, :lydian)",
    "scale(:g4, :phrygian)",
    "scale(:c4, :chromatic)",
    "scale(:c4, :harmonic_minor)",
    "scale(:c4, :melodic_minor)",
    "scale(:c4, :hungarian_minor)",
    "scale(:c4, :whole_tone)",
    "scale(:c4, :diminished)",
    "scale(:c4, :spanish)",
]

# Loops
loops = [
    ("live_loop", 4),
    ("live_loop", 8),
    ("live_loop", 16),
    ("4.times do", "end"),
    ("8.times do", "end"),
    ("16.times do", "end"),
]
