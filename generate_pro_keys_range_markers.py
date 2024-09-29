from reaper_python import RPR_ShowConsoleMsg
from parsing.parse_reaper_project import parse_project
from cat_commons import Note


def launch():
    midi_project = parse_project()
    pk_track = midi_project.parse_track('PART REAL_KEYS_X')

    keys_high, keys_low = 72, 48
    note_range_by_measure = {}

    def update_note_ranges_cache(m: int, midi_note: int):
        if m not in note_range_by_measure:
            note_range_by_measure[m] = [midi_note, midi_note]
        else:
            current_min, current_max = note_range_by_measure[m]
            note_range_by_measure[m] = [min(current_min, midi_note), max(current_max, midi_note)]

    for note in pk_track.notes:
        select_status, tick, midi_note, velocity, duration, note_on_off_channel = note
        if not keys_low <= midi_note <= keys_high:
            continue

        m_start, *_ = midi_project.mbt(tick)
        m_end, *_ = midi_project.mbt(tick + duration)
        for m in range(m_start - 1, m_end + 1):  # must be in range at least 1 measure earlier
            update_note_ranges_cache(m, midi_note)

    note_ranges = [[k, v] for k, v in sorted(note_range_by_measure.items(), key=lambda item: item[0])]

    pk_range_to_marker = {(48, 64): 0, (53, 69): 5, (57, 72): 9,
                          (50, 65): 2, (52, 67): 4, (55, 71): 7}
    primary_pk_ranges = [pk_range for pk_range, note in pk_range_to_marker.items() if note in [0, 5, 9]]
    all_pk_ranges = [pk_range for pk_range, note in pk_range_to_marker.items()]

    def find_range_shifts(primary_ranges_only: bool = True):
        solution_cache = {}
        valid_pk_ranges = primary_pk_ranges if primary_ranges_only else all_pk_ranges

        def fn(idx, curr_range):
            key = f'{idx} {curr_range}'
            if key in solution_cache:
                return solution_cache[key]
            if idx >= len(note_ranges):
                return [0, []]
            measure, [lowest_note, highest_note] = note_ranges[idx]

            valid_ranges = [(l, h) for l, h in valid_pk_ranges if (l <= lowest_note <= highest_note <= h)]
            if len(valid_ranges) == 0:
                RPR_ShowConsoleMsg(f'No solutions due to measure {measure} with range {lowest_note}-{highest_note}\n')
                raise ValueError(f'No solutions due to measure {measure} with range {lowest_note}-{highest_note}\n')

            temp = [[cost + (0 if r[0] == curr_range[0] and r[1] == curr_range[1] else 1), path + [r]] for [cost, path], r in [[fn(idx + 1, r), r] for r in valid_ranges]]

            solution_cache[key] = min(temp, key=lambda t: t[0])
            return solution_cache[key]

        try:
            cost, reversed_path = fn(0, (-1, -1))
        except ValueError:
            return None

        optimal_pk_markers = list(zip([measure for measure, _ in note_ranges], [pk_range_to_marker[r] for r in reversed(reversed_path)]))
        return optimal_pk_markers

    optimal_pk_markers = find_range_shifts(True)
    if optimal_pk_markers is None:
        RPR_ShowConsoleMsg(f'No solution found with only primary ranges, trying to solve allowing all ranges.\n')
        optimal_pk_markers = find_range_shifts(False)

    if optimal_pk_markers is None:
        RPR_ShowConsoleMsg(f'No solution found, aborting.\n')
        return

    # Remove out existing phrase markers
    note: Note
    n_before = len(pk_track.notes)
    array_notes = [note for note in pk_track.notes if note.pitch > 9]
    RPR_ShowConsoleMsg(f'Removed {n_before - len(array_notes)} existing range marker notes.\n')

    # Filter down to markers that need to be placed
    final_range_shifts = []
    prev_marker = -1
    for measure_idx, marker_note in optimal_pk_markers:
        if marker_note != prev_marker:
            final_range_shifts.append([measure_idx, marker_note])
        prev_marker = marker_note

    # Try to move each marker to the earliest possible measure
    for measure_idx, marker_note in final_range_shifts:
        r_low, r_high = [k for k, v in pk_range_to_marker.items() if v == marker_note][0]

        def in_range(m_idx, r_low, r_high):
            if m_idx not in note_range_by_measure:
                return True
            low, high = note_range_by_measure[m_idx]
            return r_low <= low and r_high >= high

        while measure_idx > 1 and in_range(measure_idx - 1, r_low, r_high):
            measure_idx -= 1

        RPR_ShowConsoleMsg(f'Placing marker {marker_note} at measure {measure_idx}\n')
        array_notes.append(Note(tick=midi_project.measures[measure_idx - 1].tick_at_start, pitch=marker_note, duration=120))

    pk_track.notes = array_notes

    midi_project.write_midi_track(pk_track)
