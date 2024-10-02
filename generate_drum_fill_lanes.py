import math
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
    events_track = midi_project.parse_track('EVENTS')

    notes_by_measure = defaultdict(lambda: set())
    notes_by_tick = defaultdict(lambda: set())
    tom_markers = []
    for note in drum_track.notes:
        if note.pitch in tom_markers_map:
            tom_markers.append(note)
        elif note.pitch in drum_pitch_map:
            m, *_ = midi_project.mbt(note.tick)
            notes_by_measure[m].add(note)
            notes_by_tick[note.tick].add(note)

    RPR_ShowConsoleMsg(f'Notes: {"\n".join([f'{k},{len(v)}' for k, v in notes_by_measure.items()])} \n')

    practice_sections = events_track.get_practice_sections()
    RPR_ShowConsoleMsg(f'practice_sections {practice_sections}\n\n')
    practice_range_start = [midi_project.mbt(section.tick).measure_idx for section in practice_sections]
    if len(practice_range_start) == 0:
        RPR_ShowConsoleMsg('No practice sections found.')
        practice_range_start.append(1)
    RPR_ShowConsoleMsg(f'practice_range_start {practice_range_start}\n\n')

    for section in practice_sections:
        measure_idx, _, _, tick_from_measure_start = midi_project.mbt(section.tick)
        if tick_from_measure_start != 0:
            RPR_ShowConsoleMsg('')
        section_start_notes = notes_by_tick[section.tick]
        RPR_ShowConsoleMsg(f'Notes at measure [{midi_project.mbt(section.tick).measure_idx}]: {section_start_notes}\n')

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
        has_kick = any(n.pitch == 96 for n in note_on_tick)
        has_snare = any(n.pitch == 97 for n in note_on_tick)
        has_crash = any(n.pitch == 100 or n.pitch == 99 for n in note_on_tick)
        kick_and_crash = has_kick and has_crash
        is_section_start = any(m_idx == midi_project.mbt(p.tick).measure_idx for p in practice_sections)

        RPR_ShowConsoleMsg(f'M{m_idx}: {building_up} {intensity_drop} {re_entry} {has_kick} {has_crash} \n')

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
    # RPR_ShowConsoleMsg(f'Scores: {[(m.measure_idx, score) for m, score in zip(midi_project.measures, temp)]}\n')

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
        n_markers_expected = math.floor(n_measure_in_section / m_between_markers)

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
                scores = [suitability[candidate_m + m][0] for m in range(n_measure_in_section % m_between_markers)]
                RPR_ShowConsoleMsg(f'candidate_m {candidate_m} scores {scores} \n')
                max_score = max(scores)
                max_idx = scores.index(max_score)
                max_measure = candidate_m + max_idx
                if max_score > 0:
                    drum_fill_markers_all.append(max_measure)
                elif max_score == 0:
                    drum_fill_markers_secondary.append(max_measure)

    RPR_ShowConsoleMsg(f'Candidate drum fill markers: {drum_fill_markers_all}\n')
    only_strong_candidates = [m for m in drum_fill_markers_all if m not in drum_fill_markers_secondary]
    RPR_ShowConsoleMsg(f'Candidate drum fill markers (strong only): {only_strong_candidates}\n')
