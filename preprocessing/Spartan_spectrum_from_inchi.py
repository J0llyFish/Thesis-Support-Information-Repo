import pyautogui , time
from os import listdir

def save_abnormal_to_list(abn):
    fr=open('abnormal_list.txt','r')
    strs = fr.readlines()
    fr.close()
    for i in range(len(strs)):
        strs[i] = strs[i].strip('\n')
    if abn in strs:
        pass
    else:
        fw=open('abnormal_list.txt','a')
        fw.write(abn+'\n')
        fw.close()
# read smiles
ptr = 0
# smiles_cas = list()
# smiles = list()
inchi_dict = dict()
fr = open('inchi_list.txt','r')
new_line = fr.readline()
while new_line != "":
    inchi_dict[new_line.split(':')[0]] = new_line.split(':')[1].strip('\n')
    # smiles_cas=new_line.split(';')[0]
    # smiles=new_line.split(';')[1].strip('\n')
    new_line = fr.readline()
fr.close()
element_table_ascii=[ord('H'),ord('h'),ord('C'),ord('c'),ord('N'),ord('n'),ord('O'),ord('o')]
# set cas choose rules
cas_list=list()
for item in inchi_dict.items():
    
    element_list = list(item[1].split('=')[1])
    # print(item[0])
    is_simple_enough = True
    # only contain H C N O
    # for i in range(len(element_list)):
        # element_list[i]=ord(element_list[i])
        # if ( (element_list[i]>=65 and element_list[i]<=90) or (element_list[i]>=97 and element_list[i]<=122) ) and not (element_list[i] in element_table_ascii):
        #     print(item[1],end='')
        #     print(' is not simple enough')
        #     is_simple_enough = False
        #     break
    if is_simple_enough:
        print(item[1],end='')
        print(' is good')
        cas_list.append(item[0])

    #print(item[0])

# read ir that has been done
mm_list_raw = listdir("SP_MM_inchi\\")
mm_list = list()
for i in range(len(mm_list_raw)):
    if '.dx' in mm_list_raw[i]:
        mm_list.append(mm_list_raw[i].strip('.dx'))
        print(mm_list_raw[i])
# delete ir that has been done
for i in range(len(mm_list)):
    if mm_list[i] in cas_list:
        print(mm_list[i]+' has been done!')
        cas_list.remove(mm_list[i])

# read abnormal list
fr=open('abnormal_list.txt','r')
abn_list = fr.readlines()
for i in range(len(abn_list)):
    abn_list[i] = abn_list[i].strip('\n')
fr.close()
# remove abnormals
for i in range(len(abn_list)):
    if abn_list[i] in cas_list:
        print(abn_list[i]+' has been remove for abnormal!')
        cas_list.remove(abn_list[i])


# # # validate
# # print('-------------')
# # for i in range(len(cas_list)):
# #     print(cas_list[i],end='')
# #     print(smiles.get(cas_list[i]))

# print(cas_list)
#print(len(cas_list))
#print(len(smiles))

# for control
pos_file_bar = [30,40] ###
pos_new_build = [30,65]
pos_close = [30,168]
pos_save = [30,190]
# save gui
pos_save_gui = [12,60] ##
pos_save_save_btn = [pos_save_gui[0]+785,pos_save_gui[1]+500] # save button in save gui
pos_refresh_file_yes = [1009,528]
pos_save_as_types = [pos_save_gui[0]+250,pos_save_gui[1]+460]
pos_save_as_jcamp =[pos_save_gui[0]+250,pos_save_gui[1]+811]


pos_setup_bar = [pos_file_bar[0]+325,pos_file_bar[1]]
pos_calculation = [pos_setup_bar[0],pos_setup_bar[1]+25]
# config gui
pos_IR = [360,547] ##
pos_density_functional = [pos_IR[0]+90,pos_IR[1]-93]
pos_mm = [pos_density_functional[0],pos_IR[1]-149]
pos_se = [pos_density_functional[0],pos_IR[1]-136]
pos_summit = [pos_IR[0]+835,pos_IR[1]+118]
#
pos_calc_complete_OK = [931,552]


# smiles
pos_smiles_btn = [1464,692] # now inchi
pos_smile_input_gui = [498,447]##
pos_smiles_input_OK = [pos_smile_input_gui[0]+372,pos_smile_input_gui[1]+123]
pos_model_area_center = [pos_smile_input_gui[0]-30,pos_smile_input_gui[1]-30]
pos_minimize = [1460,918]

# for check
pos_smiles_check_white = [pos_smile_input_gui[0]+300,pos_smile_input_gui[1]+15]
pos_refresh_file_check_white = [884,469]
pos_calc_complete_check_white = [881,467]
pos_electron_charge_pair_white = [760,590]

action_interval_time = 0.2#0.08
# start auto procedure
for i in range(len(cas_list)):
#for i in range(3):
    try:
        # first open new model # first click can let pc focus on spartan
        pyautogui.click(x=pos_file_bar[0], y=pos_file_bar[1])
        time.sleep(action_interval_time)
        pyautogui.click(x=pos_new_build[0], y=pos_new_build[1],duration=0.2)
        time.sleep(action_interval_time)
        # input smile
        pyautogui.click(x=pos_smiles_btn[0], y=pos_smiles_btn[1])
        time.sleep(action_interval_time)
        pyautogui.typewrite( inchi_dict.get(cas_list[i]) , interval=0.02)
        time.sleep(action_interval_time)
        pyautogui.click(x=pos_smiles_input_OK[0], y=pos_smiles_input_OK[1])
        time.sleep(action_interval_time)
        time.sleep(action_interval_time)
        # check if this smiles is acceptable
        if pyautogui.pixel(pos_smiles_check_white[0],pos_smiles_check_white[1])[0] < 250:
            pass#goodpos_smiles_check_white
        else:
            print('smile not good')
            save_abnormal_to_list(cas_list[i])
            raise NameError('get pixel failed')
            #pass
        # build mol
        pyautogui.doubleClick(x=pos_model_area_center[0], y=pos_model_area_center[1],duration=0.03)
        time.sleep(action_interval_time)
        # save mol
        # pyautogui.click(x=pos_file_bar[0], y=pos_file_bar[1])
        # time.sleep(action_interval_time)
        # pyautogui.click(x=pos_save[0], y=pos_save[1])
        # time.sleep(action_interval_time)
        pyautogui.hotkey('ctrl', 's')
        pyautogui.typewrite( cas_list[i] , interval=0.02)
        time.sleep(action_interval_time)
        #pyautogui.click(x=pos_save_save_btn[0], y=pos_save_save_btn[1])
        pyautogui.hotkey('ctrl', 's')
        time.sleep(action_interval_time)
        pyautogui.hotkey('enter')
        time.sleep(action_interval_time)

        pyautogui.hotkey('y')
        time.sleep(action_interval_time)
        # if pyautogui.pixel( pos_refresh_file_check_white[0],pos_refresh_file_check_white[1])[0] > 250:
        #     #press refresh 
        #     pyautogui.hotkey('y')
        #     #pyautogui.click(x=pos_refresh_file_yes[0], y=pos_refresh_file_yes[1])
        #     time.sleep(action_interval_time)
        # else:
        #     pass
        # minimize by simple algorithm
        pyautogui.click(x=pos_minimize[0], y=pos_minimize[1])
        time.sleep(action_interval_time*30)
        # stop minimization
        pyautogui.click(x=pos_minimize[0], y=pos_minimize[1])
        time.sleep(action_interval_time)
        pyautogui.hotkey('enter')
        time.sleep(action_interval_time)

        # setup configuration
        pyautogui.click(x=pos_setup_bar[0], y=pos_setup_bar[1])
        time.sleep(action_interval_time)
        pyautogui.click(x=pos_calculation[0], y=pos_calculation[1])
        time.sleep(action_interval_time)
        pyautogui.hotkey('tab'  ,interval=action_interval_time/2)
        pyautogui.hotkey('tab'  ,interval=action_interval_time/2)
        pyautogui.hotkey('tab'  ,interval=action_interval_time/2)
        # methods
        pyautogui.hotkey('up'  ,interval=action_interval_time/2)
        pyautogui.hotkey('up'  ,interval=action_interval_time/2)
        pyautogui.hotkey('up'  ,interval=action_interval_time/2)
        #
        #### for semi empirical
        # pyautogui.hotkey('tab'  ,interval=action_interval_time/2)
        # pyautogui.hotkey('tab'  ,interval=action_interval_time/2)
        # pyautogui.hotkey('space'  ,interval=action_interval_time/2)
        # for j in range(7):
        #     pyautogui.hotkey('tab'  ,interval=action_interval_time/2)
        # pyautogui.hotkey('space'  ,interval=action_interval_time/2)
        # pyautogui.click(x=pos_density_functional[0], y=pos_density_functional[1])
        # time.sleep(action_interval_time)
        # # click prefered method
        # pyautogui.click(x=pos_mm[0], y=pos_mm[1])
        # time.sleep(action_interval_time)
        # pyautogui.click(x=pos_IR[0], y=pos_IR[1])
        # time.sleep(action_interval_time)
        # pyautogui.click(x=pos_summit[0], y=pos_summit[1])
        # time.sleep(action_interval_time*32)


        #pyautogui.hotkey('enter') # start
        #check if charge is balanced
        if pyautogui.pixel( pos_electron_charge_pair_white[0],pos_electron_charge_pair_white[1])[0] > 250:
            pyautogui.hotkey('esc')
            time.sleep(action_interval_time)
            pyautogui.hotkey('esc')
            print('charge not balanced')
            save_abnormal_to_list(cas_list[i])
            raise NameError('calc too long failed')
        else:
            #print('pos_electron_charge_pair_white failed'+str(pyautogui.pixel( pos_electron_charge_pair_white[0],pos_electron_charge_pair_white[1])[0]))
            #pyautogui.click(x=pos_calc_complete_OK[0], y=pos_calc_complete_OK[1])
            pyautogui.hotkey('enter')
        time.sleep(3)
        # calc
        count = 0
        while pyautogui.pixel( pos_refresh_file_check_white[0],pos_refresh_file_check_white[1])[0] < 250 and count<360:
            time.sleep(2)
            count+=1
        #
        if pyautogui.pixel( pos_refresh_file_check_white[0],pos_refresh_file_check_white[1])[0] >= 250:
            #pyautogui.click(x=pos_calc_complete_OK[0], y=pos_calc_complete_OK[1])
            
            pyautogui.click(x=pos_calc_complete_OK[0], y=pos_calc_complete_OK[1])
            time.sleep(action_interval_time*3)
            if pyautogui.pixel( pos_refresh_file_check_white[0],pos_refresh_file_check_white[1])[0] >= 250:
                # means abnormal happens
                pyautogui.click(x=pos_refresh_file_check_white[0], y=pos_refresh_file_check_white[1])
                pyautogui.hotkey('enter')
                print('abnormal exit')
                save_abnormal_to_list(cas_list[i])
                raise NameError('calc too long failed')
            else:
                pass
        else:
            print('calc too long')
            raise NameError('calc too long failed')
        
        # export IR to dx file
        # pyautogui.click(x=pos_file_bar[0], y=pos_file_bar[1])
        # time.sleep(action_interval_time)
        # pyautogui.click(x=pos_save[0], y=pos_save[1]+25)
        # time.sleep(action_interval_time)
        pyautogui.hotkey('ctrl','shift', 's')
        time.sleep(action_interval_time)
        # pyautogui.click(x=pos_save_as_types[0], y=pos_save_as_types[1])
        # time.sleep(action_interval_time)
        pyautogui.hotkey('tab')
        time.sleep(action_interval_time)
        pyautogui.hotkey('j')
        time.sleep(action_interval_time)
        pyautogui.hotkey('j')
        time.sleep(action_interval_time)
        pyautogui.hotkey('tab')
        time.sleep(action_interval_time)
        pyautogui.hotkey('tab')

        # pyautogui.click(x=pos_save_as_jcamp[0], y=pos_save_as_jcamp[1])
        # time.sleep(action_interval_time)
        #pyautogui.click(x=pos_save_save_btn[0], y=pos_save_save_btn[1])
        pyautogui.hotkey('enter')
        time.sleep(action_interval_time)
        pyautogui.hotkey('enter')
        time.sleep(action_interval_time)
        pyautogui.hotkey('enter')
        pyautogui.hotkey('ctrl', 's')
        time.sleep(action_interval_time)
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(action_interval_time*8) # rewrite IR
        pyautogui.hotkey('y')
        print(cas_list[i] + 'has done')
        time.sleep(action_interval_time)
    except NameError:
        #print(str(NameError.args),end='')
        print(cas_list[i])
        print(' MM failed')
        pyautogui.hotkey('esc')
        time.sleep(action_interval_time)
        pyautogui.hotkey('esc')
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(action_interval_time)
        pyautogui.hotkey('n')
    except KeyboardInterrupt:
        print('Interrupted')
        break
    except:
        print(cas_list[i],end='')
        print(' MM failed for unknow')
        pyautogui.hotkey('esc')
        time.sleep(action_interval_time)
        pyautogui.hotkey('esc')
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(action_interval_time*3)
        pyautogui.hotkey('n')
print('script done!')