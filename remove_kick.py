from reaper_python import *
import C3toolbox
import sys
import os
import tkinter

global level_var
global instrument_var
global what_var
global form

sys.argv = ["Main"]

def execute(selected):
    global level_var
    global instrument_var
    global what_var
    global form
    what_array = {'Any note': 'a', 'Snare': 's', 'Any tom': 't', 'Any tom or snare': 'p', 'Multiple gems': 'm'}
    level = str(level_var.get())
    instrument = str(instrument_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    what = str(what_var.get())
    what = what_array[what]

    if instrument == "PART REAL_KEYS":
        instrument = instrument + C3toolbox.array_levels[level][1]
    C3toolbox.startup()
    C3toolbox.remove_kick(instrument, C3toolbox.array_levels[level][0], what, selected)
    form.destroy()


def launch():
    global level_var
    global instrument_var
    global what_var
    global form

    C3toolbox.startup()
    form = tkinter.Tk()
    form.wm_title('Remove kicks')

    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=1, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "2x Drums"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[0])  # default value

    instrumentOpt = tkinter.OptionMenu(*(helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    levelLbl = tkinter.Label(helpLf, text="Select level")
    levelLbl.grid(row=1, column=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["Expert", "Hard", "Medium", "Easy"]

    level_var = tkinter.StringVar(helpLf)
    level_var.set(OPTIONS[-1])  # default value

    levelOpt = tkinter.OptionMenu(*(helpLf, level_var) + tuple(OPTIONS))
    levelOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    whatLbl = tkinter.Label(helpLf, text="Remove kicks when paired with...")
    whatLbl.grid(row=1, column=3, sticky='E', padx=5, pady=2)

    OPTIONS = ["Any note", "Snare", "Any tom", "Any tom or snare", 'Multiple gems']

    what_var = tkinter.StringVar(helpLf)
    what_var.set(OPTIONS[0])  # default value

    whatOpt = tkinter.OptionMenu(*(helpLf, what_var) + tuple(OPTIONS))
    whatOpt.grid(row=0, column=3, columnspan=1, sticky="WE", pady=3)

    allBtn = tkinter.Button(helpLf, text="Remove kicks", command=lambda: execute(0))
    allBtn.grid(row=0, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    selBtn = tkinter.Button(helpLf, text="Remove selected kicks", command=lambda: execute(1))
    selBtn.grid(row=1, column=4, rowspan=1, sticky="WE", padx=5, pady=2)

    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=2, column=0, columnspan=10, sticky='WE', padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join(sys.path[0], "banner.gif")
    img = tkinter.PhotoImage(file=path)
    imageLbl = tkinter.Label(logo, image=img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.grab_release()
    form.mainloop()
    form.quit()


if __name__ == '__main__':
    launch()
