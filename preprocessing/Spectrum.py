from cmath import log
from math import exp
import math 
import peakutils
import numpy as np

# turn a list with digit within 0-1to become 1-list
def reverse_list(input_list):
    for i in range(len(input_list)):
        input_list[i] = 1 - input_list[i]
    return input_list

#### 
class Spectrum:
    def __init__(self,path,base_line=1):
        self.XUNITS = ''
        self.YUNITS = ''
        self.DELTAX = 0
        self.LASTX = ''
        self.FIRSTX = ''
        self.XFACTOR = ''
        self.YFACTOR = ''
        self.ORIGIN = ''
        self.base_line = base_line
        self.min_wave_number = 600 # 600
        self.max_wave_number = 3798 # 3750 # 3750
        self.base_line_array = None
        self.spectrum_resolution = 2 # one sample per wave number
        self.message = True

        self.spectrum_wave_number = list()
        self.spectrum_signal = list()
        self.path = path
        self.reader()

    # fcn to turn row data list into acceptable format
    def write_spectrum(self,row_x,row_y):
        # 
        ptr = self.min_wave_number
        row_ptr = 0
        #prev_x_row = 0
        if self.XUNITS == 'MICROMETERS':
            self.LASTX = 1000.0 / (self.LASTX/10.0)
            self.FIRSTX = 1000.0 / (self.FIRSTX/10.0)
            for i in range(len(row_x)):
                row_x[i] = 1000.0 / (row_x[i]/10.0)
        #
        if (float(self.XFACTOR) - 1).real**2 > 0.00001 :#if XFACTOR or YFACTOR is not 1
            for i in range(len(row_x)):
                row_x[i] = float(self.XFACTOR) * row_x[i]
        if (float(self.YFACTOR) - 1).real**2 > 0.00001 :
            for i in range(len(row_y)):
                row_y[i] =  row_y[i] * float(self.YFACTOR)
        #
        if float(self.LASTX) < float(self.FIRSTX):#sometimes row data is decreasing
            row_x.reverse()
            row_y.reverse()
        try:
            if self.XUNITS == '1/CM' or self.XUNITS == 'MICROMETERS':
                if self.YUNITS == 'TRANSMITTANCE':
                    pass
                elif self.YUNITS == 'ABSORBANCE':
                    for i in range(len(row_y)):
                        #row_y[i] = -log(row_y[i])
                        if row_y[i] < -1:
                            raise NameError()
                        row_y[i] = exp(log(10).real*-row_y[i]).real
                else:
                    return 'Unsupported Format'

                #### original
                while row_ptr < len(row_x):
                    if row_x[row_ptr] < ptr:
                        #prev_x = row_x[row_ptr]
                        row_ptr+=1
                    else:
                        if ptr > self.max_wave_number:
                            break
                        else:
                            self.spectrum_wave_number.append(ptr)
                            signal = row_y[row_ptr-1] + (row_y[row_ptr]-row_y[row_ptr-1])* ((ptr-row_x[row_ptr-1])/(row_x[row_ptr]-row_x[row_ptr-1]))
                            self.spectrum_signal.append(signal)#(float(self.base_line)-1))
                            ptr += self.spectrum_resolution
                            
                while ptr <= self.max_wave_number:
                    self.spectrum_wave_number.append(ptr)
                    #add according to last singal value
                    self.spectrum_signal.append(self.spectrum_signal[len(self.spectrum_signal)-1]) #transmittance = 1 means no absorption
                    
                    #self.spectrum_signal.append(1)
                    ptr += self.spectrum_resolution
                    
                # base line remove
                reverse_list(self.spectrum_signal)
                self.base_line_array = peakutils.baseline(y=np.array(self.spectrum_signal),deg=1)
                for i in range(len(self.spectrum_signal)):
                    self.spectrum_signal[i] = self.spectrum_signal[i] -self.base_line_array[i]
                reverse_list(self.spectrum_signal)
                
                # rescale Y axis to [0,1]
                if min(self.spectrum_signal)>0:
                    rescale_factor = 1/(-(min(self.spectrum_signal) -1))
                else:
                    rescale_factor = 1
                # rescale it!
                for i in range(len(self.spectrum_signal)):
                    self.spectrum_signal[i] = (self.spectrum_signal[i]-1)*rescale_factor + 1
                
                
                #for i in range(len(self.spectrum_wave_number)):
                #    print(str(self.spectrum_wave_number[i])+' : '+str(self.spectrum_signal[i]))
            else:
                return 'Unsupported Format'
        except NameError:
            print(self.path+' has negative value')
            f_err = open('abnormal_mm_log.txt','a')
            f_err.write(self.path+'\n')
            f_err.close()
        except:
            print('error'+self.path)
        return 'Spectrum Generated Successful'

    def reader(self):
        fr = open(self.path,'r')
        new_line = fr.readline()
        #reading 
        isInSpectrumZone = False
        row_spectrum_x = list()
        row_spectrum_y = list()

        while new_line != '':
            # Read Parameters
            if '#ORIGIN=' in new_line:
                self.ORIGIN = new_line.strip('\n').split('=')[1]
            if '##XUNITS=' in new_line:
                self.XUNITS = new_line.strip('\n').split('=')[1]
            if '##YUNITS=' in new_line:
                self.YUNITS = new_line.strip('\n').split('=')[1]
            if '##DELTAX=' in new_line:
                self.DELTAX = float(new_line.strip('\n').split('=')[1])
            if '##LASTX=' in new_line:
                self.LASTX = float(new_line.strip('\n').split('=')[1])
            if '##FIRSTX=' in new_line:
                self.FIRSTX = float(new_line.strip('\n').split('=')[1])
            if '##XFACTOR=' in new_line:
                self.XFACTOR = float(new_line.strip('\n').split('=')[1])
            if '##YFACTOR=' in new_line:
                self.YFACTOR = float(new_line.strip('\n').split('=')[1])
            # Read Spectrum
            if '##END=' in new_line :
                isInSpectrumZone = False

            if isInSpectrumZone:    
                element = new_line.strip('\n').split(' ')
                for i in range(1,len(element)):
                    row_spectrum_x.append( float(element[0]) + (i-1) * self.DELTAX )
                    row_spectrum_y.append( float(element[i]) )

            if '##XYDATA=' in new_line:
                if '##XYDATA=(X++(Y..Y))' in new_line:
                    isInSpectrumZone = True
                else:
                    print('unsupported XYDATA format')
            
            new_line = fr.readline()

        self.message = self.write_spectrum(row_spectrum_x,row_spectrum_y)
        # for i in range(len(row_spectrum_x)):
        #     print(str(row_spectrum_x[i])+' : '+str(row_spectrum_y[i]))
