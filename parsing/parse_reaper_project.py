import base64
import binascii
import codecs
import traceback

import C3notes
from collections import defaultdict
from reaper_python import RPR_CountMediaItems, RPR_GetMediaItem, RPR_GetMediaItem_Track, RPR_GetSetMediaTrackInfo_String, RPR_GetSetItemState, RPR_ShowConsoleMsg, RPR_MB
from cat_commons import MidiProject, MidiTrack, Note, MidiEvent


max_len = 1048576


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

    ticks, notes_array, end_first_part, start_second_part = array_instrument_data
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
            if ticks != 480:
                RPR_MB("One of the MIDI tracks isn't set to 480 ticks per beat. This will break Magma. CAT will now exit", "Invalid ticks per quarter", 0)
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
