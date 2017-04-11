#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import threading
import binascii
import platform

from myUI import SerialTool
from helper import SerialHelper

if platform.system() == "Windows":
    from  serial.tools import list_ports

import Tkinter as tk
#from Tkinter import ttk
import ttk


class MainSerialToolUI(SerialTool.SerialToolUI):
    def __init__(self, master=None):
        super(MainSerialToolUI, self).__init__()
        self.ser = None
        self.receive_count = 0
        self.receive_data = ""
        self.list_box_serial = list()
        self.find_all_serial()


    def __del__(self):
        pass

    def find_all_serial(self):
        '''
        获取到串口列表
        '''
        if platform.system() == "Windows":
            try:
                self.temp_serial = list()
                temp=list(list_ports.comports())
                self.temp_serial.append(temp[0][0])
                              
                              
                for item in self.temp_serial:
                    if item not in self.list_box_serial:
                        self.frm_left_listbox.insert("end", item)
                for item in self.list_box_serial:
                    if item not in self.temp_serial:
                        index = list(self.frm_left_listbox.get(0, self.frm_left_listbox.size())).index(item)
                        self.frm_left_listbox.delete(index)
                
                
                self.list_box_serial = self.temp_serial

                self.thread_findserial = threading.Timer(1, self.find_all_serial)
                self.thread_findserial.setDaemon(True)
                self.thread_findserial.start()
            except:
                pass

    def Toggle(self):
        '''
        打开关闭串口
        '''
        if self.frm_left_btn["text"] == "Open":
            try:
                self.currentStrCom = self.frm_left_listbox.get(self.frm_left_listbox.curselection())
                #print('Toggle中:'+self.currentStrCom)
                #print(self.currentStrCom)
                if platform.system() == "Windows":
                    self.port = self.currentStrCom.split(":")[0]
                    #print('self.port'+self.port)
                #波特率；奇偶；数据位；停止位设置
                self.baudrate = self.frm_left_combobox_baudrate.get()
                self.parity = self.frm_left_combobox_parity.get()
                self.databit = self.frm_left_combobox_databit.get()
                self.stopbit = self.frm_left_combobox_stopbit.get()
                self.ser = SerialHelper.SerialHelper(Port=self.port,
                                                     BaudRate=self.baudrate,
                                                     ByteSize=self.databit,
                                                     Parity=self.parity,
                                                     Stopbits=self.stopbit)
                #print(self.baudrate)
                #print(self.parity)
                #print(self.databit)
                #print(self.stopbit)
                
                self.ser.start()
                if self.ser.alive:
                    self.frm_status_label["text"] = "Open [{0}] Successful!".format(self.currentStrCom)
                    self.frm_status_label["fg"] = "#66CD00"
                    self.frm_left_btn["text"] = "Close"
                    self.frm_left_btn["bg"] = "#F08080"

                    self.thread_read = threading.Thread(target=self.SerialRead)
                    self.thread_read.setDaemon(True)
                    self.thread_read.start()

            except Exception:
                try:
                    self.frm_status_label["text"] = "Open [{0}] Failed!".format(self.currentStrCom)
                    self.frm_status_label["fg"] = "#DC143C"
                except:
                    pass

        elif self.frm_left_btn["text"] == "Close":
            try:
                self.ser.stop()
                self.receive_count = 0
            except:
                pass
            self.frm_left_btn["text"] = "Open"
            self.frm_left_btn["bg"] = "#008B8B"
            self.frm_status_label["text"] = "Close Serial Successful!"
            self.frm_status_label["fg"] = "#8DEEEE"

    def Open(self, event):
        self.Toggle()

    def Clear(self):
        self.frm_right_receive.delete("0.0", "end")
        self.receive_count = 0

    def Send(self):
        '''
        向已打开的串口发送数据
        如果为Hex发送，示例："31 32 33" [即为字符串 "123"]
        '''
        if self.ser:
            try:
                # 发送新行
                if self.new_line_cbtn_var.get() == 0:
                    send_data = str(self.frm_right_send.get("0.0", "end").encode("gbk")).strip()
                else:
                    send_data = str(self.frm_right_send.get("0.0", "end")).strip() + "\r\n"  
                
                # 是否十六进制发送
                if self.send_hex_cbtn_var.get() == 1:
                    self.ser.write(send_data, isHex=True)
                else:
                    self.ser.write(send_data)
            except Exception as ex:
                self.frm_right_receive.insert("end", str(ex) + "\n")

    def SerialRead(self):
        '''
        线程读取串口发送的数据
        '''
        #print('SerialRead之中')
        while self.ser.alive:
            try:
                n = self.ser.l_serial.inWaiting()
                print('可接受的字节数:'+str(n))
                if True:
                    print('here')
                    #print(self.ser.l_serial.read(2))
                    self.receive_data=self.ser.l_serial.readline()
                    #self.receive_data += self.ser.l_serial.read(2).replace(binascii.unhexlify("00"), "")
                    print('self.receive_data')
                    print(self.receive_data)
                    if self.thresholdValue <= len(self.receive_data):
                        self.receive_count += 1

                        # 接收显示是否为Hex
                        #if self.receive_hex_cbtn_var.get() == 1:
                            #self.receive_data = self.space_b2a_hex(self.receive_data)
                        self.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) + " - "
                                                      + str(self.receive_count) + "]:\n", "red")
                        #self.frm_right_receive.insert("end", self.receive_data + "\n")
                        #mystr=int(binascii.b2a_hex(self.receive_data),16)
                        astr=''.join([chr(b) for b in self.receive_data])
                        self.frm_right_receive.insert("end",  astr +"\n")
                        self.frm_right_receive.see("end")
                        self.receive_data = ""
                else:
                    self.frm_right_receive.insert("end", "未接收到数据\n")
            except Exception:
                print('here is Exception')
                self.receive_data = ""
                #self.Toggle()


    def space_b2a_hex(self, data):
        '''
        格式化接收到的数据字符串
        示例：123 --> 31 32 33
        '''
        new_data_list = list()
        new_data = ""

        hex_data = binascii.b2a_hex(data)
        temp_data = ""
        for index,value in enumerate(hex_data): 
            temp_data += value
            if len(temp_data) == 2:
                new_data_list.append(temp_data)
                temp_data = ""
        for index,value in enumerate(new_data_list):
            if index%25 == 0 and index != 0:
                new_data += "\n"
            new_data += value
            new_data += " "

        return new_data

if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.title("Serial Tool:周文")
    mystyle = ttk.Style()
    
    mystyle.theme_create('mystyle', parent=None,
                             settings = {
                                            "TCombobox":
                                            {
                                                "configure":
                                                {
                                                    "selectbackground": "#292929",
                                                    "fieldbackground": "#292929",
                                                    "background": "#292929",
                                                    "foreground": "#FFFFFF"
                                                }
                                            }
                                        })
    
    mystyle.theme_use('mystyle')
    MainSerialToolUI(master=root)
    root.resizable(False, False)
    #input("wh fccd rye second\n")
    root.mainloop()
