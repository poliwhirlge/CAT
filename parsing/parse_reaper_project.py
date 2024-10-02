import base64
import binascii
import codecs
import math
import operator
import traceback

import C3notes
from collections import defaultdict
from typing import List, Tuple
from bisect import bisect_right
from reaper_python import RPR_CountMediaItems, RPR_GetMediaItem, RPR_GetMediaItem_Track, RPR_GetSetMediaTrackInfo_String, RPR_GetSetItemState, RPR_ShowConsoleMsg, RPR_MB, \
    RPR_CSurf_TrackFromID, RPR_GetTrackEnvelopeByName, RPR_GetSetEnvelopeState, RPR_TimeMap_GetTimeSigAtTime
from cat_commons import Note, MidiEvent, Measure, MBTEntry, TimeSigMarker

max_len = 1048576
correct_tqn = 480


class MidiTrack:
    def __init__(self, track_name, notes: List[Note], events: List[MidiEvent], end_first_part: int, start_second_part: int, track_id: int):
        self.track_name = track_name
        self.notes = notes
        self.events = events
        self.end_first_part = end_first_part
        self.start_second_part = start_second_part
        self.track_id = track_id

    def get_practice_sections(self):
        non_practice_sections = ['EVENTS', '[crowd_intense]', '[crowd_normal]', '[crowd_mellow]', '[crowd_noclap]',
                                 '[music_start]', '[music_end]', '[end]', '[crowd_clap]', '[crowd_realtime]', '[coda]']
        return [event for event in self.events if event.event_text not in non_practice_sections]


class MidiProject:
    def __init__(self, track_id_map, end_event_tick: int, end_of_track: str):
        self.track_id_map = track_id_map
        self.end_event_tick = end_event_tick  # tick of [end] event on EVENTS track
        self.end_of_track = end_of_track  # end of track event in raw string form
        self.measures, self.time_sig_changes = parse_tempo_map(end_event_tick)
        RPR_ShowConsoleMsg(f'TS changes: {self.time_sig_changes}\n')
        RPR_ShowConsoleMsg(f'Measures: {self.measures}\n')
        if len(self.measures) == 0:
            RPR_MB("No time markers found, aborting", "Invalid tempo map", 0)
            raise Exception("No time markers found, aborting.")

    def parse_track(self, track_name):
        if track_name not in self.track_id_map:
            return None

        track_id = self.track_id_map[track_name]
        array_instrument_data = parse_midi_track_by_id(track_id)
        ticks_per_beat, notes_array, end_first_part, start_second_part = array_instrument_data
        array_notes, array_events = parse_notes_and_events(notes_array)
        return MidiTrack(track_name, array_notes, array_events, end_first_part, start_second_part, track_id)

    def mbt(self, tick):
        idx = bisect_right(self.time_sig_changes, tick, key=lambda x: x.tick)
        time_sig = self.time_sig_changes[idx - 1]
        ticks_from_prev_marker = tick - time_sig.tick
        ticks_per_measure = correct_tqn * time_sig.ts_num / time_sig.ts_den * 4
        ticks_per_beat = correct_tqn / time_sig.ts_den * 4
        n_measures = math.floor(ticks_from_prev_marker / ticks_per_measure)
        relative_position = round(ticks_from_prev_marker - n_measures * ticks_per_measure)
        b = math.floor(relative_position / ticks_per_beat)
        t = round(relative_position % ticks_per_beat)
        return MBTEntry(measure_idx=time_sig.measure_idx + n_measures, beat=b + 1, ticks_from_beat=t, ticks_from_measure_start=relative_position)

    def write_midi_track(self, track: MidiTrack):
        rebuilt_array = rebuild_array([track.notes, track.events], self.end_of_track)
        chunk = rebuild_chunk(rebuilt_array, track.track_id, track.end_first_part, track.start_second_part)
        mi = RPR_GetMediaItem(0, track.track_id)
        RPR_GetSetItemState(mi, chunk, max_len)


def rebuild_array(array_notesevents, end_of_track):
    # Create a new temp array
    array_temp = []  # This array will contain all events/notes and it will be used for sorting. Its content will then go in a raw text array
    array_raw = []
    # Loop through each note and convert the note on event in raw format to add it to the raw array

    for x in range(0, len(array_notesevents[0])):
        array_temp.append([array_notesevents[0][x][0], int(array_notesevents[0][x][1]), array_notesevents[0][x][5], (hex(int(array_notesevents[0][x][2])))[2:], array_notesevents[0][x][3]])
        # and create a note off event with absolute location
        array_temp.append(
            [array_notesevents[0][x][0], int(array_notesevents[0][x][1]) + int(array_notesevents[0][x][4]), str("8" + str(array_notesevents[0][x][5])[1:]), (hex(int(array_notesevents[0][x][2])))[2:],
             "00"])

    for x in range(0, len(array_notesevents[1])):
        hex_lyric = array_notesevents[1][x][5] + binascii.hexlify(array_notesevents[1][x][3].encode()).decode('utf-8')

        encoded_text = str(base64.b64encode(codecs.decode(hex_lyric, 'hex_codec')).decode('utf-8'))
        array_temp.append([array_notesevents[1][x][0], int(array_notesevents[1][x][1]), array_notesevents[1][x][2], encoded_text, array_notesevents[1][x][4]])

    # Incorporate the events from array_rawevents and sort by absolute location
    array_temp.sort(key=operator.itemgetter(1, 0))

    # We add the end of track event so the MIDI track doesn't cut off
    end_of_track_array = end_of_track.split(" ")
    end_of_track_time = int(end_of_track_array[1])
    if array_temp[-1][1] > int(end_of_track_array[1]):
        end_of_track_time = array_temp[-1][1] + correct_tqn
    array_temp.append([end_of_track_array[0], end_of_track_time, end_of_track_array[2], (hex(int(end_of_track_array[3])))[2:], end_of_track_array[4]])

    # Loop through the rawarray. Set location of all notes based on difference between location of note x and of note x-1 of the rawarray

    if array_temp[0][0].startswith('E') or array_temp[0][0].startswith('e'):
        array_raw.append(array_temp[0][0] + " " + str(array_temp[0][1]) + " " + str(array_temp[0][2]) + " " + str(array_temp[0][3]) + " " + str(array_temp[0][4]))
    else:
        array_raw.append(array_temp[0][0] + " " + str(array_temp[0][1]) + " " + str(array_temp[0][2]) + "\n  " + str(array_temp[0][3]) + "\n" + str(array_temp[0][4]))

    for x in range(1, len(array_temp)):
        new_location = array_temp[x][1] - array_temp[x - 1][1]

        if array_temp[x][0].startswith('E') or array_temp[x][0].startswith('e'):
            array_raw.append(array_temp[x][0] + " " + str(new_location) + " " + str(array_temp[x][2]) + " " + str(array_temp[x][3]) + " " + str(array_temp[x][4]))
        else:
            array_raw.append(array_temp[x][0] + " " + str(new_location) + " " + str(array_temp[x][2]) + "\n  " + array_temp[x][3] + "\n" + str(array_temp[x][4]))
    return array_raw


def rebuild_chunk(notes_array, instrument, end, start):
    # Let's start by putting the notes/events portion of the chunk back together. The array is already prepped here.
    notes_chunk = ""
    for x in range(0, len(notes_array)):
        if notes_array[x].startswith('E') or notes_array[x].startswith('e'):
            notes_chunk += notes_array[x] + "\n"
        else:
            notes_chunk += notes_array[x] + "\n"
    # The notes/events portion of the chunk is done, now we loop through the whole chunk to find the spot where we need to snip
    bi = RPR_GetMediaItem(0, instrument)
    first_chunk = ""
    second_chunk = ""
    sub_chunk = ""
    _, _, sub_chunk, _ = RPR_GetSetItemState(bi, sub_chunk, max_len)

    vars_array = sub_chunk.splitlines()

    for j in range(0, end + 1):
        first_chunk += vars_array[j] + "\n"

    for k in range(start, len(vars_array)):
        second_chunk += str(vars_array[k])
        if k < len(vars_array):
            second_chunk += "\n"

    chunk = first_chunk + notes_chunk + second_chunk
    return chunk


def get_track_id_map():
    num_mi = RPR_CountMediaItems(0)

    track_id_map = defaultdict(lambda: 999)
    for idx in range(num_mi):
        media_item = RPR_GetMediaItem(0, idx)
        track_id = RPR_GetMediaItem_Track(media_item)
        track_name = RPR_GetSetMediaTrackInfo_String(track_id, "P_NAME", "", 0)[3]
        RPR_GetSetItemState(media_item, '', max_len)

        if track_name in C3notes.notesname_instruments_array.keys():
            track_id_map[track_name] = idx
        elif track_name in ['EVENTS', 'BEAT', 'VENUE']:
            track_id_map[track_name] = idx
        elif track_name in ["PART DRUMS 2x", "PART DRUMS_2x", "PART DRUMS_2X"]:
            RPR_ShowConsoleMsg(f'Warning: Please use track name \'PART DRUMS 2X\' instead of {track_name}')
            track_id_map['PART DRUMS 2X'] = idx

    return track_id_map


def parse_project() -> MidiProject:
    try:
        track_name_to_id = get_track_id_map()
    except UnicodeDecodeError:
        RPR_MB(f'Unicode Error caught.\n\nPlease screenshot this error and report it.\n\n{traceback.format_exc()}', "Unicode Error", 0)
        raise

    array_instrument_data = parse_midi_track_by_id(track_name_to_id['EVENTS'])  # This toggles the processing of the EVENTS chunk that sets end_event

    ticks_per_beat, notes_array, end_first_part, start_second_part = array_instrument_data
    array_notes, array_events = parse_notes_and_events(notes_array)

    end_events = [e for e in array_events if e.event_text == '[end]']
    end_event = end_events[0].tick if len(end_events) >= 1 else 0

    end_of_track = notes_array[-1]

    return MidiProject(track_name_to_id, end_event, end_of_track)


# Originally sets end_of_track and end_event
def parse_midi_track_by_id(track_id: int):
    media_item = RPR_GetMediaItem(0, track_id)
    chunk = ""
    _, _, chunk, _ = RPR_GetSetItemState(media_item, chunk, max_len)
    notes_array = []
    vars_array = chunk.splitlines()
    n_vars = len(vars_array)
    note_loc = 0
    ticks = 0
    end_first_part = 0
    start_second_part = 0

    for j in range(n_vars):
        if vars_array[j].startswith('E ') or vars_array[j].startswith('e '):
            note = vars_array[j].split(" ")
            if len(note) >= 5:
                dec_val = int(note[3], 16)
                note_loc = note_loc + int(note[1])
                notes_array.append(note[0] + " " + str(note_loc) + " " + note[2] + " " + str(dec_val) + " " + str(note[4]))
        elif vars_array[j].startswith('<X') or vars_array[j].startswith('<x'):
            note = vars_array[j].split(" ")
            if len(note) >= 2:
                note_loc = note_loc + int(note[1])
                enc_text = vars_array[j + 1]
                enc_close = vars_array[j + 2]
                notes_array.append(note[0] + " " + str(note_loc) + " " + note[2] + " " + str(enc_text) + " " + enc_close)

                _temp_event = base64.b64decode(str(enc_text))
                _temp_event = _temp_event[2:]
                _temp_event = codecs.decode(_temp_event, 'utf-8')
        elif "HASDATA" in vars_array[j]:
            note = vars_array[j].split(" ")
            ticks = int(note[2])
            if ticks != correct_tqn:
                RPR_MB(f'One of the MIDI tracks isn\'t set to {correct_tqn} ticks per beat. This will break Magma. CAT will now exit', 'Invalid ticks per quarter', 0)
                return
        elif "<SOURCE MIDI" in vars_array[j]:
            end_first_part = j + 2  # it's the last element before the MIDI notes/events chunk
        elif "IGNTEMPO" in vars_array[j]:
            start_second_part = j - 1  # it's the first element after the MIDI notes/events chunk
    array_instrument = [ticks, notes_array, end_first_part, start_second_part]

    return array_instrument


def parse_notes_and_events(notes):  # instrument is the instrument shortname, NOT the instrument track number
    raw_notes = []  # An array containing only notes in raw format, notes on and off
    raw_events = []  # An array containing all text markers/events
    array_notes: [Note] = []  # An array containing only notes, with:
    # 0. 'E' or 'e' (unselected or selected), 1. location, 2. pitch, 3. velocity, 4. duration, 5. noteonoffchannel
    array_events: [MidiEvent] = []  # An array containing only text markers/events

    # First off we sort the notes from the markers, so it's easier to loop through notes
    for x in range(0, len(notes)):
        if notes[x].startswith('E') or notes[x].startswith('e'):
            raw_notes.append(notes[x])
        else:
            raw_events.append(notes[x])
    # Now we loop through the notes to remove all note off events and set a length for the notes

    for x in range(0, len(raw_notes)):
        note_bit = raw_notes[x].split(" ")
        if note_bit[2].startswith('9') and note_bit[4] != '00':
            for y in range(x, len(raw_notes)):
                cur_note = raw_notes[y].split(" ")
                if x != y and cur_note[3] == note_bit[3] and int(cur_note[1]) > int(note_bit[1]) and (cur_note[2].startswith('8') or cur_note[4] == '00'):
                    array_notes.append(Note(note_bit[0], int(note_bit[1]), int(note_bit[3]), note_bit[4], (int(cur_note[1]) - int(note_bit[1])), note_bit[2]))
                    break

    for x in range(0, len(raw_events)):
        note_bit = raw_events[x].split(" ")
        enc_text = note_bit[3]
        event_header = binascii.a2b_base64(enc_text)
        event_header = codecs.encode(event_header, 'hex_codec')
        event_header = codecs.decode(event_header, 'utf-8')
        event_header = event_header[:4]

        lyric = base64.b64decode(str(enc_text))
        lyric = lyric[2:]
        lyric = codecs.decode(lyric, 'utf-8')
        array_events.append(MidiEvent(note_bit[0], int(note_bit[1]), note_bit[2], str(lyric), note_bit[4], event_header))

    return [array_notes, array_events]


def parse_tempo_map(end_event_tick, ppq: int = 480) -> Tuple[List[Measure], List[TimeSigMarker]]:
    # This function creates measures array, an array containing all measures with their TS, BPM, starting point, etc.
    tsden_array = {'1048': 16, '983': 15, '917': 14, '851': 13, '786': 12, '720': 11, '655': 10, '589': 9, '524': 8, '458': 7, '393': 6, '327': 5, '262': 4, '196': 3, '131': 2, '65': 1}
    tsnum_array = {16: 577, 15: 41, 14: 505, 13: 969, 12: 433, 11: 897, 10: 361, 9: 825, 8: 289, 7: 753, 6: 217, 5: 681, 4: 145, 3: 609, 2: 73, 1: 537}
    # Examples:
    # 4/4: 262 and 148 (145 is 1, 145+3 is 4)
    # 7/8: 524 and 295 (289 is 1, 289+6 is 7)
    trkptr = RPR_CSurf_TrackFromID(0, 0)

    # Get Envelope Pointer:
    envptr = RPR_GetTrackEnvelopeByName(trkptr, 'Tempo map')

    envstr = ''
    # Get Envelope Data:
    envstate = RPR_GetSetEnvelopeState(envptr, envstr, max_len)

    nodes_array = []
    timesigchanges_array = []
    timesignature = '262148'  # By default it's 4/4
    chunk = "" + envstate[2]
    vars_array = chunk.splitlines()
    RPR_ShowConsoleMsg(f'VARS ARRAY: {vars_array}\n\n')

    temp_tempo = RPR_TimeMap_GetTimeSigAtTime(0, 0, 0, 0, 0)
    RPR_ShowConsoleMsg(f'TEMPO: {temp_tempo}\n\n')

    # Create an array of 0. seconds of the point, 1. BPM, 2. time signature num, 3. time signature den , 4. ticks since 0
    for j in range(0, len(vars_array)):
        if vars_array[j].startswith('PT '):
            node = vars_array[j].split(" ")

            node_array = [float(node[1]), float(node[2])]
            if len(node) > 4:
                if node[4] != '0':
                    timesignature = str(node[4])

            if len(timesignature) > 6:
                numerator = timesignature[4:]
                denominator = timesignature[:4]
            else:
                numerator = timesignature[3:]
                denominator = timesignature[:3]
            timesignature_denominator = tsden_array[denominator]
            timesignature_numerator = (int(numerator) - tsnum_array[timesignature_denominator]) + 1
            node_array.append(timesignature_numerator)
            node_array.append(timesignature_denominator)
            nodes_array.append(node_array)

    RPR_ShowConsoleMsg(f'node_array: {nodes_array}\n\n')

    # Create an array of TS changes: 0. BPM, 1. time signature num, 2. time signature den, 3. ticks passed since 0
    # decimal.Decimal(ticks_passed)
    ticks_passed = 0

    if len(nodes_array) == 0:
        return [], []

    if len(nodes_array) > 0:
        old_ts = str(nodes_array[0][2]) + str(nodes_array[0][3])
        timesigchanges_array.append(TimeSigMarker(0, nodes_array[0][2], nodes_array[0][3], 0, 1))
        nodes_array[0].append(0)
        for j in range(1, len(nodes_array)):

            ticks_per_second = (ppq * nodes_array[j - 1][1]) / 60
            time_passed = nodes_array[j][0] - nodes_array[j - 1][0]
            ticks_passed = (time_passed * ticks_per_second) + ticks_passed
            ticks_passed = round(ticks_passed, 10)
            nodes_array[j].append(ticks_passed)
            cur_ts = str(nodes_array[j][2]) + str(nodes_array[j][3])

            if old_ts != cur_ts:
                prev_marker = timesigchanges_array[-1]
                ticks_per_measure = correct_tqn * 4 * prev_marker.ts_num / prev_marker.ts_den
                n_measures = (round(ticks_passed) - prev_marker.tick) / ticks_per_measure
                RPR_ShowConsoleMsg(f'{ticks_per_measure} {n_measures}\n\n')
                timesigchanges_array.append(TimeSigMarker(0, nodes_array[j][2], nodes_array[j][3], round(ticks_passed), prev_marker.measure_idx + round(n_measures)))

            old_ts = str(nodes_array[j][2]) + str(nodes_array[j][3])

        # Loop through the TS array and for each time signature span find out duration and then divide by numerator and denominator. The result is the number of measures in that ts
        m = 0
        x = 0  # This is needed in case we only have one time signature event
        measures_array: List[Measure] = []

        for x in range(1, len(timesigchanges_array)):

            duration = float(timesigchanges_array[x][3] - timesigchanges_array[x - 1][3])
            duration = round(duration, 0)
            duration = int(duration)

            divider = ppq / (timesigchanges_array[x - 1][2] * 0.25)
            number_of_measures = round(round(duration / divider) / timesigchanges_array[x - 1][1], 0)
            number_of_measures = int(number_of_measures)

            ticks_per_measure = duration / number_of_measures
            ticks_per_beat = ticks_per_measure / timesigchanges_array[x][2]
            for j in range(0, number_of_measures):
                m += 1
                ticks_start = float((timesigchanges_array[x - 1][3]) + (j * ticks_per_measure))
                ticks_start = round(ticks_start, 0)
                ticks_start = int(ticks_start)
                measures_array.append(Measure(m, ticks_start, timesigchanges_array[x - 1][1], timesigchanges_array[x - 1][2], divider, bpm=0))

        # Now we need to add all measures from the last (or in some cases only) BPM marker to the end of the song, marked by the end event
        ticks_start = float(timesigchanges_array[len(timesigchanges_array) - 1][3])
        ticks_start = round(ticks_start, 0)
        ticks_start = int(ticks_start)
        ticks_per_measure = ppq / (timesigchanges_array[x][2] * 0.25)
        ticks = ticks_per_measure * timesigchanges_array[x][1]
        ticks_per_beat = ticks / timesigchanges_array[x][2]
        ticks_startmeasure = ticks_start
        loop_measure = 0
        while ticks_startmeasure < end_event_tick + ticks:  # The whole loop runs for one measure longer than the end event
            m += 1
            ticks_startmeasure = ticks_start + (ticks * loop_measure)
            loop_measure += 1
            measures_array.append(Measure(m, ticks_startmeasure, timesigchanges_array[x][1], timesigchanges_array[x][2], ticks_per_measure, bpm=0))

        # Now we add the BPM for each measure taking the BPM value of the measure from nodes_array
        for x in range(0, len(measures_array)):
            ticks_start = measures_array[x][1]
            measures_array[x].bpm = nodes_array[0][1]
            for j in reversed(list(range(0, len(nodes_array)))):
                if int(round(float(ticks_start), 0)) >= int(float(nodes_array[j][4])):
                    measures_array[x].bpm = nodes_array[j][1]
                    break

        return measures_array, timesigchanges_array
