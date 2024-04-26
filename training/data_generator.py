import os
import itertools
from utils import generate_file_name
from musical_elements import (
    notes,
    chords,
    durations,
    rests,
    synths,
    samples,
    effects,
    envelopes,
    rhythms,
    scales,
)


class DataGenerator:
    def __init__(self):
        self.total_scripts = 0
        self.create_folders()

    def create_folders(self):
        folders = [
            "data",
            "data/notes",
            "data/chords",
            "data/durations",
            "data/rests",
            "data/synths",
            "data/samples",
            "data/effects",
            "data/envelopes",
            "data/rhythms",
            "data/scales",
            "data/note_duration",
            "data/chord_duration",
            "data/synth_note",
            "data/effect_note",
            "data/envelope_note",
            "data/scale_note",
        ]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

    def generate_scripts(self):
        self.generate_primitive_scripts()
        self.generate_combination_scripts()

    def generate_primitive_scripts(self):
        for note in notes:
            self.generate_script("notes", "note", note.lstrip(":"), f"play {note}")

        for chord in chords:
            self.generate_script(
                "chords", "chord", chord.split(",")[1].strip()[1:-1], f"play {chord}"
            )

        for duration in durations:
            self.generate_script(
                "durations", "duration", str(duration), f"play :c4, sustain: {duration}"
            )

        for rest in rests:
            self.generate_script("rests", "rest", str(rest), f"sleep {rest}")

        for synth in synths:
            self.generate_script(
                "synths", "synth", synth.lstrip(":"), f"use_synth {synth}\nplay :c4"
            )

        for sample in samples:
            self.generate_script(
                "samples", "sample", sample.lstrip(":"), f"sample {sample}"
            )

        for effect, values in effects:
            for value in values:
                self.generate_script(
                    "effects",
                    "effect",
                    f"{effect}_{value}",
                    f"play :c4, {effect}: {value}",
                )

        for envelope, values in envelopes:
            for value in values:
                self.generate_script(
                    "envelopes",
                    "envelope",
                    f"{envelope}_{value}",
                    f"play :c4, {envelope}: {value}",
                )

        for rhythm in rhythms:
            self.generate_script(
                "rhythms",
                "rhythm",
                rhythm.replace('"', "")
                .replace("(", "")
                .replace(")", "")
                .replace(" ", "_"),
                f"play_pattern {rhythm}",
            )

        for scale in scales:
            self.generate_script(
                "scales",
                "scale",
                scale.split(",")[0].split("(")[1][1:]
                + "_"
                + scale.split(",")[1].strip()[1:-1],
                f"{scale}\nplay_pattern_timed [:c4, :e4, :g4], [0.5, 0.5, 0.5]",
            )

    def generate_combination_scripts(self):
        for note, duration in itertools.product(notes, durations):
            self.generate_script(
                "note_duration",
                "note_duration",
                f'{note.lstrip(":")}_{duration}',
                f"play {note}, sustain: {duration}",
            )

        for chord, duration in itertools.product(chords, durations):
            self.generate_script(
                "chord_duration",
                "chord_duration",
                f'{chord.split(",")[1].strip()[1:-1]}_{duration}',
                f"play {chord}, sustain: {duration}",
            )

        for synth, note in itertools.product(synths, notes):
            self.generate_script(
                "synth_note",
                "synth_note",
                f'{synth.lstrip(":")}_{note.lstrip(":")}',
                f"use_synth {synth}\nplay {note}",
            )

        for effect, value in itertools.product(
            effects, [v for _, values in effects for v in values]
        ):
            for note in notes:
                self.generate_script(
                    "effect_note",
                    "effect_note",
                    f'{effect[0]}_{value}_{note.lstrip(":")}',
                    f"play {note}, {effect[0]}: {value}",
                )

        for envelope, value in itertools.product(
            envelopes, [v for _, values in envelopes for v in values]
        ):
            for note in notes:
                self.generate_script(
                    "envelope_note",
                    "envelope_note",
                    f'{envelope[0]}_{value}_{note.lstrip(":")}',
                    f"play {note}, {envelope[0]}: {value}",
                )

        for scale, note in itertools.product(scales, notes):
            self.generate_script(
                "scale_note",
                "scale_note",
                f'{scale.split(",")[0].split("(")[1][1:]}_{scale.split(",")[1].strip()[1:-1]}_{note.lstrip(":")}',
                f"{scale}\nplay {note}",
            )

    def generate_script(self, subfolder, prefix, suffix, content):
        file_name = generate_file_name(prefix, suffix, content)
        with open(f"data/{subfolder}/{file_name}.rb", "w") as f:
            f.write(content)
        self.total_scripts += 1
