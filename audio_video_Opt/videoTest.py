import cv2
import time

if __name__ == '__main__':

    cv2.namedWindow("camera", 1)
    #开启ip摄像头
    video = "rtmp://www.easydss.com:10085/live/stream_1048279"
    capture = cv2.VideoCapture(video)

    while True:
        success, img = capture.read()
        if success:
            cv2.imshow("camera", img)

        #按键处理，注意，焦点应当在摄像头窗口，不是在终端命令行窗口
        key = cv2.waitKey(10)

        if key == 27:
            #esc键退出
            print("esc break...")
            break
    capture.release()
    cv2.destroyWindow("camera")