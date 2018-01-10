import cv2
import numpy as np

redLower = np.array([26, 73, 46])  
redUpper = np.array([54, 255, 255])

camera = cv2.VideoCapture(0)

while True:
    ret, frame= camera.read()
    if not ret:
        break
    

    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv, redLower, redUpper)
    cv2.imshow('mask', mask)
    mask = cv2.erode(mask, None, iterations=2)  
    #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点  
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('contours', frame)
    key = cv2.waitKey(1) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
