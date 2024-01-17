from reaper_python import *
import C3toolbox
import sys
import os
sys.argv=["Main"]
import tkinter

global instrument_var
global expression_var
global fldRowTxt
global form

def execute():
    global form
    instrument = str(instrument_var.get())
    expression = str(expression_var.get())
    instrument = C3toolbox.array_instruments[instrument]
    if instrument == "PART REAL_KEYS":
        instrument = "PART REAL_KEYS_X"
    pause = str(fldRowTxt.get())
    if pause == 'default':
        pause = 0
    C3toolbox.startup()
    C3toolbox.create_animation_markers(instrument, expression, pause, 0) #instrument, expression, pause
    form.destroy()


def launch():
    global instrument_var
    global expression_var
    global fldRowTxt
    global form
    C3toolbox.startup()
    form = tkinter.Tk()
    form.wm_title('Create animation markers')

    instrument_name = C3toolbox.get_trackname()

    if instrument_name in C3toolbox.array_dropdownid:
        instrument_id = C3toolbox.array_dropdownid[instrument_name]
    else:
        instrument_id = 0
    
    helpLf = tkinter.Frame(form)
    helpLf.grid(row=0, column=1, sticky='NS', padx=5, pady=5)

    inFileLbl = tkinter.Label(helpLf, text="Select instrument")
    inFileLbl.grid(row=1, column=1, sticky='E', padx=5, pady=2)

    OPTIONS = ["Drums", "Guitar", "Bass", "Keys", "Pro Keys", "2x Drums", "Rhythm", "Vocals"]

    instrument_var = tkinter.StringVar(helpLf)
    instrument_var.set(OPTIONS[instrument_id]) # default value

    instrumentOpt = tkinter.OptionMenu(*(helpLf, instrument_var) + tuple(OPTIONS))
    instrumentOpt.grid(row=0, column=1, columnspan=1, sticky="WE", pady=3)

    expressionLbl = tkinter.Label(helpLf, text="Select expression")
    expressionLbl.grid(row=1, column=2, sticky='E', padx=5, pady=2)

    OPTIONS = ["play", "mellow", "intense"]

    expression_var = tkinter.StringVar(helpLf)
    expression_var.set(OPTIONS[0]) # default value

    expressionOpt = tkinter.OptionMenu(*(helpLf, expression_var) + tuple(OPTIONS))
    expressionOpt.grid(row=0, column=2, columnspan=1, sticky="WE", pady=3)

    fldLbl = tkinter.Label(helpLf, \
                           text="Pause in tick between notes to trigger an idle event")
    fldLbl.grid(row=1, column=3, padx=5, pady=2, sticky='W')
    var = tkinter.StringVar()
    fldRowTxt = tkinter.Entry(helpLf, textvariable=var)
    var.set('default')
    fldRowTxt.grid(row=0, column=3, columnspan=1, padx=5, pady=2, sticky='W')

    halveselBtn = tkinter.Button(helpLf, text="Create markers", command= lambda: execute()) 
    halveselBtn.grid(row=0, column=4, rowspan=2, sticky="NS", padx=5, pady=2)

    logo = tkinter.Frame(form, bg="#000")
    logo.grid(row=2, column=0, columnspan=10, sticky='WE', \
                 padx=0, pady=0, ipadx=0, ipady=0)

    path = os.path.join( sys.path[0], "banner.gif" )
    img = tkinter.PhotoImage(file=path)
    imageLbl = tkinter.Label(logo, image = img, borderwidth=0)
    imageLbl.grid(row=0, column=0, rowspan=2, sticky='E', padx=0, pady=0)

    form.mainloop()
    
if __name__ == '__main__':
    #launch()
    C3toolbox.startup()
    C3toolbox.create_animation_markers("PART VOCALS", "play", 0, 0) #instrument, expression, pause, mute
