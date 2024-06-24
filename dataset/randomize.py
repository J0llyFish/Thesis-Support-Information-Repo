from os import listdir
import random
# load data # currently load data by hand
# X_data = np.genfromtxt('target.dat', delimiter=',', skip_header = 1)
# Y_data = np.genfromtxt('label.dat', delimiter=',', skip_header = 1,)
# name_list = np.recfromcsv('index.dat')

IR_PATH_EXP = 'label.dat'
IR_PATH_SIM = 'target.dat'
IR_PATH_NAME = 'index.dat'

exp_ir_r = open(IR_PATH_EXP,'r')
sim_ir_r = open(IR_PATH_SIM,'r')
name_ir_r = open(IR_PATH_NAME,'r')

X_data = sim_ir_r.readlines()
Y_data = exp_ir_r.readlines()
name_list = name_ir_r.readlines()

name_list_header = name_list.pop(0)
Y_data_header = Y_data.pop(0)
X_data_header = X_data.pop(0)

randomlist = random.sample(range(0,len(name_list)), len(name_list))
print(len(randomlist))

X_data_new = []
Y_data_new = []
name_list_new = []
while len(name_list) > 0:
    random_index = random.randint(0,len(name_list)-1)
    X_data_new.append(X_data.pop(random_index))
    Y_data_new.append(Y_data.pop(random_index))
    name_list_new.append(name_list.pop(random_index))
    
# X_data = X_data[randomlist]
# Y_data = Y_data[randomlist]
# name_list = name_list[randomlist]

exp_ir_r.close()
sim_ir_r.close()
name_ir_r.close()


## w
exp_ir_r = open(IR_PATH_EXP,'w')
sim_ir_r = open(IR_PATH_SIM,'w')
name_ir_r = open(IR_PATH_NAME,'w')

exp_ir_r.write(Y_data_header)
sim_ir_r.write(X_data_header)
name_ir_r.write(name_list_header)

for i in range(len(name_list_new)):
    exp_ir_r.write(Y_data_new[i])
    sim_ir_r.write(X_data_new[i])
    name_ir_r.write(name_list_new[i])

print('done!')
exp_ir_r.flush()
sim_ir_r.flush()
name_ir_r.flush()
exp_ir_r.close()
sim_ir_r.close()
name_ir_r.close()

# cas_list = listdir("GAS\\")
# for i in range(len(cas_list)):
#     cas_list[i] = cas_list[i].strip('.jdx')
    
# mm_list = listdir("SP_MM_1\\")
# count = 0
# for i in range(len(cas_list)):
#     if cas_list[i]+'.dx' in mm_list:
#         #print(cas_list[i]+' exists')
#         pass
#     else:
#         print(cas_list[i]+' does not exists!')
#         count += 1

# print(count)
        

# def write_generate_input_data(fw_index,fw_data,spectrum,cas_num,cas_name):
#     tot_num = (spectrum.max_wave_number-spectrum.min_wave_number) +1
#     input_spectrum = [0 for o in range(tot_num)]
#     input_spectrum_text = ''
#     for i in range(len(spectrum.spectrum_signal)):
#         input_spectrum[i] = spectrum.spectrum_signal[i]
    
#     for i in range(len(input_spectrum)):
#         input_spectrum_text += str(input_spectrum[i])
#         if i != len(input_spectrum)-1:
#             input_spectrum_text += ','

#     fw_data.write(input_spectrum_text+'\n')
#     fw_index.write(cas_num+','+cas_name+'\n')