# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 13:06:23 2018

@author: fahad

@contributor: Lianxin Zhang
"""

import os
import time
import tcpserver
import globalvar as gl
import threading
import looping
# import RPi.GPIO as GPIO
import IMU
import sensor
# import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    gl.set_value('flag',False) # Stop sign
    gl.set_value('heading',0) # initial heading angle zero
    gl.set_value('PWM1',0) # PWM for Motor1
    gl.set_value('PWM2',0) # PWM for Motor2
    
    conn = tcpserver.tcpserver()
    
    t1 = threading.Thread(target= looping.looping,args= (conn,)) # Receiving Commands
    t2 = threading.Thread(target= IMU.IMU)
    t3 = threading.Thread(target= sensor.sensor)
    
#    t1.setDaemon(True)
    t1.start() # start thread 1
    time.sleep(1)
    t2.start() # start thread 2
    t3.start() # start thread 3    
    
    t1.join() # wait for the t1 thread to complete
#    t2.join() # wait for the t2 thread to complete
#    t3.join() # wait for the t3 thread to complete

#    conn.close()
    time.sleep(1)
    print('Connection closed!')
    
    
#-----------------------------------------------------------
