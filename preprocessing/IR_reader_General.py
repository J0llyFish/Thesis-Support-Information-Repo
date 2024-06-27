
#from IR_Download import Data_node

from cmath import log
from math import exp
import math 
import peakutils
import numpy as np
from os import listdir
from Spectrum import Spectrum

class Data_node:
    def __init__(self):
        self.index_num = ''
        self.nist_name  = ''
        self.nist_cas = ''
        self.nist_weight = ''
        self.nist_has_cob_GAS = False
        self.nist_has_cob_LIQUID = False
        self.nist_has_cob_SOLUTION = False
        self.has_selected = False
        self.has_GAS = False
        #self.nist_has_cob_SOLID = False
        #self.non_cob_GAS = False
        #self.non_cob_LIQUID = False
        #self.non_cob_SOLID = False



# first thing to do ,load input chemical compound list
def read_file_csv(file_name):
    #open file with read only mode (you should not write any think with this mode)
    fr = open(file_name,'r')
    # build a list for store all data read from file 
    data = list()
    title_tags = fr.readline() # tags, no use
    # while loop for load data ,try is used for prevent loading error ()
    new_line = fr.readline()
    try:
        while new_line != '':
            new_node = Data_node()
            if '"' in new_line:
                chem_name = new_line.split('"')[1]
                new_line = (new_line.split('"')[0]+new_line.split('"')[2]).split(',')
                new_line[1] = '"'+chem_name+'"'
            else:
                new_line = new_line.strip('\n').split(',')
            new_node.index_num,new_node.nist_name = new_line[0],new_line[1]
            new_node.nist_cas,new_node.nist_weight = new_line[2],new_line[3]
            
            new_node.nist_has_cob_GAS = new_line[4]
            new_node.nist_has_cob_LIQUID = new_line[5]
            new_node.nist_has_cob_SOLUTION = new_line[6]
            new_node.has_selected = new_line[7].strip('\n')
            new_node.has_GAS = new_line[8].strip('\n')
            new_node.base_line = new_line[9].strip('\n')
            data.append(new_node)
            new_line = fr.readline()
    except:
        print('exception occur when reading')
        fr.close()
    fr.close()
    return data

def write_IR_index_file(data,file_name):
    fw = open(file_name,'w')
    fw.write('index_num,nist_name,nist_cas,nist_weight,has_gas,has_liquid,has_solution,hes_selected,has_GAS,base_line\n')
    for i in range(len(data)):
    #for i in range(13):
        try:
            new_line = ''
            new_line += data[i].index_num+','+data[i].nist_name
            new_line += ','+data[i].nist_cas + ',' + data[i].nist_weight.strip('\n') #+ '\n'
            new_line += ','+str(data[i].nist_has_cob_GAS)
            new_line += ','+str(data[i].nist_has_cob_LIQUID)
            new_line += ','+str(data[i].nist_has_cob_SOLUTION)
            new_line += ','+str(data[i].has_selected)
            new_line += ','+str(data[i].has_GAS)
            new_line += ','+str(data[i].base_line)
            new_line += '\n'
            fw.write(new_line)
        except:
            print(new_line+' error when writing\n')
    fw.flush()
    fw.close()
# generate spectrum data in a specific format for futher usage
# target = x / label = y
# for INCHI usage 
def generate_input_data(exp_path,sim_path):
    f_x=open('generated_input_data\\target.dat','w')
    f_y=open('generated_input_data\\label.dat','w')
    f_i=open('generated_input_data\\index.dat','w')
    
    cas_list_raw = listdir(exp_path) # experimental IR path
    for i in range(len(cas_list_raw)):
        cas_list_raw[i] = cas_list_raw[i].split('_')[0].strip('.jdx')
    
    cas_list=[]
    mm_list = listdir(sim_path)
    for cas in cas_list_raw:
        if cas+'.dx' in mm_list:
            #print(cas_list[i]+' exists')
            cas_list.append(cas)
            pass
        else:
            #cas_list.remove(cas)
            print(cas+' does not exists!')
    
    
    
    for i in range(len(cas_list)):
        spectrum_DB = Spectrum(exp_path+cas_list[i]+'.jdx')
        spectrum_DFT = Spectrum(sim_path+cas_list[i]+'.dx')
        try:
            if(len(spectrum_DB.spectrum_signal) != len(spectrum_DFT.spectrum_signal)):
                print("length inequal")
                print(len(spectrum_DB.spectrum_signal))
                print(len(spectrum_DFT.spectrum_signal))
                raise NameError()
            else:
                # header
                if i < 1:
                    f_i.write('cas_list'+'\n')
                    for j in range(len(spectrum_DB.spectrum_wave_number)):
                        if j >0:
                            f_x.write(',')
                            f_y.write(',')
                        f_x.write(str(spectrum_DFT.spectrum_wave_number[j]))
                        f_y.write(str(spectrum_DB.spectrum_wave_number[j]))
                    f_x.write('\n')
                    f_y.write('\n')
                # content
                for j in range(len(spectrum_DB.spectrum_signal)):
                    if j >0:
                        f_x.write(',')
                        f_y.write(',')
                    f_x.write(str(spectrum_DFT.spectrum_signal[j]))
                    f_y.write(str( float(spectrum_DB.spectrum_signal[j]) +(1-float(spectrum_DB.base_line)) ) )
                f_x.write('\n')
                f_y.write('\n')
                f_i.write(cas_list[i]+'\n')
        except:
            print(cas_list[i]+"writing failed")
    f_x.flush()
    f_x.close()
    f_y.flush()
    f_y.close()
    f_i.flush()
    f_i.close()



    # fw_index = open(output_path_for_index,'w')
    # fw_data = open(output_path_for_data,'w')
    # #
    # for i in range(len(ir_list)):
    #     if ir_list[i].has_selected == "GAS":
    #         spectrum = Spectrum('IRDB\\COB_GAS\\'+ir_list[i].nist_cas+'.jdx')
    #         write_generate_input_data(fw_index,fw_data,spectrum,ir_list[i].nist_cas,ir_list[i].nist_name)
    #     elif ir_list[i].has_selected == "LIQUID":
    #         spectrum = Spectrum('IRDB\\COB_LIQUID\\'+ir_list[i].nist_cas+'.jdx')
    #         write_generate_input_data(fw_index,fw_data,spectrum,ir_list[i].nist_cas,ir_list[i].nist_name)
    #     elif ir_list[i].has_selected == "SOLUTION":    
    #         spectrum = Spectrum('IRDB\\COB_SOLUTION\\'+ir_list[i].nist_cas+'.jdx')
    #         write_generate_input_data(fw_index,fw_data,spectrum,ir_list[i].nist_cas,ir_list[i].nist_name)
    #     else:
    #         pass
    
    # fw_index.close()
    # fw_data.close()
    # only accept case: spectrum_resolution = 1 
def write_generate_input_data(fw_index,fw_data,spectrum,cas_num,cas_name):
    tot_num = (spectrum.max_wave_number-spectrum.min_wave_number) +1
    input_spectrum = [0 for o in range(tot_num)]
    input_spectrum_text = ''
    for i in range(len(spectrum.spectrum_signal)):
        input_spectrum[i] = spectrum.spectrum_signal[i]
    
    for i in range(len(input_spectrum)):
        input_spectrum_text += str(input_spectrum[i])
        if i != len(input_spectrum)-1:
            input_spectrum_text += ','

    fw_data.write(input_spectrum_text+'\n')
    fw_index.write(cas_num+','+cas_name+'\n')



# export all data point that contains IR spectrum
def export_full_table(ir_list,output_path_for_table):
    fw = open(output_path_for_table,'w')   
    line = ''
    for ir in ir_list:
        if ir.nist_has_cob_GAS == 'True':
            line = ir.nist_name+',GAS,'+ir.nist_cas + ',\n'
            fw.write(line)
        if ir.nist_has_cob_LIQUID == 'True':
            line = ir.nist_name+',LIQUID,'+ir.nist_cas + ',\n'
            fw.write(line)
        if ir.nist_has_cob_SOLUTION == 'True':
            line = ir.nist_name+',SOLUTION,'+ir.nist_cas + ',\n'
            fw.write(line)
    fw.flush()
    fw.close()
#Spectrum('IRDB\\COB_GAS\\74-86-2.jdx')