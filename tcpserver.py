# -*- coding: utf-8 -*-
"""
Created on Tue May 15 14:36:37 2018

@author: fahad

@contributor: Lianxin Zhang
"""

import socket
import sys
import time


#-----------TCP Connectivity-----------------
def tcpserver():
    
    # to build a TCP connection as a server
    # configuration
    TCP_IP = ''
    TCP_PORT = 50007
    BUFFER_SIZE = 1024
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server socket is created')
    try:
        s.bind((TCP_IP, TCP_PORT))
    except:
        print('Error: No binding could be done')
        sys.exit()

    s.listen(1)
    print('Socket is now listening')

    conn,addr = s.accept()
    print('Connection address:', addr)
    data = conn.recv(BUFFER_SIZE)         
    ReceivedData = str(data.decode('utf-8'))

    if ReceivedData == 'Hello':
        print('Communication is built! Received data: ', ReceivedData)

        MESSAGE = 'Data received! Communication is built.'.encode('utf-8')
        conn.sendall(MESSAGE) #echo
        time.sleep(1)
    else:
        MESSAGE = 'Wrong data! Reconnect please.'.encode('utf-8')
        conn.sendall(MESSAGE) 
        sys.exit()

    return conn
#--------------------------------------------------
#tcpserver()

