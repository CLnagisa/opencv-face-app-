# -*- coding: UTF-8 -*-
#发送消息
import socket 
import time  
def send(image_path):    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        sock.connect(('192.168.191.2', 12462))    
          
        flag = '1'  
#while True:   
        #        time.sleep(3)    
        import base64
        f = open(image_path,'rb')
        ls_f = base64.b64encode(f.read())
        f.close()
        print 'send to server with value: send succeed'
        sock.send(ls_f)    
        #        print sock.recv(1024)   
        #        flag = (flag=='1') and '2' or '1' #change to another type of value each time              
        sock.close() 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.settimeout(1)
s.bind(('0.0.0.0', 12462))
s.listen(1)
def rece():        #接收数据
	# 创建一个socket:
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       # try:
        #        s.setblocking(0)
         #       s.settimeout(1)

        # 建立连接:
          #      s.bind(('0.0.0.0', 12462))          #不知道为什么用000总之可以用就是了
           #     s.listen(1)
	try:
                sock, addr = s.accept()                            #接收一个新连接[A
        except socket.timeout:                          #捕获超时
                return 0
	data = sock.recv(1024)                         #接受其数据
	time.sleep(1)                                  #延迟
	#sock.send(data.decode('utf-8').upper().encode())  #发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
	sock.close()                                       #关闭连接
	return 1

