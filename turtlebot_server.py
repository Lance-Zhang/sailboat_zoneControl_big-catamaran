# -*- coding: utf-8 -*-
"""
Created on Sat Jun 09 12:41:28 2018

@author: CUHKSZ
"""

from socket import *
import threading
import math
import re
import time

# TCP/IP
address='192.168.1.106'     #监听哪些网络  127.0.0.1是监听本机 0.0.0.0是监听整个网络
port=8080             #监听自己的哪个端口
buffsize=1024          #接收从客户端发来的数据的缓存区大小
s = socket(AF_INET, SOCK_STREAM)
s.bind((address,port))
print('Server is created!')
s.listen(3)     #最大连接数


def tcplink(clientsock,addr,i):
    x=[]
    y=[]
    xx=[]
    yy=[]
    
    r_err_k=0
    r_err_k_1=0

    #plt.figure()
    while True:
        recvdata=clientsock.recv(buffsize).decode('utf-8')
        print(recvdata+' from '+ str(addr))
        #print(t-t0)

        trans=list(eval(re.findall(r'[^\[\]]+', recvdata)[0])) # (x,y,z) coordinates
        rot=list(eval(re.findall(r'[^\[\]]+', recvdata)[1])) # Euler  Quaternion (w,x,y,z)
        a=trans[0]   # x,y coordinates
        b=trans[1]
        y=rot[2]     # sin theta/2
        z=rot[3]     # cos theta/2
        l_ref=[-b/math.sqrt(a*a+b*b),a/math.sqrt(a*a+b*b)] # target vector as reference
        l_tes=[(z*z-y*y),(2*y*z)] # current orientation vector as feedback
        
        err_test=l_ref[0]*l_tes[1]-l_ref[1]*l_tes[0] # cross multiplication
        print(-err_test)
        
        r_err_k_1=r_err_k
        r_err_k=-math.sqrt(a*a+b*b)+1 # 1 is the radius
        #print(r_err_k)
        
        v=0.2 # constant v
        if abs(err_test)>0.2:
            w=0.2-0.2*err_test
            print('w: ',w)
        else:
            w=0.2-0.5*r_err_k-0.05*(r_err_k-r_err_k_1)
            print('r: ',w)

       # print('rp: ' + str(rp) + 'w: ' + str(w))
        with open("1.txt", "a") as f:
            x=str(a)+' '+str(b)+'\n'
            xx.append(a)
            yy.append(b)
            f.write(x)
            #plt.plot(xx,yy)
            #plt.show()
        #else:
           #w=0.6
        #senddata=recvdata+'from sever'
        senddata=str((v,w))
        clientsock.send(senddata.encode())
    clientsock.close()

# main program
i = 0
while True:
    clientsock,clientaddress=s.accept()
    print('connect from:',clientaddress)
#传输数据都利用clientsock，和s无关
    t=threading.Thread(target=tcplink,args=(clientsock,clientaddress,i))  #t为新创建的线程
    t.start()
    i += 1
s.close()