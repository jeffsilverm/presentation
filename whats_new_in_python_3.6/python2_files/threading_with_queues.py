#!/usr/bin/env python


import thread
import time
from threading import *
import Queue

class Producer(Thread):

    def __init__(self,itemq):
        Thread.__init__(self)
        self.itemq=itemq

    def run(self):
        
        itemq=self.itemq
        i=0
        while 1 :
            
            print currentThread(),"Produced One Item:",i
            itemq.put(i,1)
            i+=1
            time.sleep(1)


class Consumer(Thread):

    def __init__(self,itemq):
        Thread.__init__(self)
        self.itemq=itemq

    def run(self):
        itemq=self.itemq

	time.sleep(3)		# give the producer a chance to get ahead
        while 1:
            time.sleep(1)	# this should consume things faster than 
				# the producer can create them.
            it=itemq.get(1)
            print currentThread(),"  Consumed One Item:",it
            
        
        

        
if __name__=="__main__":

    q=Queue.Queue(10)

   
    pro=Producer(q)
    cons1=Consumer(q)
    cons2=Consumer(q)

    pro.start()
    cons1.start()
    cons2.start()
#    while 1: pass
