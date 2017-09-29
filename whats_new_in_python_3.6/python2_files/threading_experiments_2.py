#!/usr/bin/env python

import time
import thread

def myfunction(string,sleeptime,lock,*args):
    while 1:
        print string,"entering critical section, waiting to acquire lock"
        lock.acquire() 
        print string,"After acquiting the lock, Sleeping for ",sleeptime
        time.sleep(sleeptime) 
        print string," Now releasing lock and then sleeping again"
        lock.release()
	#exiting critical section
        time.sleep(sleeptime) # why?

if __name__=="__main__":

    lock=thread.allocate_lock()
    thread.start_new_thread(myfunction,("Thread No:1 ",2,lock))
    thread.start_new_thread(myfunction,("Thread No: 2",0.7,lock))
    thread.start_new_thread(myfunction,("Thread No: three",1.7,lock))
    while 1:pass
