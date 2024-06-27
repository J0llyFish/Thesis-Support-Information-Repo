from msilib.schema import ComboBox
from tkinter import *
from tkinter.ttk import Combobox
from requests import get
from os import listdir

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
# local resource
import IR_reader_General
from IR_reader_General import Data_node

## data 
ptr = -1 # pointer to specified IR data
ptr_sub = 0
#ir_list = IR_reader.read_file_csv('IR_index.csv')
## window basics
IR_PATH_EXP = "GAS\\" # folder for downloaded spectra from NIST
IR_PATH_SIM = 'SP_MM_INCHI\\' # folder for simulated spectra
cas_list = listdir(IR_PATH_EXP)

plt.style.use('dark_background')
form = Tk()
form.title("IR Viewer")
form.geometry("1280x768+200+10")
form_header = Label(form,text='IR Viewer')

# title information
infor = StringVar()
infor.set('IR Viewer')

# information on top
f = Figure(figsize=(5, 4), dpi=100)
label = Label(form,textvariable=infor,anchor='w').pack()
#spectrum = IR_reader.Spectrum('IRDB\\COB_GAS\\110-86-1.jdx')

## text box for input cas
text_cas = Text(form,height=1,width=10)
choosen_ir_type = StringVar()

text_base_line = Text(form,height=1,width=10)
#text_base_line.delete(0,"end")
text_base_line.insert('1.0', "1")
text_IR_index = Text(form,height=1,width=10)
is_show_dft = IntVar()
##
f_plot=f.add_subplot(111)
#f_plot.plot(spectrum.spectrum_wave_number,spectrum.spectrum_signal)

canvs = FigureCanvasTkAgg(f, form)
canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

def refresh_info(additional_info=''):
    global infor , ptr , cas_list
    #mode = ''
    infor.set(str(ptr)+':'+cas_list[ptr].strip('.jdx')+additional_info)
    # if ptr_sub == 0:
    #     mode = '[Gas]'
    # elif ptr_sub == 1:
    #     mode = '[Liquid]'
    # elif ptr_sub == 2:
    #     mode = '[Solution]'
    # if ir_list[ptr].has_selected == "False":
    #     infor.set(str(ptr)+':'+cas_list[ptr]+additional_info)
    # else:
    #     infor.set(str(ptr)+':'+ir_list[ptr].nist_name+mode+ir_list[ptr].nist_cas+': has been selected : '+ir_list[ptr].has_selected+additional_info)

def refresh_spectrum(nist_cas,ptr_sub):
    global f_plot ,canvs , infor , is_show_dft
    spectrum = None
    #try:
    spectrum = IR_reader_General.Spectrum(IR_PATH_EXP+nist_cas.strip('.jdx')+'.jdx')
    # after spectrum was generated , print it to window
    if spectrum and spectrum.message == 'Spectrum Generated Successful':
        f_plot.clear()
        f_plot.plot(spectrum.spectrum_wave_number,spectrum.spectrum_signal,c='g')
        if is_show_dft.get() == 1:
            try:
                spectrum_DFT = IR_reader_General.Spectrum(IR_PATH_SIM+nist_cas.strip('.jdx')+'.dx')
                f_plot.plot(spectrum_DFT.spectrum_wave_number,spectrum_DFT.spectrum_signal,c='b')
            except:
                print("no Simulated IR found")
        #f_plot.plot(spectrum.spectrum_wave_number,[float(cas_list[ptr]) for i in spectrum.spectrum_wave_number],c='r')
        f_plot.invert_xaxis()
        f_plot.grid(True)
        f_plot.set_ylim([0, 1.2])
        canvs.draw()
        # print origin # can be modify with Spectrum class in IR_reader
        return ' origin:'+spectrum.ORIGIN
    else:
        f_plot.clear()
        #f_plot.plot([spectrum.min_wave_number,spectrum.max_wave_number],[0,0])
        canvs.draw()
        print('spectrum printing failed')
        return ' '
    # except:
    #     print('this plot cannot be read')
def next_spectrum(): # run this fcn to let pointer point to correct data
    global ptr , ptr_sub ,cas_list
    if ptr == len(cas_list)-1:
        ptr = 0
    else:
        ptr += 1

def prev_spectrum(): # run this fcn to let pointer point to correct data
    global ptr , ptr_sub ,cas_list
    if ptr <= 0:
        ptr = len(cas_list)-1
    else:
        ptr -= 1
        
def set_spectrum_usage():
    # if ir_list[ptr].has_selected == "False":
    #     if ptr_sub == 0:
    #         ir_list[ptr].has_selected = "GAS"
    #     elif ptr_sub == 1:
    #         ir_list[ptr].has_selected = "LIQUID"
    #     elif ptr_sub == 2:
    #         ir_list[ptr].has_selected = "SOLUTION"
    # else:
    #     ir_list[ptr].has_selected = "False"
    # #print(ir_list[ptr].has_selected)
    refresh_info()

def next():
    global ptr_sub , ptr
    next_spectrum()
    refresh_info(refresh_spectrum(cas_list[ptr],ptr_sub))

def prev():
    global ptr_sub , ptr
    prev_spectrum()
    refresh_info(refresh_spectrum(cas_list[ptr],ptr_sub))    

# def save_to_file():
#     IR_reader.write_IR_index_file(ir_list,'generated_input_data\\IR_index_opt.csv')

def generate_input_data():
    IR_reader_General.generate_input_data(IR_PATH_EXP,IR_PATH_SIM)
    
# def export_full_table():
#     IR_reader.export_full_table(ir_list,'generated_input_data\\IR_stats_table.csv')

def Read_IR_by_cas():
    #try:
        refresh_spectrum(text_cas.get("1.0",END).strip('\n'),0)
    #except:
        #print('wrong cas')
        #print(text_cas.get("1.0",END).strip('\n'))
def show_sim():
    global ptr
    refresh_spectrum(cas_list[ptr],0)
    
# def Set_base_line():
#     global ptr
#     ir_list[ptr].base_line = text_base_line.get("1.0",END).strip('\n')
#     refresh_spectrum(ir_list[ptr].nist_cas,0)
# def set_ir_index():
#     global ptr
#     ptr = int(text_IR_index.get("1.0",END).strip('\n'))
    
#     refresh_info(refresh_spectrum(ir_list[ptr].nist_cas,0))

Button(form, text='previous spectrum', command=prev).pack(side=LEFT)
Button(form, text='next spectrum', command=next).pack(side=LEFT)
#Button(form, text='save to Index', command=save_to_file).pack(side=LEFT)
## special buttons
#Button(form, text='export full table', command=export_full_table).pack(side=LEFT)
Button(form, text='Read IR by cas', command=Read_IR_by_cas).pack(side=LEFT)
text_cas.pack(side=LEFT,pady=20)
# cmb = Combobox(form,textvariable=choosen_ir_type,width=10)
# cmb["value"]=("GAS","LIQUID","SOLUTION")
# cmb.pack(side=LEFT,pady=20)
# Button(form, text='Set Base Line=>', command=Set_base_line).pack(side=LEFT)
# text_base_line.pack(side=LEFT,pady=20)
# Button(form, text='set spectrum usage', command=set_spectrum_usage).pack(side=LEFT)
#text_IR_index.pack(side=LEFT,pady=20)
# Button(form, text='<=set IR index', command=set_ir_index).pack(side=LEFT)
show_Sim=Checkbutton(form,text='show Sim',variable=is_show_dft,command=show_sim,onvalue=1,offvalue=0).pack(side=LEFT)
Button(form, text='generate input file', command=generate_input_data).pack(side=LEFT)
form.mainloop() # start running 
