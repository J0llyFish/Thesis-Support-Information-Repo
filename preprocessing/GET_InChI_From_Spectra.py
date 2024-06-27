from time import time
import requests
#import pandas as pd
from bs4 import BeautifulSoup
import threading
import queue

# for store found data
# valid_cas_list = []
# valid_ir_list = []
# current_head = -1
# cas_1_per_loop = 3

# cas_list_file_path = 'cas_list.txt'
# valid_smiles_file_path = 'SMILES_List.txt'

# spectra path
spectra_files_path = 'GAS_classified_by_origin//'
# Inchi file path
inchi_path = 'inchi_list.txt'

from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(spectra_files_path) if isfile(join(spectra_files_path, f))]

inchi_list = []

# def find_smiles(cas='') :
#     re = 
#     #print if the response is good or bad ,200 means it's good
#     #print(re)
#     if
#     return re



def get_cas_list():
    global data_queue , inchi_path , onlyfiles , inchi_list
    # get cas with InChI
    fr = open(inchi_path,'r')
    inchi_list = fr.readlines()
    inchi_check_list = [element.split(':')[0] for element in inchi_list]
    fr.close()
    for i in range(len(onlyfiles)):
        if onlyfiles[i].strip('.jdx') not in inchi_check_list:
            data_queue.put( onlyfiles[i].strip('.jdx') )
        
        #data_queue.put( onlyfiles[i].strip('.jdx') )
    # # find valid smiles cas
    # smiles_list_prev = []
    # fr = open(valid_smiles_file_path,'r')
    # new_line = fr.readline()
    # while new_line != "":
    #     smiles_list_prev.append(new_line.split(';')[0])
    #     new_line = fr.readline()
    # fr.close()
    
    # # find cas not with smiles
    # fr = open(cas_list_file_path,'r')
    # new_line = fr.readline()
    # while new_line != "":
    #     new_data = new_line.split(':')[0].strip(' ')
    #     if new_data not in smiles_list_prev:
    #         data_queue.put( new_data )
    #     else:
    #         pass
    #     new_line = fr.readline()
    # fr.close()
    # print('done encoding cas')
    # print(data_queue.get())
    # print(data_queue.get())
# def write_cas():

    
thread_list = []
# define the number of threads, it can be different from number of tasks
MultiThreadNumber = 100
# define a class to inherit Thread class
class Worker(threading.Thread):
    def __init__(self, queue,lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock=lock
    def run(self):
        global valid_smiles_list
        while self.queue.qsize() > 0:
            data = self.queue.get()
            try:
                re = requests.get('https://webbook.nist.gov/cgi/cbook.cgi?Name='+str(data)+'&Units=SI')
                
                soup = BeautifulSoup(re.text, 'html.parser')
                check_tag = soup.find('span',{"clss":"inchi-text"})
                
                #re = requests.get('https://cactus.nci.nih.gov/chemical/structure/'+str(data)+'/smiles')
                # soup = BeautifulSoup(re.text, 'html.parser')
                # check_tag = soup.find(id='Top')
                if check_tag != None and 'InChI' in check_tag.contents[0]: #'Page not found' not in re.text :#'InChI' in check_tag.contents[0]:#
                    new_data = data+':'+check_tag.contents[0]
                    
                else:
                    print(data+' DOES NOT EXISTS IN NIST CHEM SITE')
                    re = requests.get('https://cactus.nci.nih.gov/chemical/structure/'+str(data)+'/stdinchi')
                    if 'Page not found' in re.text:
                        raise ValueError 
                    new_data = data+':'+re.text
                
                self.lock.acquire()
                #valid_smiles_list.append(new_data)
                #write found cas to file
                fs = open(inchi_path,'a')
                fs.write(new_data+'\n')
                fs.flush()
                fs.close()
                print(new_data)
                self.lock.release()
                self.queue.task_done()
            except:
                print(data+':data unexpected failed')
                try:
                    self.lock.release()
                except:
                    pass
                self.queue.task_done()
            
#cas_1_list = get_list()
data_queue = queue.Queue()
diction_lock = threading.Lock()
valid_smiles_list=list()

get_cas_list()
#while True:
for i in range(MultiThreadNumber):
    t = Worker(queue=data_queue,lock=diction_lock)
    thread_list.append(t)
    # make this thread start to work 
    t.start()
# lock process unitl all element in the queue were processed
data_queue.join()

# join every thread to wait until every thread's work is done
for t in thread_list:
    t.join()

#write found cas to file

# fw = open(valid_smiles_file_path,'a')
# for item in valid_smiles_list:
#     try:
#         fw.write(item)
#     except:
#         pass
# fw.flush()
# fw.close()
print("done!")