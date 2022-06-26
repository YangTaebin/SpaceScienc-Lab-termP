import math

import cv2
import numpy as np

import serial
import threading
import time

class Point:
    P = ()
    def __init__(self, center):
        self.P = center
        self.current = 0

    def __add__(self, other):
        if type(other) == type(self):
            return Point((self.P[0] + other.P[0], self.P[1] + other.P[1]))
        return Point((self.P[0]+other, self.P[1]+other))

    def __radd__(self, other):
        if type(other) == type(self):
            return Point((self.P[0] + other.P[0], self.P[1] + other.P[1]))
        return Point((self.P[0]+other, self.P[1]+other))

    def __sub__(self, other):
        if type(other) == type(self):
            return Point((self.P[0] - other.P[0], self.P[1] - other.P[1]))
        return Point((self.P[0]-other, self.P[1]-other))

    def __rsub__(self, other):
        if type(other) == type(self):
            return Point((other.P[0]-self.P[0], other.P[1]-self.P[1]))
        return Point((other - self.P[0], other - self.P[1]))

    def __truediv__(self, other):
        return Point((int(self.P[0]/other), int(self.P[1]/other)))

    def __str__(self):
        return str(self.P)

    def __repr__(self):
        return str(self.P)

    def len(self):
        return math.sqrt(self.P[0]**2+self.P[1]**2)

    def __iter__(self):
        return self.P

    def __getitem__(self, item):
        return self.P[item]

def post_processing_image(src):
    img_shape = src.shape[:2]
    if img_shape[1] > img_shape[0]:
        img = cv2.resize(src, (img_size, int(img_shape[0] * (img_size / img_shape[1]))))
    else:
        img = cv2.resize(src, (int(img_shape[1] * (img_size / img_shape[0])), img_size))
    img = cv2.rotate(img, cv2.ROTATE_180)
    return img

def readthread(ser):
    while True:
        if ser.readable():
            res = ser.readline()
            print(res)
    ser.close()

def act(angle, xory):
    print(angle)
    if abs(angle) < 10 or abs(angle)>50: return None
    if angle >= 0 and xory == 0:
        data = "CC "+str(int(angle*10))+" 0 "+str(angle/2)
        print(data)
        ser.write(data.encode("utf-8"))
    elif angle < 0 and xory == 0:
        data = "CW " + str(int(-angle*10)) + " 0 " + str(-angle/2)
        print(data)
        ser.write(data.encode("utf-8"))
    elif angle >= 0 and xory == 1:
        data = "CC "+str(int(angle*10))+" 1 "+str(angle/2)
        print(data)
        ser.write(data.encode("utf-8"))
    elif angle < 0 and xory == 1:
        data = "CW " + str(int(-angle*10)) + " 1 " + str(-angle/2)
        print(data)
        ser.write(data.encode("utf-8"))


threshold = 10
max_diff = 5
img_size = 500
Angle_x = 100
Angle_y = 80
move = []
pre_move = []

port = "COM3"
baud = 9600
ser = serial.Serial(port, baud, timeout=1)

thread = threading.Thread(target=readthread, args=(ser, ))
thread.start()

a, b, c = None, None, None

cap = cv2.VideoCapture(0)

if cap.isOpened():
    ret, a = cap.read()
    ret, b = cap.read()
    a = post_processing_image(a)
    b = post_processing_image(b)

    while ret:
        ret, c = cap.read()
        if not ret:
            break
        c = post_processing_image(c)

        a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)

        diff1 = cv2.absdiff(a_gray, b_gray)
        diff2 = cv2.absdiff(b_gray, c_gray)

        ret, diff1_t = cv2.threshold(diff1, threshold, 255, cv2.THRESH_BINARY)
        ret, diff2_t = cv2.threshold(diff2, threshold, 255, cv2.THRESH_BINARY)

        diff = cv2.bitwise_and(diff1_t, diff2_t)

        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

        diff_cnt = cv2.countNonZero(diff)
        if diff_cnt > max_diff:
            nzero = np.nonzero(diff)
            center = Point((int((min(nzero[0])+max(nzero[0]))/2), int((min(nzero[1])+max(nzero[1]))/2)))
            move.append(center)
            # cv2.rectangle(c, (min(nzero[1]), min(nzero[0])), (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
            center = center + center

            if len(move) == 10:
                if pre_move == []:
                    pre_center = [Point((int(diff.shape[1]/2), int(diff.shape[0]/2)))]*10
                pre_center = sum(pre_move) / 10
                now_center = sum(move)/10
                direction = pre_center - now_center
                x_move = Angle_x * (direction[1]/diff.shape[1])
                y_move = Angle_y * (direction[0]/diff.shape[0])
                act(x_move, 0)
                act(y_move, 1)
                pre_move = move
                move = []


        cv2.imshow("image", c)
        cv2.imshow("diff", diff)

        a = b
        b = c

        key = cv2.waitKey(1)
        if key == ord("f"):
            break