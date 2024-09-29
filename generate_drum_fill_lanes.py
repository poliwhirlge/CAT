from reaper_python import RPR_ShowConsoleMsg
from parsing.parse_reaper_project import parse_project


def launch():
    midi_project = parse_project()
    drum_track = midi_project.parse_track('PART DRUMS')

    RPR_ShowConsoleMsg(f'Drum track {len(drum_track.notes)}\n')
    RPR_ShowConsoleMsg(f'Drum events {len(drum_track.events)}\n')
    RPR_ShowConsoleMsg(f'Measures: {midi_project.measures}\n')
    RPR_ShowConsoleMsg(f'MBT 10000: {midi_project.mbt(10000)}\n')
    RPR_ShowConsoleMsg(f'MBT 30000: {midi_project.mbt(30000)}\n')
