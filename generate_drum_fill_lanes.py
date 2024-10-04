import math
from collections import defaultdict
from typing import Dict, Set, List
from dataclasses import dataclass
from enum import Enum, auto
from bisect import bisect_right

from cat_commons import Note
from reaper_python import RPR_ShowConsoleMsg
from parsing.parse_reaper_project import parse_project, MidiProject, MidiTrack


class DrumNote(Enum):
    GreenCymbal = auto()
    BlueCymbal = auto()
    YellowCymbal = auto()
    Red = auto()
    Kick = auto()
    GreenTom = auto()
    BlueTom = auto()
    YellowTom = auto()


class NoteColor(Enum):
    Green = auto()
    Blue = auto()
    Yellow = auto()
    Red = auto()
    Kick = auto()


drum_pitch_map = {
    100: DrumNote.GreenCymbal,
    99: DrumNote.BlueCymbal,
    98: DrumNote.YellowCymbal,
    97: DrumNote.Red,
    96: DrumNote.Kick,
    95: DrumNote.Kick,
}

tom_markers_map = {
    112: NoteColor.Green,
    111: NoteColor.Blue,
    110: NoteColor.Yellow
}

bre_notes = [120, 121, 122, 123, 124]


def replace_bre_notes(midi_project: MidiProject, drum_track: MidiTrack, drum_fill_markers_to_place, coda_tick: int = -1):
    # remove existing BRE notes
    notes = [n for n in drum_track.notes if n.pitch not in bre_notes or (n.pitch in bre_notes and n.tick == coda_tick)]

    # add new fill markers
    n_placed = 0
    for m_idx in drum_fill_markers_to_place:
        m_start = midi_project.measures[m_idx - 2]
        m_end = midi_project.measures[m_idx - 1]
        if m_start.tick_at_start >= coda_tick != -1:
            continue

        n_placed += 1
        for fill_note in bre_notes:
            notes.append(Note(tick=m_start.tick_at_start, pitch=fill_note, duration=m_end.tick_at_start - m_start.tick_at_start))

    drum_track.notes = notes
    midi_project.write_midi_track(drum_track)
    RPR_ShowConsoleMsg(f'Placed {n_placed} drum fill markers.\n')


def launch():
    midi_project = parse_project()
    drum_track = midi_project.parse_track('PART DRUMS')
    events_track = midi_project.parse_track('EVENTS')

    notes_by_measure: Dict[int, Set[DrumNote]] = defaultdict(lambda: set())
    notes_by_tick: Dict[int, Set[DrumNote]] = defaultdict(lambda: set())
    tom_markers: Dict[NoteColor, List[Note]] = defaultdict(lambda: list())
    for note in drum_track.notes:
        if note.pitch in tom_markers_map:
            tom_markers[tom_markers_map[note.pitch]].append(note)

    def is_tom(color, tick):
        if color not in tom_markers_map:
            return False
        markers = tom_markers[color]
        idx = bisect_right(markers, tick, key=lambda n: n.tick)
        return markers[idx - 1].tick <= tick < markers[idx - 1].tick + markers[idx - 1].duration

    for note in drum_track.notes:
        if note.pitch in drum_pitch_map:
            d_note = drum_pitch_map[note.pitch]
            m, *_ = midi_project.mbt(note.tick)
            if d_note == DrumNote.GreenCymbal:
                d_note = DrumNote.GreenTom if is_tom(NoteColor.Green, note.tick) else DrumNote.GreenCymbal
            if d_note == DrumNote.BlueCymbal:
                d_note = DrumNote.BlueTom if is_tom(NoteColor.Blue, note.tick) else DrumNote.BlueCymbal
            if d_note == DrumNote.YellowCymbal:
                d_note = DrumNote.YellowTom if is_tom(NoteColor.Yellow, note.tick) else DrumNote.YellowCymbal

            notes_by_measure[m].add(d_note)
            notes_by_tick[note.tick].add(d_note)

    practice_sections = events_track.get_practice_sections()

    if len(practice_sections) == 0:
        RPR_ShowConsoleMsg('No practice sections found, this function works better if section markers are correctly placed.\n')

    for section in practice_sections:
        measure_idx, _, _, tick_from_measure_start = midi_project.mbt(section.tick)
        if tick_from_measure_start != 0:
            RPR_ShowConsoleMsg('')

    def rate_suitability(m_idx: int, m_tick_start: int):
        notes_m_2 = notes_by_measure[m_idx - 2]
        notes_m_1 = notes_by_measure[m_idx - 1]
        notes_m = notes_by_measure[m_idx]
        notes_m_1_a = notes_by_measure[m_idx + 1]
        note_on_tick = notes_by_tick[m_tick_start]

        building_up = len(notes_m_1) > len(notes_m_2)
        intensity_drop = len(notes_m_1) * 0.60 > len(notes_m) and len(notes_m_2) * 0.60 > len(notes_m)
        is_empty = len(notes_m) == 0
        is_quiet = len(notes_m) <= 3
        next_measure_quiet = len(notes_m_1_a) <= 2
        re_entry = len(notes_m) > len(notes_m_1) and len(notes_m) > len(notes_m_2)
        has_kick = DrumNote.Kick in note_on_tick
        has_snare = DrumNote.Red in note_on_tick
        has_crash = DrumNote.GreenCymbal in note_on_tick or DrumNote.BlueCymbal in note_on_tick
        kick_and_crash = has_kick and has_crash
        is_section_start = any(m_idx == midi_project.mbt(p.tick).measure_idx for p in practice_sections)

        return (
                (5 if building_up and kick_and_crash else 0) -
                (1 if intensity_drop else 0) +
                (1 if re_entry else 0) +
                (1 if kick_and_crash else 0) +
                (-3 if next_measure_quiet else 0) +
                (-100 if is_empty else 0)
        ), {
            'building_up': building_up,
            'intensity_drop': intensity_drop,
            'is_empty': is_empty,
            'is_quiet': is_quiet,
            'next_measure_quiet': next_measure_quiet,
            're_entry': re_entry,
            'has_kick': has_kick,
            'has_snare': has_snare,
            'has_crash': has_crash,
            'is_note': len(note_on_tick) > 0
        }

    suitability = [rate_suitability(m.measure_idx, m.tick_at_start) for m in midi_project.measures]

    drum_fill_markers_all = []
    drum_fill_markers_secondary = []

    for section, next_section in zip(practice_sections, practice_sections[1:]):
        measure_idx, b, _, tick_from_measure_start = midi_project.mbt(section.tick)
        next_measure_idx, *_ = midi_project.mbt(next_section.tick)
        tempo = midi_project.measures[measure_idx - 1].bpm
        m_between_markers = 8 if tempo >= 160 else 4
        if tick_from_measure_start != 0:
            RPR_ShowConsoleMsg(f'Section {section.event_text} doesn\'t start at the start of the measure ({measure_idx.b})')
            # TODO look for first note after section start

        n_measure_in_section = next_measure_idx - measure_idx

        if n_measure_in_section % m_between_markers == 0:
            for candidate_m in range(measure_idx, next_measure_idx, m_between_markers):
                _, features = suitability[candidate_m]
                if (features['has_kick'] or features['has_snare']) and features['has_crash']:
                    drum_fill_markers_all.append(candidate_m)
                elif features['is_note']:
                    drum_fill_markers_secondary.append(candidate_m)
                    drum_fill_markers_all.append(candidate_m)
        else:
            for candidate_m in range(measure_idx, next_measure_idx, m_between_markers):
                scores = [suitability[candidate_m + m - 1][0] for m in range(n_measure_in_section % m_between_markers + 1)]
                max_score = max(scores)
                max_idx = scores.index(max_score)
                max_measure = candidate_m + max_idx
                if max_score > 0:
                    drum_fill_markers_all.append(max_measure)
                elif max_score == 0:
                    drum_fill_markers_secondary.append(max_measure)

    # Handle last section (or entire song if there were no practice sections markers
    # TODO improve algorithm: use snare/tom density to detect fills,
    start_of_last_section_tick = practice_sections[-1].tick if len(practice_sections) > 0 else min(notes_by_tick.keys())
    end_of_song_tick = max([k for k, v in notes_by_tick.items() if len(v) > 0])
    m_start, *_ = midi_project.mbt(start_of_last_section_tick)
    m_end, *_ = midi_project.mbt(end_of_song_tick)
    m_end -= 8  # stop putting markers near the end of the song
    m_between_markers = 4  # just put them everywhere
    for candidate_m in range(m_start, m_end, m_between_markers):
        scores = [suitability[candidate_m + m - 1][0] for m in range(4)]
        max_score = max(scores)
        max_idx = scores.index(max_score)
        max_measure = candidate_m + max_idx
        if max_score > 0:
            drum_fill_markers_all.append(max_measure)
        elif max_score == 0:
            drum_fill_markers_secondary.append(max_measure)

    drum_fill_markers_to_place = []

    for m in drum_fill_markers_all:
        tempo = midi_project.measures[m - 1].bpm
        m_between_markers = 8 if tempo >= 160 else 4
        m_between_weak_markers = 8 if tempo >= 120 else 4
        if len(drum_fill_markers_to_place) == 0:
            drum_fill_markers_to_place.append(m)
        elif m in drum_fill_markers_secondary:
            if drum_fill_markers_to_place[-1] + m_between_weak_markers <= m:
                drum_fill_markers_to_place.append(m)
        else:
            if drum_fill_markers_to_place[-1] + m_between_markers <= m:
                drum_fill_markers_to_place.append(m)

    coda_events = [e for e in events_track.events if e.event_text == '[coda]']
    if len(coda_events) > 1:
        RPR_ShowConsoleMsg(f'Warning: detected multiple [coda] text events on measures {[midi_project.mbt(e.tick).measure_idx for e in coda_events]}\n')
    coda_tick = coda_events[0].tick if len(coda_events) != 0 else -1

    replace_bre_notes(midi_project, drum_track, drum_fill_markers_to_place, coda_tick)
