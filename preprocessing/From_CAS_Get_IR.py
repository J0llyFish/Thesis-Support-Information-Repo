import queue
import threading
import time
import requests
import math
from IR_reader_General import *
from os import listdir

# plain text file of the list of cas numbers
file_name = 'cas_list.txt'
# downloaded spectra will be saved in the folder
save_path = "GAS\\"

files = listdir(save_path)
for i in range(len(files)):
    files[i] = files[i].split('_')[0]
print("has "+str(len(files))+" files exist in GAS folder")

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
            data.append( new_line.split(':')[0].strip(' ') )
            new_line = fr.readline()
    except:
        print('exception occur when reading')
        fr.close()
    fr.close()
    return data

## search IR spectrums for each chemicals
thread_list = []
available_index = []
# define the number of threads, it can be different from number of tasks
MultiThreadNumber = 32
# define a class to inherit Thread class
class Worker(threading.Thread):
    def __init__(self, queue,lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock=lock
    def run(self):
        global valid_cas_list
        while self.queue.qsize() > 0:
            data = self.queue.get()
            try:
                index_num = 0
                re = requests.get('https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C'+data+'&amp;Index='+str(index_num)+'&amp;Type=IR')
                while 'TITLE=Spectrum not found' not in re.text and index_num < 8:
                    re = requests.get('https://webbook.nist.gov/cgi/cbook.cgi?JCAMP=C'+data+'&amp;Index='+str(index_num)+'&amp;Type=IR')
                    if ("#STATE=gas" in re.text or "#STATE=Gas" in re.text or "#STATE=GAS" in re.text) and True:
                        # if "#ORIGIN=Sadtler Research Labs Under US-EPA Contract" in re.text:
                        #     fw = open(save_path+data+'.jdx','w')
                        #     fw.write(re.text)
                        #     fw.flush()
                        #     fw.close()
                        #     available_index.append(data)
                        #     print(data+' has IR spectrum')
                        #     break
                        # if "#ORIGIN=DOW CHEMICAL COMPANY" in re.text:
                        #     fw = open(save_path+data+'.jdx','w')
                        #     fw.write(re.text)
                        #     fw.flush()
                        #     fw.close()
                        #     available_index.append(data)
                        #     print(data+' has IR spectrum')
                        #     break
                        # if "#ORIGIN=NIST Mass Spectrometry Data Center" not in re.text:
                        #     fw = open(save_path+data+'.jdx','w')
                        #     fw.write(re.text)
                        #     fw.flush()
                        #     fw.close()
                        #     available_index.append(data)
                        #     print(data+' has IR spectrum')
                        #     break
                        fw = open(save_path+data+'_'+str(index_num)+'.jdx','w')
                        fw.write(re.text)
                        fw.flush()
                        fw.close()
                        available_index.append(data+'_'+str(index_num))
                        print(data+'_'+str(index_num)+' has IR spectrum')
                        #break

                    index_num += 1
                
            except:
                print(data+':data extraction failed')
                self.lock.release()
                self.queue.task_done()

data_queue = queue.Queue()
diction_lock = threading.Lock()
    

# read file with format of  xxx-xx-x : chemcial name
cas_list = read_file_csv(file_name)

for chem in cas_list:
    if chem not in files:
        data_queue.put(chem)
    #data_queue.put(chem)
print("has "+str(data_queue.qsize())+" unfined CAS in the list")

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
        
# export available cas list
fw = open('available cas list.txt','w')
fw.writelines(available_index)
fw.flush()
fw.close()