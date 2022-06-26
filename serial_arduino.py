import serial
import threading
import time

port = "COM3"
baud = 9600
ser = serial.Serial(port, baud, timeout=1)

def main():
    thread = threading.Thread(target=readthread, args=(ser, ))
    thread.start()

    cc = True

    while True:
        if cc:
            data = "CC 360 0 12.56".encode("utf-8")
            ser.write(data)
            cc = False
        else:
            data = "CW 360 0 12.56".encode("utf-8")
            ser.write(data)
            cc = True
        time.sleep(3)

def readthread(ser):
    while True:
        if ser.readable():
            res = ser.readline()
            print(res)
    ser.close()

main()