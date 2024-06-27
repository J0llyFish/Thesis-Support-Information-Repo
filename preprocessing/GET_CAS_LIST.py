from time import time
import requests
#import pandas as pd
from bs4 import BeautifulSoup
import threading
import queue

# for store found data
valid_cas_list = []
valid_ir_list = []
current_head = -1
cas_1_per_loop = 3

def find_chemical(cas='') :
    re = requests.get('https://webbook.nist.gov/cgi/cbook.cgi?Name='+str(cas)+'&Units=SI')
    #print if the response is good or bad ,200 means it's good
    #print(re)
    return re
def find_ir():
    pass
def generate_cas_list(data_queue=None,cas_1_number=108):
    for i in range(100):
        cas_1 = str(cas_1_number)
        cas_2 = str(i)
        if int(cas_2) < 10:
            cas_2 = '0'+str(i)
        #checksum
        checksum = 1*(int(cas_2[1]))+2*(int(cas_2[0]))
        for i in range(len(cas_1)):
            index = len(cas_1)-1-i
            checksum+=int(cas_1[index])*(i+3)
        checksum = str(checksum%10)
        
        if data_queue is not None:
            data_queue.put(cas_1+'-'+cas_2+'-'+checksum)
        #print(cas_1+'-'+cas_2+'-'+checksum)

# start head
start_head = 10 

def get_list():
    global current_head , cas_1_per_loop
    fr = open('cas_list.txt','r')
    new_line = fr.readline()
    last_cas = new_line
    while new_line != "":
        last_cas = new_line
        new_line = fr.readline()
    fr.close()
    # check if file is empty
    if last_cas != "":
        new_head = int(last_cas.split('-')[0])+1
        if new_head < start_head:
            new_head = start_head
    else:
        new_head = start_head
    if current_head != -1:
        current_head += cas_1_per_loop
    else:
        current_head = new_head
    return [i for i in range(current_head,current_head+cas_1_per_loop)]

def write_cas():
    global valid_cas_list
    global valid_ir_list
    
    fw = open('cas_list.txt','a')
    for item in valid_cas_list:
        try:
            fw.write(item)
        except:
            pass
    fw.flush()
    fw.close()
    
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
        global valid_cas_list
        while self.queue.qsize() > 0:
            data = self.queue.get()
            try:
                re = find_chemical(data)
                soup = BeautifulSoup(re.text, 'html.parser')
                check_tag = soup.find(id='Top')
                if check_tag and check_tag.get_text() is not 'Name Not Found':
                    new_cas = data+' : '+check_tag.get_text() + '\n'
                    self.lock.acquire()
                    valid_cas_list.append(new_cas)
                    print(new_cas)
                    self.lock.release()
                #self.lock.acquire()
                #self.lock.release()
                self.queue.task_done()
            except:
                print(data+':data extraction failed')
                self.lock.release()
                self.queue.task_done()
            
#cas_1_list = get_list()
data_queue = queue.Queue()
diction_lock = threading.Lock()

while True:
    cas_1_list = get_list()
    for chem in cas_1_list:
        generate_cas_list(data_queue,chem)
        #data_queue.put(chem)
        
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
    write_cas()
    
    print(' a loop just done ',end='')
    print(current_head)
    valid_ir_list = []
    valid_cas_list = []