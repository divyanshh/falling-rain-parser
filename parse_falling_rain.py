#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 12:45:04 2018

@author: divyanshjain
"""

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from threading import Thread, Lock
from queue import Queue
import time

url = "http://www.fallingrain.com/world/IN/"
num_threads = 50

def saveData(data_rows, o_file, o_file_mutex):
    o_file_mutex.acquire()
    for i in range(len(data_rows)):
        row = []
        # go through each data element in each table row
        for td in data_rows[i].findAll('td'): # td tag contains data for each row
            row.append(td.getText())

        if len(row) != 8:
            continue # invalid data

        data = str(row[0]) + "," + str(row[2]) + "," + str(row[4]) + "," + str(row[5]) + "," + str(row[6]) + "," + str(row[7]) + "\n"
        #print(data)
        try:
            o_file.write(data)
        except:
            print("fatal! could not write data to file: " + data)

    o_file_mutex.release()


def crawl(tasks_q, o_file, o_file_mutex):
    global total_tasks_complete
    while True:        
        urlc = tasks_q.get()
        if urlc is None:
            return;
        try:
            req = Request(urlc)
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")
            data_rows = soup.findAll('tr')   # tr tag contains all the rows of a table

            links = []
            for link in soup.findAll('a'):
                links.append(link.get('href'))
            
            if len(data_rows) > 0:  # page contains a table
                saveData(data_rows, o_file, o_file_mutex)
            
            if len(links) > len(data_rows):  # page contains links not in the table therefore can be further parsed
                generateURLs(tasks_q, urlc)
        except Exception as e:
            #print("Does not exist : " + str(e))
            pass
        finally:
            tasks_q.task_done()
            total_tasks_complete += 1


def generateURLs(tasks_q, urlg):
    for i in range(97, 123): # ASCII codes
        urlgn = urlg + chr(i) + "/"
        urlgn = urlgn[:41] + urlgn[41].upper() + urlgn[42:] # make the 41 index char uppercase
        tasks_q.put(urlgn)


def monitorTasks(tasks_q):
    global total_tasks_complete
    total_tasks_complete_prev = total_tasks_complete
    while total_tasks_complete >= 0:
        time.sleep(60)
        print("Tasks size: " + str(tasks_q.qsize()) +  ", Speed: " + str(total_tasks_complete - total_tasks_complete_prev) + " / min")
        total_tasks_complete_prev = total_tasks_complete


tasks = Queue(maxsize = 0)
total_tasks_complete = 0
o_file = None
o_file_mutex = Lock()

try:
    o_file = open('fallingrain.csv', 'w')
except:
    print("fatal! could not open file")
    quit()

for i in range(0 , 40): # generating basic urls
    if i < 10:
        urln = url + "0" + str(i)
    else:
        urln = url + str(i)
    urln = urln + "/a/"
    tasks.put(urln)

for i in range(num_threads):
    worker = Thread(target = crawl, args = (tasks, o_file, o_file_mutex,))
    worker.setDaemon(True)
    worker.start()

monitor = Thread(target = monitorTasks, args = (tasks,))
monitor.setDaemon(True)
monitor.start()

tasks.join()
o_file.close()

total_tasks_complete = -1
for i in range(num_threads):
    tasks.put(None)  # signal all worker threads to quit