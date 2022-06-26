import cv2
import numpy as np
import time

def color_area():
    video_capture = cv2.VideoCapture(1)
    img_size = 500
    while 1:
        grabbed, src = video_capture.read()

        img_shape = src.shape[:2]
        if img_shape[1] > img_shape[0]: img = cv2.resize(src, (img_size, int(img_shape[0]*(img_size/img_shape[1]))))
        else: img = cv2.resize(src, (int(img_shape[1]*(img_size/img_shape[0])), img_size))
        img = cv2.rotate(img, cv2.ROTATE_180)

        # dst = cv2.fastNlMeansDenoisingColored(blur,None,10,10,7,21)
        # src1 = dst
        # hsv1 = cv2.cvtColor(src1, cv2.COLOR_BGR2HSV)
        # lowerb1=(170, 100, 100)
        # upperb1=(180, 255, 255)
        # dst1 = cv2.inRange(hsv1, lowerb1, upperb1)
        # dilation = cv2.dilate(dst1, kernel, iterations=2)

        cv2.imshow("Origin", img)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
color_area()