import cv2
import numpy as np
import time
camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
# 判断视频是否打开
if (camera.isOpened()):
    print('Open')
else:
    print('摄像头未打开')

# 测试用,查看视频size
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:'+repr(size))

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
background = None


redLower = np.array([26, 73, 46])  
redUpper = np.array([54, 255, 255])


def drawR(x,y,xt,yt,w,h,wt,ht):
    if x>xt:
        xt=x
    if y<yt:
        yt=y
    if w<wt:
        wt=w
    if h<ht:
        ht=h
    return xt,yt,wt,ht

while True:
    # 读取视频流
    grabbed, frame_lwpCV = camera.read()

    hsv=cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)  
    mask = cv2.dilate(mask, None, iterations=2)
    
    # 对帧进行预处理，先转灰度图，再进行高斯滤波。
    # 用高斯滤波进行模糊处理，进行处理的原因：每个输入的视频都会因自然震动、光照变化或者摄像头本身等原因而产生噪声。对噪声进行平滑是为了避免在运动和跟踪时将其检测出来。
    gray_lwpCV = cv2.cvtColor(frame_lwpCV, cv2.COLOR_BGR2GRAY)
    gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (71, 71), 0)

    cv2.imshow('d', gray_lwpCV)
    # 将第一帧设置为整个输入的背景
    if background is None:
        background = gray_lwpCV
        continue
    # 对于每个从背景之后读取的帧都会计算其与北京之间的差异，并得到一个差分图（different map）。
    # 还需要应用阈值来得到一幅黑白图像，并通过下面代码来膨胀（dilate）图像，从而对孔（hole）和缺陷（imperfection）进行归一化处理
    diff = cv2.absdiff(background, gray_lwpCV)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1] # 二值化阈值处理
    diff = cv2.dilate(diff, es, iterations=2) # 形态学膨胀

    # 显示矩形框
    image, contours, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
    
    image2, contours2, hierarchy2 = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 该函数计算一幅图像中目标的轮廓
    
    if len(contours) > 0 and len(contours2) > 0:
        c = max(contours, key = cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c) # 该函数计算矩形的边界框
        c2 = max(contours2, key = cv2.contourArea)
        (x2, y2, w2, h2) = cv2.boundingRect(c2) # 该函数计算矩形的边界框
        x,y,w,h=drawR(x,y,x2,y2,w,h,w2,h2)

        cv2.rectangle(frame_lwpCV, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('contours', frame_lwpCV)
    
    key = cv2.waitKey(1) & 0xFF
    # 按'q'健退出循环
    if key == ord('q'):
        break
# When everything done, release the capture
camera.release()
cv2.destroyAllWindows()
