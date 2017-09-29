#!/usr/bin/env python

import time
import _thread

def myfunction(string,sleeptime,lock,*args):
    while 1:
	#entering critical section
        lock.acquire() 
        print(string,"After acquiting the lock, Sleeping for ",sleeptime)
        time.sleep(sleeptime) 
        print(string," Now releasing lock and then sleeping again")
        lock.release()
	#exiting critical section
        time.sleep(sleeptime) # why?

if __name__=="__main__":

    lock=_thread.allocate_lock()
    _thread.start_new_thread(myfunction,("Thread No:1 ",2,lock))
    _thread.start_new_thread(myfunction,("Thread No: 2",0.7,lock))

    while 1:pass
