# opencv-face-app-
### 项目介绍
	这是一个基于树莓派用opencv和face++做人脸对比的，可以运行在app上的（局域网）视频监控
	用mjpg打开摄像头并用http流显示出来，opencv用来做人脸识别，face++用来做人脸对比
	app获取mjpg的视频流，显示出来。
### 各文件介绍
*	MyApplication
		整个app工程
*	bidui.py
		这是face++做比对的文件，用来比对要识别的人和存储在库里的人是否一致，识别度很高
*	feng.py
		这是树莓派上的蜂鸣器和灯用的，用gpio编程
*	haarcascade_eye_tree_eyeglasses.xml && lbpcascade_frontalface.xml
		这两个是opencv用来做识别的训练xml
*	main.py
		主python文件，里面有实现opencv的函数和主函数
*	push.py
		这是face++的，用来上传要保存的库任务，
*	send.py
		这是tcp编程，和app最交互用的
