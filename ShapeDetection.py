# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 23:28:57 2021

@author: Ahmet
"""


import cv2
import numpy as np



frame_W=640 #width  
frame_H=480 #height  

frame=cv2.VideoCapture(0)


frame.set(3,frame_W) 
frame.set(4,frame_H)



#Function to calculating canny parameters and applying canny
def canny_smart(img,sigma=0.33):  
	v = np.median(img)
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(img, lower, upper)
	return edged

#get and draw contours
def get_contours(img,imgCntr):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    for c in contours:
        object_area=cv2.contourArea(c)
        if object_area>500: #reduce noise
            cv2.drawContours(imgCntr, contours, -1, (0,255,0), 3)
            
            perimeter=cv2.arcLength(c,True)
            epsilon = 0.02*perimeter
            approx = cv2.approxPolyDP(c,epsilon,True)
            x_,y_,w,h=cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x_,y_),(x_+w,y_+h), (0,255,255), 3)
            cv2.putText(imgCntr, 'POINTS: '+str(len(approx)),(x_+w+15,y_+50), cv2.FONT_HERSHEY_COMPLEX, .5,(255,255,0),2)
            cv2.putText(imgCntr, 'AREA: '+str(int(object_area)),(x_+w+20,y_+20), cv2.FONT_HERSHEY_COMPLEX, .7,(255,255,0),2)
while True:
    _,img=frame.read()
    imgContour=img.copy()
    img_blur=cv2.GaussianBlur(img,(5,5),1)
    img_gray = cv2.cvtColor(img_blur,cv2.COLOR_BGR2GRAY)
    img_canny=canny_smart(img_gray)
    img_stack1=np.hstack([img,img_blur,cv2.cvtColor(img_gray,cv2.COLOR_GRAY2BGR)])
 
    
    # Taking a matrix of size 5 as the kernel
    kernel = np.ones((5,5), np.uint8)      
    img_dilation = cv2.dilate(img_canny, kernel, iterations=1)
    get_contours(img_dilation,imgContour)
    img_stack2=np.hstack([cv2.cvtColor(img_canny,cv2.COLOR_GRAY2BGR),cv2.cvtColor(img_dilation,cv2.COLOR_GRAY2BGR),imgContour])    
    
    v_stack=np.vstack([img_stack1,img_stack2])
    cv2.imshow("imgc",v_stack)
     
  
    
    if cv2.waitKey(1)& 0xFF== ord("x"):
        break
    
frame.release()
cv2.destroyAllWindows()