import math
from collections import defaultdict
from typing import Dict, Set, List
from dataclasses import dataclass
from enum import Enum, auto
from bisect import bisect_right

import C3notes
from cat_commons import Note
from reaper_python import RPR_ShowConsoleMsg
from parsing.parse_reaper_project import parse_project, MidiProject, MidiTrack


def run():
    midi_project = parse_project()
    drum_track: MidiTrack = midi_project.parse_track('PART DRUMS')
    guitar_track: MidiTrack = midi_project.parse_track('PART GUITAR')
    bass_track: MidiTrack = midi_project.parse_track('PART BASS')
    keys_track: MidiTrack = midi_project.parse_track('PART KEYS')

    notes_x = {
        'PART DRUMS': {k: v for k, v in C3notes.notesname_array['DRUMS'].items() if v[1] == 'notes_x'},
        'PART GUITAR': {k: v for k, v in C3notes.notesname_array['5LANES'].items() if v[1] == 'notes_x'},
        'PART BASS': {k: v for k, v in C3notes.notesname_array['5LANES'].items() if v[1] == 'notes_x'},
        'PART KEYS': {k: v for k, v in C3notes.notesname_array['5LANES'].items() if v[1] == 'notes_x'},
    }
    RPR_ShowConsoleMsg(f'Notes x: {notes_x}\n')

    valid_tracks: List[MidiTrack] = [track for track in [drum_track, guitar_track, bass_track, keys_track] if len(track.notes) > 0]
    valid_measures_map: Dict[str, Set[int]] = {}
    for track in valid_tracks:
        valid_measures = set()
        valid_measures_map[track.track_name] = valid_measures
        for note in track.notes:
            if note.pitch in notes_x[track.track_name]:
                m, *_ = midi_project.mbt(note.tick)
                valid_measures.add(m)

    RPR_ShowConsoleMsg(f'valid_measures_map: {valid_measures_map}\n')
