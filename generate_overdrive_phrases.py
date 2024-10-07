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


bre_notes = [120, 121, 122, 123, 124]


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

    RPR_ShowConsoleMsg(f'# of measures with notes: { {k: len(v) for k, v in valid_measures_map.items()} }\n')
    target_num_od_phrases = {k: round(len(v) / 10) for k, v in valid_measures_map.items()}
    RPR_ShowConsoleMsg(f'target_num_od_phrases: { target_num_od_phrases }\n')
    target_num_unison_phrases = round(min(target_num_od_phrases.values()) / 2)
    RPR_ShowConsoleMsg(f'target_num_unison_phrases: {target_num_unison_phrases}\n')
    last_measures = {k: max(v) for k, v in valid_measures_map.items()}
    first_measures = {k: min(v) for k, v in valid_measures_map.items()}
    RPR_ShowConsoleMsg(f'last_measures: {last_measures}\n')

    # drum fill measures are invalid for overdrive
    if 'PART DRUMS' in [track.track_name for track in valid_tracks]:
        drum_fills_notes: List[Note] = [n for n in drum_track.notes if n.pitch in bre_notes]
        invalid_measures = set()
        for n in drum_fills_notes:
            start_measure = midi_project.mbt(n.tick).measure_idx
            end_measure = midi_project.mbt(n.tick + n.duration).measure_idx
            # block 1 measure before and after the drum fill
            invalid_measures.update(list(range(start_measure - 1, end_measure + 1)))

        RPR_ShowConsoleMsg(f'invalid drums: {invalid_measures}\n')
        valid_measures_map['PART DRUMS'] -= invalid_measures

    # remove last 12 measures from valid measures
    for track in valid_tracks:
        last_valid_measure = last_measures[track.track_name] - 12
        valid_measures_map[track.track_name] -= set(range(last_valid_measure, last_measures[track.track_name] + 1))

    valid_unison_measures = sorted(set.intersection(*valid_measures_map.values()))
    RPR_ShowConsoleMsg(f'valid unisons: {valid_unison_measures}\n')

    #
    min_m = min(first_measures.values())
    max_m = max(last_measures.values())
    song_length = max_m - min_m
    num_divisions = max(target_num_od_phrases.values())
    divided_song = [round(n / (num_divisions + 1) * song_length) + min_m for n in range(1, num_divisions + 1)]
    RPR_ShowConsoleMsg(f'divided_song {divided_song}\n')

    RPR_ShowConsoleMsg(f'valid od measures: {valid_measures_map}\n')
    target_unison_locations = divided_song[::2]
    for m in target_unison_locations:
        i = bisect_right(valid_unison_measures, m)
    unison_measures = [valid_unison_measures[bisect_right(valid_unison_measures, m) - 1]for m in target_unison_locations]

    RPR_ShowConsoleMsg(f'unison_measures: {unison_measures}\n')

