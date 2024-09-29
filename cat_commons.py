from enum import Enum
from collections import namedtuple


class Note:
    def __init__(self, is_selected: str = 'E', tick: int = 0, pitch: int = 0, velocity: str = '60', duration: int = 0, note_on_off_channel: str = '90'):
        if isinstance(is_selected, bool):
            self.is_selected = 'e' if is_selected else 'E'
        else:
            if is_selected not in ['e', 'E']:
                raise ValueError(f'Invalid is_selected attribute in Note object, must be \'e\' or \'E\'')
            self.is_selected = is_selected
        self.tick: int = tick
        self.pitch: int = pitch
        self.velocity: str = velocity
        self.duration = duration
        self.note_on_off_channel = note_on_off_channel

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise TypeError('Note object is unsliceable')
        if not isinstance(item, int):
            raise ValueError(f'Invalid index: {item}')
        if 6 <= item < 0:
            raise ValueError(f'Invalid index: {item}')
        if item == 0:
            return self.is_selected
        elif item == 1:
            return self.tick
        elif item == 2:
            return self.pitch
        elif item == 3:
            return self.velocity
        elif item == 4:
            return self.duration
        elif item == 5:
            return self.note_on_off_channel
        return None

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise TypeError('Note object is unsliceable')
        if not isinstance(key, int):
            raise ValueError(f'Invalid index: {key}')
        if 6 <= key < 0:
            raise ValueError(f'Invalid index: {key}')
        if key == 0:
            self.is_selected = value
        elif key == 1:
            self.tick = value
        elif key == 2:
            self.pitch = value
        elif key == 3:
            self.velocity = value
        elif key == 4:
            self.duration = value
        elif key == 5:
            self.note_on_off_channel = value
        return None

    def __iter__(self):
        return iter((self.is_selected, self.tick, self.pitch, self.velocity, self.duration, self.note_on_off_channel))

    def __repr__(self):
        return f'NOTE [Pitch:{self.pitch}, Tick:{self.tick}]'


class MidiEventType(Enum):
    TEXT_MARKER = 'ff01'
    TRACK_NAME = 'ff03'
    LYRICS = 'ff05'


class MidiEvent:
    def __init__(self, is_selected: str = '<X', tick: int = 0, pre_text: str = '0', event_text: str = '', post_text: str = '>', event_type_code: str = 'ff01'):
        if isinstance(is_selected, bool):
            self.is_selected = '<x' if is_selected else '<X'
        else:
            if is_selected not in ['<x', '<X']:
                raise ValueError(f'Invalid is_selected attribute in MidiEvent object, must be \'<x\' or \'<X\', not {is_selected}')
            self.is_selected = is_selected
        self.tick = tick
        self.pre_text = pre_text
        self.event_text = event_text
        self.post_text = post_text
        try:
            self.event_type_code = event_type_code
            MidiEventType(event_type_code)
        except Exception as e:
            raise ValueError(f'Invalid MidiEvent type code: {event_type_code}')

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise TypeError('MidiEvent object is unsliceable')
        if not isinstance(item, int):
            raise ValueError(f'Invalid index: {item}')
        if 6 <= item < 0:
            raise ValueError(f'Invalid index: {item}')
        if item == 0:
            return self.is_selected
        elif item == 1:
            return self.tick
        elif item == 2:
            return self.pre_text
        elif item == 3:
            return self.event_text
        elif item == 4:
            return self.post_text
        elif item == 5:
            return self.event_type_code
        return None

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise TypeError('MidiEvent object is unsliceable')
        if not isinstance(key, int):
            raise ValueError(f'Invalid index: {key}')
        if 6 <= key < 0:
            raise ValueError(f'Invalid index: {key}')
        if key == 0:
            self.is_selected = value
        elif key == 1:
            self.tick = value
        elif key == 2:
            self.pre_text = value
        elif key == 3:
            self.event_text = value
        elif key == 4:
            self.post_text = value
        elif key == 5:
            self.event_type_code = value
        return None

    def get_midi_event_type(self) -> MidiEventType:
        return MidiEventType(self.event_type_code)

    def __repr__(self):
        return f'EVENT [EventType: {self.get_midi_event_type().name}, Text: {self.event_text}, Tick:{self.tick}]'


class Measure:
    def __init__(self, measure_idx, tick_at_start, ts_den, ts_num, ticks_per_beat, bpm):
        self.measure_idx = measure_idx
        self.tick_at_start = tick_at_start
        self.ts_den = ts_den
        self.ts_num = ts_num
        self.ticks_per_beat = ticks_per_beat
        self.bpm = bpm

    def __getitem__(self, item):
        if isinstance(item, slice):
            raise TypeError('Measure object is unsliceable')
        if not isinstance(item, int):
            raise ValueError(f'Invalid index: {item}')
        if 6 <= item < 0:
            raise ValueError(f'Invalid index: {item}')
        if item == 0:
            return self.measure_idx
        elif item == 1:
            return self.tick_at_start
        elif item == 2:
            return self.ts_den
        elif item == 3:
            return self.ts_num
        elif item == 4:
            return self.ticks_per_beat
        elif item == 5:
            return self.bpm
        return None

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise TypeError('Measure object is unsliceable')
        if not isinstance(key, int):
            raise ValueError(f'Invalid index: {key}')
        if 6 <= key < 0:
            raise ValueError(f'Invalid index: {key}')
        if key == 0:
            self.measure_idx = value
        elif key == 1:
            self.tick_at_start = value
        elif key == 2:
            self.ts_den = value
        elif key == 3:
            self.ts_num = value
        elif key == 4:
            self.ticks_per_beat = value
        elif key == 5:
            self.bpm = value
        return None

    def __iter__(self):
        return iter((self.measure_idx, self.tick_at_start, self.ts_den, self.ts_num, self.ticks_per_beat, self.bpm))

    def __repr__(self):
        return f'M{self.measure_idx} [Tick: {int(self.tick_at_start)}, TS: {self.ts_num}/{self.ts_den}, BPM: {self.bpm}]'


MBTEntry = namedtuple('MBTEntry', field_names=['measure_idx', 'beat', 'ticks_from_beat', 'ticks_from_measure_start'])
