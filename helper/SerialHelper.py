#! /usr/bin/env python
# -*- coding: utf-8 -*-

#import sys
#import threading
#import time
import serial
import binascii

class SerialHelper(object):
    def __init__(self, Port="COM6", BaudRate="9600", ByteSize="8", Parity="N", Stopbits="1"):
        self.l_serial = None
        self.alive = False
        self.port = Port
        self.baudrate = BaudRate
        self.bytesize = ByteSize
        self.parity = Parity
        self.stopbits = Stopbits
        self.thresholdValue = 64
        self.receive_data = ""

    def start(self):
        self.l_serial = serial.Serial()
        self.l_serial.port = self.port
        self.l_serial.baudrate = self.baudrate
        self.l_serial.bytesize = int(self.bytesize)
        self.l_serial.parity = self.parity
        self.l_serial.stopbits = int(self.stopbits)
        self.l_serial.timeout = 2
        
        try:
            self.l_serial.open()
            if self.l_serial.isOpen():
                self.alive = True
        except:
            self.alive = False

    def stop(self):
        self.alive = False
        if self.l_serial.isOpen():
            self.l_serial.close()

    def read(self):
        while self.alive:
            try:
                number = self.l_serial.inWaiting()
                if number:
                    self.receive_data += self.l_serial.read(number).replace(binascii.unhexlify("00"), "")
                    if self.thresholdValue <= len(self.receive_data):
                        print(self.receive_data)
                        self.receive_data = ""
            except Exception as ex:
                print(ex.message)
                pass

    def write(self, data, isHex=False):
        if self.alive:
            if self.l_serial.isOpen():
                if isHex:
                    data = data.replace(" ", "").replace("\n", "")
                    data = binascii.unhexlify(data)
                self.l_serial.write(data)

if __name__ == '__main__':
    import threading
    ser = SerialHelper()
    ser.start()

    ser.write("123", isHex=False)
    thread_read = threading.Thread(target=ser.read)
    thread_read.setDaemon(True)
    thread_read.start()
    import time
    time.sleep(25)
    ser.stop()