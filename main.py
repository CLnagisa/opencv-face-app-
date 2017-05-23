# -*- coding: utf-8 -*-


import time
import cv2
import os
import urllib
from PIL import Image,ImageDraw
import bidui                    #比对文件
from feng import begin         #蜂鸣器文件
import send                     #发送文件
import os
import sys
import shutil                   #删除文件夹用



#检测人脸
def detectFaces(image_name):
	img = cv2.imread(image_name)
	face_cascade = cv2.CascadeClassifier(r'./lbpcascade_frontalface.xml')
	if img.ndim == 3:
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	else:
		gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

	faces = face_cascade.detectMultiScale(gray, 1.2, 5)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
	result = []
	for (x,y,width,height) in faces:
		result.append((x,y,x+width,y+height))
	return result
	
#保存人脸图
def saveFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        #将人脸保存在save_dir目录下。
        #Image模块：Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
        save_dir = image_name.split('.')[0]+"_faces"
        count = 0
        for (x1,y1,x2,y2) in faces:
            file_name = os.path.join('./pic/', 'savepic' + str(count)+".jpg")
            Image.open(image_name).crop((x1,y1,x2,y2)).save(file_name)
            count+=1

#框出人脸出来
def drawFaces(image_name):
	faces = detectFaces(image_name)
	if faces:
		img = cv2.imread(image_name)
		for (x1,y1,x2,y2) in faces:
			cv2.rectangle( img, ( x1, y1 ), ( x2, y2 ), ( 100, 255, 100 ), 2 )
			cv2.putText( img, "Face No." + str( len( faces ) ), ( x1, y1 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
		cv2.imwrite('./pic/drawfaces_'+image_name, img)

		
#检测眼睛，返回坐标
def detectEyes(image_name):
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    faces = detectFaces(image_name)

    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = []
    for (x1,y1,x2,y2) in faces:
        roi_gray = gray[y1:y2, x1:x2]
        eyes = eye_cascade.detectMultiScale(roi_gray,1.3,2)
        for (ex,ey,ew,eh) in eyes:
            result.append((x1+ex,y1+ey,x1+ex+ew,y1+ey+eh))
    return result
	
#在原图像上框出眼睛.
def drawEyes(image_name):
    eyes = detectEyes(image_name)
    if eyes:
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1,y1,x2,y2) in eyes:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(0, 0,255))
        img.save('./pic/draweyes_'+image_name)
	

if __name__ == '__main__':
        while 1:
                shutil.rmtree('./pic/')  
                os.mkdir('./pic') 
                urllib.urlretrieve('http://192.168.191.6:8080/?action=snapshot','aaaaa.jpg' )
                faces = detectFaces('aaaaa.jpg')
                print "Found " + str( len( faces ) ) + " face(s)"
                Mflag = 0
                if faces:
                        print 'face success'
                        eyes = detectEyes('aaaaa.jpg')
                        print  1
                        if eyes:
                                print 'eye success'
                                drawFaces('aaaaa.jpg')      #画出人脸
                                drawEyes('aaaaa.jpg')       #画出眼睛
                                saveFaces('aaaaa.jpg')      #保存人脸图，做对比
                                #查询已经保存了的截取出来的人的图片
                                path = './pic/'
                                word = 'savepic'
                                for filename in os.listdir(path):
                                        fp = os.path.join(path, filename)
                                        if os.path.isfile(fp) and word in filename:
                                                a = bidui.bidui('./pic/' + filename)
                                                print  4
                                                if a == 1:
                                                        Mflag = 0                                               
                                                        break
                                                else:
                                                        Mflag = 1
                                        elif os.path.isdir(fp):
                                                search(fp, word)
                                                
                                if Mflag == 1:                                                                   
                                        send.send('aaaaa.jpg')                               
                                        begin()
			else:
				print 'eye_error'
                else:
                                print 'error'
                time.sleep(4)                  

				
