import cv2
import numpy as np


def main():
    cv2.namedWindow("test")
    cap = cv2.VideoCapture("rtsp://192.168.14.139:8080/1122")
    classifier = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")

    while True:
        success, frame = cap.read()
        if not success:
            break

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

        if len(faceRects) > 0:

            for faceRect in faceRects:
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0))
        cv2.imshow("test", frame)
        key = cv2.waitKey(10)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            break
    cv2.destroyWindow("test")

if __name__ == '__main__':
    main()
