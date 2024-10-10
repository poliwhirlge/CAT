import math
import random
from collections import defaultdict
from typing import Dict, Set, List
from dataclasses import dataclass
from enum import Enum, auto
from bisect import bisect_right

import C3notes
from cat_commons import Note
from reaper_python import RPR_ShowConsoleMsg
from parsing.parse_reaper_project import parse_project, MidiProject, MidiTrack


overdrive_note = 116
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
            RPR_ShowConsoleMsg(f'{start_measure} - {end_measure} {list(range(start_measure - 1, end_measure + 1))}\n')
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

    def get_bin(m: int) -> int:
        return math.floor((m - min_m) / (max_m - min_m - 12) * num_divisions)

    all_bins = list(range(num_divisions))
    unison_bins = [get_bin(m) for m in valid_unison_measures]
    RPR_ShowConsoleMsg(f'unison_measures binned: {unison_bins}\n')
    for track in valid_tracks:
        RPR_ShowConsoleMsg(f'{track.track_name} binned: {[get_bin(m) for m in valid_measures_map[track.track_name]]}\n')

    # choose unison bins
    curr_bin = None
    selected_unison_bins = []
    for b in reversed(unison_bins):
        if curr_bin is None or curr_bin - 1 > b:
            selected_unison_bins.append(b)
            curr_bin = b
    selected_unison_bins = selected_unison_bins[:target_num_unison_phrases]

    RPR_ShowConsoleMsg(f'selected_unison_bins: {selected_unison_bins}\n')
    selected_unison_measures = []
    for b in selected_unison_bins:
        unison_measures = [m for m in valid_unison_measures if b == get_bin(m)]
        selected_unison_measures.append(unison_measures[(len(unison_measures) + 1) // 2])

    RPR_ShowConsoleMsg(f'selected_unison_measures: {selected_unison_measures}\n')

    for track in valid_tracks:
        invalid_measures = set.union(*[set(range(m - 4, m + 5)) for m in selected_unison_measures])
        valid_measures_map[track.track_name] -= invalid_measures

    RPR_ShowConsoleMsg(f'valid od measures after unisons: {valid_measures_map}\n')

    # add non-unison overdrives
    non_unison_overdrives: Dict[str, List[int]] = defaultdict(lambda: list())
    for b in [bin for bin in all_bins if bin not in selected_unison_bins]:
        for track in valid_tracks:
            overdrive_candidates = [m for m in valid_measures_map[track.track_name] if b == get_bin(m)]
            if len(overdrive_candidates) == 0:
                continue
            selected_overdrive_measure = overdrive_candidates[(len(overdrive_candidates) + 1) // 2]
            non_unison_overdrives[track.track_name].append(selected_overdrive_measure)
            for track_ in valid_tracks:
                if track_ == track:
                    valid_measures_map[track_.track_name] -= set(range(selected_overdrive_measure - 3, selected_overdrive_measure + 4))
                else:
                    # remove measure as a valid overdrive measure from other tracks (to avoid unisons)
                    valid_measures_map[track_.track_name].discard(selected_overdrive_measure)

    RPR_ShowConsoleMsg(f'selected_non_unison_measures: {non_unison_overdrives}\n')

    # randomly add some random overdrive measures if not enough measures were picked for some instruments
    random.seed(19)
    for track in valid_tracks:
        while (len(non_unison_overdrives[track.track_name]) + len(selected_unison_measures) < target_num_od_phrases[track.track_name]
               and len(valid_measures_map[track.track_name]) > 0):
            random_overdrive_measure = random.choice(list(valid_measures_map[track.track_name]))
            non_unison_overdrives[track.track_name].append(random_overdrive_measure)
            valid_measures_map[track.track_name] -= set(range(random_overdrive_measure - 3, random_overdrive_measure + 4))

    # place overdrives
    for track in valid_tracks:
        replace_overdrives(midi_project, track, non_unison_overdrives[track.track_name] + selected_unison_measures)


def replace_overdrives(midi_project: MidiProject, track: MidiTrack, overdrive_measures: List[int]):
    # remove existing overdrives
    notes = [n for n in track.notes if n.pitch != overdrive_note]

    # add new fill markers
    n_placed = 0
    for m_idx in overdrive_measures:
        m_start = midi_project.measures[m_idx - 1]
        m_end = midi_project.measures[m_idx]
        notes.append(Note(tick=m_start.tick_at_start, pitch=overdrive_note, duration=m_end.tick_at_start - m_start.tick_at_start))
        n_placed += 1

    track.notes = notes
    midi_project.write_midi_track(track)
    RPR_ShowConsoleMsg(f'Placed {n_placed} overdrive markers on track {track.track_name}.\n')
