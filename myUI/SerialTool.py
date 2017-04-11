#! /usr/bin/env python
# -*- coding: utf-8 -*-
from myUI import Adaptive

import Tkinter as tk
#from Tkinter import ttk
import ttk
# set size and font
#import Adaptive
size_dict = Adaptive.size_dict
font = Adaptive.monaco_font


class SerialToolUI(object):
    def __init__(self, master=None):
        self.root = master
        self.create_frame()
        self.thresholdValue = 1

    def create_frame(self):
        '''
        新建窗口，分为上下2个部分，下半部分为状态栏
        '''
        self.frm = tk.LabelFrame(self.root, text="", bg="#292929", fg="#1E90FF")
        self.frm_status = tk.LabelFrame(self.root, text="", bg="#292929", fg="#1E90FF")

        self.frm.grid(row=0, column=0, sticky="wesn")
        self.frm_status.grid(row=1, column=0, sticky="wesn")

        self.create_frm()
        self.create_frm_status()

    def create_frm(self):
        '''
        上半部分窗口分为左右2个部分
        '''
        self.frm_left = tk.LabelFrame(self.frm, text="", bg="#292929", fg="#1E90FF")
        self.frm_right = tk.LabelFrame(self.frm, text="", bg="#292929", fg="#1E90FF")

        self.frm_left.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_right.grid(row=0, column=1, padx=5, pady=5, sticky="wesn")

        self.create_frm_left()
        self.create_frm_right()

    def create_frm_left(self):
        '''
        上半部分左边窗口：
        Listbox显示可用的COM口
        Button按钮点击连接设备
        '''
        self.frm_left_label = tk.Label(self.frm_left, text="Serial Ports",
                                       bg="#292929", fg="#E0EEEE",
                                       font=font)
        self.frm_left_listbox = tk.Listbox(self.frm_left,
                                           height=size_dict["list_box_height"],
                                           bg="#292929", fg="#1E90FF",
                                           selectbackground="#00B2EE",
                                           font=font)
        self.frm_left_serial_set = tk.LabelFrame(self.frm_left, text="",
                                                 bg="#292929", fg="#1E90FF")
        self.frm_left_btn = tk.Button(self.frm_left, text="Open",
                                      activebackground="#00B2EE",
                                      activeforeground="#E0EEEE",
                                      bg="#008B8B", fg="#FFFFFF",
                                      font=font,
                                      command=self.Toggle)

        self.frm_left_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.frm_left_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_left_serial_set.grid(row=2, column=0, padx=5, pady=5, sticky="wesn")
        self.frm_left_btn.grid(row=3, column=0, padx=5, pady=5, sticky="wesn")

        self.frm_left_listbox.bind("<Double-Button-1>", self.Open)
        self.create_frm_left_serial_set()

    def create_frm_left_serial_set(self):
        '''
        串口配置，比如波特率，奇偶校验等
        '''
        setting_label_list = ["BaudRate :", "Parity :", "DataBit :", "StopBit :"]
        baudrate_list = ["1200", "2400", "4800", "9600", "14400", "19200", "38400",
                         "43000", "57600", "76800", "115200", "12800"]
        # PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
        parity_list = ["N", "E", "O", "M", "S"]
        bytesize_list = ["5", "6", "7", "8"]
        stopbits_list = ["1", "1.5", "2"]
        for index,item in enumerate(setting_label_list):
            frm_left_label_temp = tk.Label(self.frm_left_serial_set, text=item,
                                           bg="#292929", fg="#E0EEEE",
                                           font=('Monaco', 10))
            frm_left_label_temp.grid(row=index, column=0, padx=1, pady=2, sticky="e")
        self.frm_left_combobox_baudrate = ttk.Combobox(self.frm_left_serial_set,
                                                       width=15,
                                                       values=baudrate_list)
        self.frm_left_combobox_parity = ttk.Combobox(self.frm_left_serial_set,
                                                       width=15,
                                                       values=parity_list)
        self.frm_left_combobox_databit = ttk.Combobox(self.frm_left_serial_set,
                                                       width=15,
                                                       values=bytesize_list)
        self.frm_left_combobox_stopbit = ttk.Combobox(self.frm_left_serial_set,
                                                       width=15,
                                                       values=stopbits_list)
        self.frm_left_combobox_baudrate.grid(row=0, column=1, padx=2, pady=2, sticky="e")
        self.frm_left_combobox_parity.grid(row=1, column=1, padx=2, pady=2, sticky="e")
        self.frm_left_combobox_databit.grid(row=2, column=1, padx=2, pady=2, sticky="e")
        self.frm_left_combobox_stopbit.grid(row=3, column=1, padx=2, pady=2, sticky="e")

        self.frm_left_combobox_baudrate.current(3)
        self.frm_left_combobox_parity.current(0)
        self.frm_left_combobox_databit.current(3)
        self.frm_left_combobox_stopbit.current(0)

    def create_frm_right(self):
        '''
        上半部分右边窗口：
        分为4个部分：
        1、Label显示和重置按钮和发送按钮
        2、Text显示（发送的数据）
        3、Label显示和十六进制选择显示和清除接收信息按钮
        4、Text显示接收到的信息
        '''
        self.frm_right_reset = tk.LabelFrame(self.frm_right, text="",
                                             bg="#292929", fg="#1E90FF")
        self.frm_right_send = tk.Text(self.frm_right,
                                      width=50, height=size_dict["send_text_height"],
                                      bg="#292929", fg="#1E90FF",
                                      font=("Monaco", 9))
        self.frm_right_clear = tk.LabelFrame(self.frm_right, text="",
                                             bg="#292929", fg="#1E90FF")
        self.frm_right_receive = tk.Text(self.frm_right,
                                         width=50, height=size_dict["receive_text_height"],
                                         bg="#292929", fg="#1E90FF",
                                         font=("Monaco", 9))

        self.frm_right_reset.grid(row=0, column=0, padx=1, sticky="wesn")
        self.frm_right_send.grid(row=1, column=0, padx=1, sticky="wesn")
        self.frm_right_clear.grid(row=2, column=0, padx=1, sticky="wesn")
        self.frm_right_receive.grid(row=3, column=0, padx=1, sticky="wesn")

        self.frm_right_receive.tag_config("green", foreground="#228B22")

        self.create_frm_right_reset()
        self.create_frm_right_clear()

    def create_frm_right_reset(self):
        '''
        1、Label显示和重置按钮和发送按钮
        '''
        self.frm_right_reset_label = tk.Label(self.frm_right_reset,
                                              text="Data Send" + " "*size_dict["reset_label_width"],
                                              bg="#292929", fg="#E0EEEE",
                                              font=font)
        self.new_line_cbtn_var = tk.IntVar()
        self.send_hex_cbtn_var = tk.IntVar()
        self.frm_right_reset_newLine_checkbtn = tk.Checkbutton(self.frm_right_reset,
                                                               text="New Line",
                                                               variable=self.new_line_cbtn_var,
                                                               bg="#292929", fg="#FFFFFF",
                                                               activebackground="#292929",
                                                               selectcolor="#292929",
                                                               font=font)
        self.frm_right_reset_hex_checkbtn = tk.Checkbutton(self.frm_right_reset,
                                                           text="Hex",
                                                           variable=self.send_hex_cbtn_var,
                                                           bg="#292929", fg="#FFFFFF",
                                                           activebackground="#292929",
                                                           selectcolor="#292929",
                                                           font=font)
        self.frm_right_reset_btn = tk.Button(self.frm_right_reset, text="Reset",
                                             activebackground="#00B2EE",
                                             activeforeground="#E0EEEE",
                                             bg="#008B8B", fg="#FFFFFF",
                                             width=10,
                                             font=font,
                                             command=self.Reset)
        self.frm_right_send_btn = tk.Button(self.frm_right_reset, text="Send",
                                            activebackground="#00B2EE",
                                            activeforeground="#E0EEEE",
                                            bg="#008B8B", fg="#FFFFFF",
                                            width=10,
                                            font=font,
                                            command=self.Send)

        self.frm_right_reset_label.grid(row=0, column=0, sticky="w")
        self.frm_right_reset_newLine_checkbtn.grid(row=0, column=1, sticky="wesn")
        self.frm_right_reset_hex_checkbtn.grid(row=0, column=2, sticky="wesn")
        self.frm_right_reset_btn.grid(row=0, column=3, padx=5, pady=5, sticky="wesn")
        self.frm_right_send_btn.grid(row=0, column=4, padx=5, pady=5, sticky="wesn")

    def create_frm_right_clear(self):
        '''
        3、Label显示和十六进制显示和清除接收信息按钮
        '''
        self.receive_hex_cbtn_var = tk.IntVar()
        self.frm_right_clear_label = tk.Label(self.frm_right_clear,
                                              text="Data Received"+ " "*size_dict["clear_label_width"],
                                              bg="#292929", fg="#E0EEEE",
                                              font=font)
        self.frm_right_threshold_label = tk.Label(self.frm_right_clear,
                                                  text="Threshold:",
                                                  bg="#292929", fg="#E0EEEE",
                                                  font=font)
        self.thresholdStr = tk.StringVar()
        self.frm_right_threshold_entry = tk.Entry(self.frm_right_clear,
                                                  textvariable=self.thresholdStr,
                                                  width=6,
                                                  bg="#292929", fg="#E0EEEE",
                                                  font=font)
        self.frm_right_hex_checkbtn = tk.Checkbutton(self.frm_right_clear,
                                                     text="Hex",
                                                     variable=self.receive_hex_cbtn_var,
                                                     bg="#292929", fg="#FFFFFF",
                                                     activebackground="#292929",
                                                     relief="flat",
                                                     selectcolor="#292929",
                                                     font=font)
        self.frm_right_clear_btn = tk.Button(self.frm_right_clear, text="Clear",
                                             activebackground="#00B2EE",
                                             activeforeground="#E0EEEE",
                                             bg="#008B8B", fg="#FFFFFF",
                                             width=10,
                                             font=font,
                                             command=self.Clear)

        self.frm_right_clear_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        #self.frm_right_threshold_label.grid(row=0, column=1, padx=5, pady=5, sticky="wesn")
        #self.frm_right_threshold_entry.grid(row=0, column=2, padx=5, pady=5, sticky="wesn")
        #self.frm_right_hex_checkbtn.grid(row=0, column=3, padx=5, pady=5, sticky="wesn")
        self.frm_right_clear_btn.grid(row=0, column=4, padx=5, pady=5, sticky="wesn")

        self.thresholdStr.set(1)
        self.thresholdStr.trace('w', self.GetThresholdValue)

    def create_frm_status(self):
        '''
        下半部分状态栏窗口
        '''
        self.frm_status_label = tk.Label(self.frm_status, text="Ready",
                                         bg="#292929", fg="#8DEEEE",
                                         font=font)
        self.frm_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def Toggle(self):
        pass

    def Open(self, event):
        pass

    def Reset(self):
        self.frm_right_send.delete("0.0", "end")

    def Send(self):
        pass

    def Clear(self):
        self.frm_right_receive.delete("0.0", "end")

    def GetThresholdValue(self, *args):
        try:
            self.thresholdValue = int(self.thresholdStr.get())
        except:
            pass


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    combostyle = ttk.Style()
    combostyle.theme_create("combostyle", parent="alt",
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
    combostyle.theme_use('combostyle')
    root.title("Serial-Tool")
    SerialToolUI(master=root)
    root.resizable(False, False)
    root.mainloop()
