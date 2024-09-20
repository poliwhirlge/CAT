# CAT 1.3.0 dev
from reaper_python import *
import C3toolbox
import create_beattrack
import create_animation_markers
import filter_notes
import remove_notes
import create_triplets
import fix_sustains
import simplify_roll
import remove_kick
import flip_discobeat
import unflip_discobeat
import single_pedal
import drums_animations
import reduce_5lane
import auto_animations
import polish_notes
import reduce_chords
import reduce_singlenotes
import add_slides
import tubes_space
import remove_invalid_chars
import capitalize_first
import check_capitalization
import unpitch
import pitch
import hide_lyrics
import create_phrase_markers
import trim_phrase_markers
import compact_harmonies
import add_vocalsoverdrive
import fix_textevents
import cleanup_phrases
import compound_phrases
import copy_od_solo
import single_snare
import auto_cleanup
import vocals_cleanup
import create_keys_animations
import edit_by_mbt
import cleanup_notes
import export_lyrics
import show_lyrics
import remove_notes_prokeys
import pgrootnotes
import fhp
import pg_copy_od_solo
import remove_notes_pg
import create_singalong
import reduce_by_pattern

import os
import sys

sys.argv = ["Main"]
import tkinter

global root


def execute_this(function):
    global root
    if function == 'reduce_drums':
        root.destroy()
        reduce_5lane.launch('PART DRUMS')
    elif function == 'reduce_5lane':
        root.destroy()
        reduce_5lane.launch('5LANE')
    else:
        subwindow = eval(function)
        root.destroy()
        subwindow.launch()


class GenerateProKeysRangeMarkers:
    @staticmethod
    def launch():
        global root
        root.destroy()
        C3toolbox.startup()
        C3toolbox.generate_pro_keys_range_markers()


def RunCARV():
    global root
    root.destroy()

    tempDirectory = (str(sys.path[0]) + "/CARV")
    sys.path.insert(0, tempDirectory)
    import RBNCheck


if __name__ == '__main__':
    root = tkinter.Tk()
    root.wm_title('C3 Reaper Automation Project')

    secVarious = tkinter.LabelFrame(root, text=" Animation and System: ")
    secVarious.grid(row=0, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    beattrackBtn = tkinter.Button(secVarious, text="Create BEAT track", command=lambda: execute_this('create_beattrack'))
    beattrackBtn.grid(row=0, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    animationsBtn = tkinter.Button(secVarious, text="Create animations events", command=lambda: execute_this('create_animation_markers'))
    animationsBtn.grid(row=0, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    drumsanimationsBtn = tkinter.Button(secVarious, text="Create drums animations", command=lambda: execute_this('drums_animations'))
    drumsanimationsBtn.grid(row=0, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    prokeysanimationsBtn = tkinter.Button(secVarious, text="Create pro keys animations", command=lambda: execute_this('create_keys_animations'))
    prokeysanimationsBtn.grid(row=0, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    invalidmarkersBtn = tkinter.Button(secVarious, text="Remove invalid markers", command=lambda: execute_this('filter_notes'))
    invalidmarkersBtn.grid(row=0, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    sec5lane = tkinter.LabelFrame(root, text=" 5-lane: ")
    sec5lane.grid(row=1, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    removenotesBtn = tkinter.Button(sec5lane, text="Remove notes", command=lambda: execute_this('remove_notes'))
    removenotesBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    tripleBtn = tkinter.Button(sec5lane, text="Reduce to triple hits", command=lambda: execute_this('create_triplets'))
    tripleBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    sustainsBtn = tkinter.Button(sec5lane, text="Fix sustains", command=lambda: execute_this('fix_sustains'))
    sustainsBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    rollsBtn = tkinter.Button(sec5lane, text="Fix trills/rolls", command=lambda: execute_this('simplify_roll'))
    rollsBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    editbymbtBtn = tkinter.Button(sec5lane, text="Edit by MBT", command=lambda: execute_this('edit_by_mbt'))
    editbymbtBtn.grid(row=1, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    polishBtn = tkinter.Button(sec5lane, text="Polish notes", command=lambda: execute_this('polish_notes'))
    polishBtn.grid(row=2, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    chordsBtn = tkinter.Button(sec5lane, text="Reduce chords", command=lambda: execute_this('reduce_chords'))
    chordsBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    singlenotesBtn = tkinter.Button(sec5lane, text="Lower frets complexity", command=lambda: execute_this('reduce_singlenotes'))
    singlenotesBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    prosoloodBtn = tkinter.Button(sec5lane, text="Add missing solo/OD to pro", command=lambda: execute_this('copy_od_solo'))
    prosoloodBtn.grid(row=2, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    cleanupnotesBtn = tkinter.Button(sec5lane, text="Clean up notes' length", command=lambda: execute_this('cleanup_notes'))
    cleanupnotesBtn.grid(row=2, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    reducepatternBtn = tkinter.Button(sec5lane, text="Reduce by pattern", command=lambda: execute_this('reduce_by_pattern'))
    reducepatternBtn.grid(row=3, column=1, columnspan=1, sticky="WE", padx=5, pady=2)

    prokeysreduceBtn = tkinter.Button(sec5lane, text="Reduce pro keys note density based on 5-lane", command=lambda: execute_this('remove_notes_prokeys'))
    prokeysreduceBtn.grid(row=3, column=2, columnspan=3, sticky="WE", padx=5, pady=2)

    secDrums = tkinter.LabelFrame(root, text=" Drums: ")
    secDrums.grid(row=2, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    removekicksBtn = tkinter.Button(secDrums, text="Remove kicks", command=lambda: execute_this('remove_kick'))
    removekicksBtn.grid(row=2, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    singlesnareBtn = tkinter.Button(secDrums, text="Leave single snare hits", command=lambda: execute_this('single_snare'))
    singlesnareBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    flipBtn = tkinter.Button(secDrums, text="Flip disco beats", command=lambda: execute_this('flip_discobeat'))
    flipBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    unflipBtn = tkinter.Button(secDrums, text="Unflip disco beats", command=lambda: execute_this('unflip_discobeat'))
    unflipBtn.grid(row=2, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    doublepedalBtn = tkinter.Button(secDrums, text="Reduce 2x bass pedal", command=lambda: execute_this('single_pedal'))
    doublepedalBtn.grid(row=2, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    secVocals = tkinter.LabelFrame(root, text=" Vocals: ")
    secVocals.grid(row=3, columnspan=5, sticky='WE', \
                   padx=5, pady=5, ipadx=5, ipady=5)

    addslidesBtn = tkinter.Button(secVocals, text="Add slides", command=lambda: execute_this('add_slides'))
    addslidesBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    spacetubesBtn = tkinter.Button(secVocals, text="Add space between tubes", command=lambda: execute_this('tubes_space'))
    spacetubesBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    punctuationBtn = tkinter.Button(secVocals, text="Remove illegal punctuation", command=lambda: execute_this('remove_invalid_chars'))
    punctuationBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    capitalizeBtn = tkinter.Button(secVocals, text="Capitalize first lyric in phrases", command=lambda: execute_this('capitalize_first'))
    capitalizeBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    checkcapsBtn = tkinter.Button(secVocals, text="Check/fix capitalization", command=lambda: execute_this('check_capitalization'))
    checkcapsBtn.grid(row=1, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    unpitchBtn = tkinter.Button(secVocals, text="Change notes to non-pitched", command=lambda: execute_this('unpitch'))
    unpitchBtn.grid(row=2, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    hidelyricsBtn = tkinter.Button(secVocals, text="Hide lyrics", command=lambda: execute_this('hide_lyrics'))
    hidelyricsBtn.grid(row=2, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    createphraseBtn = tkinter.Button(secVocals, text="Create phrase markers", command=lambda: execute_this('create_phrase_markers'))
    createphraseBtn.grid(row=2, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    trimphraseBtn = tkinter.Button(secVocals, text="Trim phrase markers", command=lambda: execute_this('trim_phrase_markers'))
    trimphraseBtn.grid(row=2, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    harmoniesBtn = tkinter.Button(secVocals, text="Compact harmonies", command=lambda: execute_this('compact_harmonies'))
    harmoniesBtn.grid(row=2, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    overdriveBtn = tkinter.Button(secVocals, text="Add overdrive phrases", command=lambda: execute_this('add_vocalsoverdrive'))
    overdriveBtn.grid(row=3, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    fixtexteventsBtn = tkinter.Button(secVocals, text="Fix text events", command=lambda: execute_this('fix_textevents'))
    fixtexteventsBtn.grid(row=3, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    cleanupphrasesBtn = tkinter.Button(secVocals, text="Delete empty phrases", command=lambda: execute_this('cleanup_phrases'))
    cleanupphrasesBtn.grid(row=3, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    compactphrasesBtn = tkinter.Button(secVocals, text="Compact phrases", command=lambda: execute_this('compound_phrases'))
    compactphrasesBtn.grid(row=3, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    unpitchBtn = tkinter.Button(secVocals, text="Change notes to pitched", command=lambda: execute_this('pitch'))
    unpitchBtn.grid(row=3, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    exportlyricsBtn = tkinter.Button(secVocals, text="Export lyrics", command=lambda: execute_this('export_lyrics'))
    exportlyricsBtn.grid(row=4, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    showlyricsBtn = tkinter.Button(secVocals, text="Show lyrics", command=lambda: execute_this('show_lyrics'))
    showlyricsBtn.grid(row=4, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    createSingBtn = tkinter.Button(secVocals, text="Create sing-a-long notes", command=lambda: execute_this('create_singalong'))
    createSingBtn.grid(row=4, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    secSupersets = tkinter.LabelFrame(root, text=" Supersets: ")
    secSupersets.grid(row=4, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    reductionsBtn = tkinter.Button(secSupersets, text="Automatic reductions (5-lane)", command=lambda: execute_this('reduce_5lane'))
    reductionsBtn.grid(row=4, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    reductionsBtn = tkinter.Button(secSupersets, text="Automatic reductions (drums)", command=lambda: execute_this('reduce_drums'))
    reductionsBtn.grid(row=4, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    animationsBtn = tkinter.Button(secSupersets, text="Automatic animations", command=lambda: execute_this('auto_animations'))
    animationsBtn.grid(row=4, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    vocalsBtn = tkinter.Button(secSupersets, text="Vocals clean up", command=lambda: execute_this('vocals_cleanup'))
    vocalsBtn.grid(row=4, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    generalBtn = tkinter.Button(secSupersets, text="General clean up", command=lambda: execute_this('auto_cleanup'))
    generalBtn.grid(row=4, column=5, rowspan=1, sticky="WE", padx=5, pady=2)

    secPGB = tkinter.LabelFrame(root, text=" Pro Guitar/Bass: ")
    secPGB.grid(row=5, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    GenerateRootNotesBtn = tkinter.Button(secPGB, text="Generate Root Notes", command=lambda: execute_this('pgrootnotes'))
    GenerateRootNotesBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    GenerateFretHandPositionsBtn = tkinter.Button(secPGB, text="Generate Fret Hand Positions", command=lambda: execute_this('fhp'))
    GenerateFretHandPositionsBtn.grid(row=1, column=2, rowspan=1, sticky="WE", padx=5, pady=2)

    CopyODSoloFromBasicGtrBtn = tkinter.Button(secPGB, text="Copy OD/Solo Markers from 5-lane", command=lambda: execute_this('pg_copy_od_solo'))
    CopyODSoloFromBasicGtrBtn.grid(row=1, column=3, rowspan=1, sticky="WE", padx=5, pady=2)

    ReduceFromBasicGtrBtn = tkinter.Button(secPGB, text="Reduce from 5-lane", command=lambda: execute_this("remove_notes_pg"))
    ReduceFromBasicGtrBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    sec_pro_keys = tkinter.LabelFrame(root, text=' Pro Keys: ')
    sec_pro_keys.grid(row=6, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    generate_pro_keys_ranges = tkinter.Button(sec_pro_keys, text="Generate Pro Keys Range Markers", command=lambda: GenerateProKeysRangeMarkers.launch())
    generate_pro_keys_ranges.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    secValidation = tkinter.LabelFrame(root, text=" Validation: ")
    secValidation.grid(row=7, columnspan=5, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)

    CARVBtn = tkinter.Button(secValidation, text="Run C3 Automatic Rules Validator (CARV)", command=RunCARV)
    CARVBtn.grid(row=1, column=1, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = tkinter.Frame(root, bg="#000")
    logo.grid(row=9, column=0, columnspan=10, sticky='WE', padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join(sys.path[0], "banner.gif")
    img = tkinter.PhotoImage(file=path)
    imageLbl = tkinter.Label(logo, image=img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    root.mainloop()
