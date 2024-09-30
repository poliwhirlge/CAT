from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from reaper_python import RPR_ShowConsoleMsg
from parsing.parse_reaper_project import parse_project


class NoteColor(Enum):
    Green = auto()
    Blue = auto()
    Yellow = auto()
    Red = auto()
    Kick = auto()


class NoteType(Enum):
    Cymbal = auto()
    Tom = auto()


@dataclass
class DrumNote:
    color: NoteColor
    type: NoteType = NoteType.Cymbal


drum_pitch_map = {
    100: ["Expert Green", "notes_x", "G"],
    99: ["Expert Blue", "notes_x", "B"],
    98: ["Expert Yellow", "notes_x", "Y"],
    97: ["Expert Red", "notes_x", "R"],
    96: ["Expert Kick", "notes_x", "O"],
    95: ["Expert 2x Kick", "notes_x", "O"],
}

tom_markers_map = {
    112: NoteColor.Green,
    111: NoteColor.Blue,
    110: NoteColor.Yellow
}


def launch():
    midi_project = parse_project()
    drum_track = midi_project.parse_track('PART DRUMS')

    notes_by_measure = defaultdict(lambda: set())
    tom_markers = []
    for note in drum_track.notes:
        if note.pitch in tom_markers_map:
            tom_markers.append(note)
        elif note.pitch in drum_pitch_map:
            m, *_ = midi_project.mbt(note.tick)
            notes_by_measure[m].add(note)

    RPR_ShowConsoleMsg(f'Notes: {"\n".join([f'{k},{len(v)}' for k, v in notes_by_measure.items()])} \n')
