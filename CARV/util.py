from dataclasses import dataclass


@dataclass
class TimeSignature:
    n: int = 4
    d: int = 4


@dataclass
class TimeSignatureChange:
    tick: int
    measure: int
    time_sig: TimeSignature


class TimeSignatureMap:
    def __init__(self):
        self.project_time_signature_location = []
        self.project_time_signature_location_measure = []
        self.project_time_signatures = []

    def add_time_signature(self, time_sig_tick: int, time_sig_measure: int, time_sig: TimeSignature):
        self.project_time_signature_location.append(time_sig_tick)
        self.project_time_signature_location_measure.append(time_sig_measure)
        self.project_time_signatures.append(time_sig)

    def __iter__(self):
        self.idx = 0
        return self

    def __reversed__(self):
        return reversed(list(self))  # lol

    def __next__(self):
        if len(self.project_time_signature_location) > self.idx:
            value = TimeSignatureChange(self.project_time_signature_location[self.idx],
                                        self.project_time_signature_location_measure[self.idx],
                                        self.project_time_signatures[self.idx])
            self.idx += 1
            return value
        else:
            raise StopIteration

    def tick_to_measure_str(self, note_location: int):
        _ppq = 480

        time_sig_change: TimeSignatureChange
        for time_sig_change in reversed(self):
            if note_location >= time_sig_change.tick:
                _location_base = time_sig_change.tick
                _location_offset = note_location - _location_base

                _location_num, _location_denom = time_sig_change.time_sig.n, time_sig_change.time_sig.d

                _divisor_factor = (_location_denom / 4)
                _divisor = (_ppq / _divisor_factor) * _location_num

                _time_1 = (_location_offset / _divisor) + time_sig_change.measure
                _time_2 = (_location_offset % _divisor) / (_ppq / (_location_denom / 4))

                return f'{int(_time_1 + 1)}.{int(_time_2 + 1)}'

        return "Error.Error"
