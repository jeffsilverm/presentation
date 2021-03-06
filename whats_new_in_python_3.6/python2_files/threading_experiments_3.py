#!/usr/bin/env python
# simple code which uses threads

import time
from threading import Thread
import sys

print(("Running Python Version ", sys.version_info))

class MyThread(Thread):

    def __init__(self,bignum):

        Thread.__init__(self)
        self.bignum=bignum
    
    def run(self):
        print("MyThread.run was called")
        for l in range(10):
            for k in range(self.bignum):
                res=0
                for i in range(self.bignum):
                    res+=1
        print("MyThread.run has completed")


def test():
    bignum=1000
    thr1=MyThread(bignum)
    thr1.start()
    print("In test(), waiting to join thr1")
    thr1.join()
    
if __name__=="__main__":
    test()
