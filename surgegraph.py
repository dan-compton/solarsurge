import sys, serial
import numpy as np
import struct
import pyaudio
from collections import deque
import math
from matplotlib import pyplot as plt

class AnalogData:
    def __init__(self,maxlen):
        self.counter = 0
        self.ax = deque([0.0]*maxlen)
        self.ay = deque([0.0]*maxlen)
        self.maxlen = maxlen

    def addToBuff(self,buff,val):
        if len(buff) < self.maxlen:
            buff.append(val)
        else:
            buff.pop()
            buff.appendleft(val)
    
    def add(self,data):
        self.addToBuff(self.ay,data[0])
        self.addToBuff(self.ax,0)

class AnalogPlot:
    def __init__(self,analogData):
        plt.ion()
        self.axline, = plt.plot(analogData.ax)
        self.ayline, = plt.plot(analogData.ay)
        plt.ylim([2.5,4.5])
        plt.xlim([0,100])

    def update(self,analogData):
        self.axline.set_ydata(analogData.ax)
        self.axline.set_ydata(analogData.ay)
        plt.draw()

def main():
    analogData = AnalogData(100)
    analogPlot = AnalogPlot(analogData)
    ser = serial.Serial('/dev/ttyACM0',9600)

    while True:
        line = ser.readline()
        try:
            data = [float(val) for val in line.split()]
            if len(data) > 0:
                analogData.add(data)
                analogPlot.update(analogData)
        except:
            continue

if __name__ == '__main__':
    main()
