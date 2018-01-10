import cv2
import numpy as np
import pygame


def doSomething():
    if pygame.mixer.music.get_busy()!=1:
        print("play")
        pygame.mixer.music.play()
   
    


def catchFace(frame,classifier):
    size = frame.shape[:2]
    image = np.zeros(size, dtype=np.float16)
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cv2.equalizeHist(image, image)
    divisor = 8
    h, w = size
    minSize = (int(w / divisor), int(h / divisor))
    faceRects = classifier.detectMultiScale(
        image,
        scaleFactor=1.2,
        minNeighbors=2,
        flags=cv2.CASCADE_SCALE_IMAGE,
        minSize=minSize)
    return faceRects

def main():
    cv2.namedWindow("test")
    pygame.mixer.init()
    pygame.mixer.music.load(r"ad.mp3")
    cap = cv2.VideoCapture("rtsp://192.168.1.106:8080/1122")
    classifier = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    while True:
        success, frame = cap.read()
        if not success:
            break
        faceRects =catchFace(frame,classifier)
        if len(faceRects) > 0:
            for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))
            doSomething()
        else:
            if pygame.mixer.music.get_busy()==1:
                print("stop")
                pygame.mixer.music.stop()
            
        cv2.imshow("test", frame)
        key = cv2.waitKey(10)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            break
    cv2.destroyWindow("test")
    pygame.mixer.music.stop()

if __name__ == '__main__':
    main()
