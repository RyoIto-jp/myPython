# -*- coding: utf-8 -*-

import sys
import os.path
import datetime
import psutil
import socket
import platform
import numpy as np
import json
import win32api
import win32net

# import time

import func_time
import func_mysql

""" Load UI(.ui) """
# from PySide2 import QtCore, QtGui, QtWidgets 
# from PySide2.QtUiTools import QUiLoader 
# CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

# """ Load UI(.py) """
from PySide2 import QtCore, QtUiTools, QtWidgets
from usinf import Ui_FORM

class UISample(QtWidgets.QMainWindow):
    """
        App全体の処理

            Notes
            -----
                Widgetのシグナル->スロットと、タイムイベントの設定。
        """
    def __init__(self, parent=None):
        super(UISample, self).__init__(parent)

        """ Load UI(.ui) """
        # self.ui = QUiLoader().load(os.path.join(CURRENT_PATH, 'ui/cpu_inf02.ui')) 
        # self.setCentralWidget(self.ui)
     
        """ Load UI(.py) """
        self.ui = Ui_FORM()
        self.ui.setupUi(self)

        # Signal作成
        self.ui.btn_cancel.clicked.connect(self.click_btn)

        # ユーザー名
        tus = psutil.users()
        tus = tus[0].name
        self.ui.label_7.setText(str(tus))

        # ホスト名を取得、表示
        host = socket.gethostname()
        self.ui.label_10.setText(str(host))

        # ipアドレスを取得、表示
        ip = socket.gethostbyname(host)
        self.ui.label_13.setText(str(ip))

        # OS
        os_ver = platform.platform(terse=True)
        self.ui.label_14.setText(str(platform.platform(terse=True)))

        # AD情報
        # user_info = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 2)
        # full_name = user_info["full_name"]
        # self.ui.label_15.setText(str(full_name))
        
        # json初期化
        sec_json = 'json/sec_inf.json'
        min_json = 'json/min_inf.json'
        min10_json = 'json/min10_inf.json'
        spec_json = 'json/spec_inf.json'

        try:
            os.remove(sec_json)
            os.remove(min_json)
            os.remove(min10_json)
            os.remove(spec_json)
        except FileNotFoundError:
            pass
        
        # PC_specの保存
        spec_dict = {'user_name':tus, 'host_name':host, 'ip_address': ip, 'os_ver': os_ver} # 配列を定義 
        spec_num = func_time.write_json(spec_dict, spec_json)

        # タイマーイベント Timer.startがインターバル
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.TimerProcess)#(tus, host, ip, os_ver))
        timer.start(1000)

    def click_btn(self):
        # 押したときの動作
        print("push!!")
        sys.exit()

    def TimerProcess(self):#, tus, host, ip, os_ver):
        """
            main処理部分
            """
        # time.sleep(3) #debug用 これがないと、デバッグでボタン押すとlast_inputが０に・・・

        # 未操作時間を取得
        last_input = round((win32api.GetTickCount() - win32api.GetLastInputInfo())/1000, 0) #last_input関数
        no_operation_time = datetime.timedelta(seconds=last_input) #時刻に変換
        is_operation = (last_input > 1) # ●秒以上 last_inputあれば無操作判定
        self.ui.label_2.setText(str(no_operation_time))

        # メモリ使用率を取得
        mem = psutil.virtual_memory()
        self.ui.label_4.setText(str(mem.percent) + " %")

        # CPU使用率を取得
        cpu = psutil.cpu_percent()
        self.ui.label_6.setText(str(cpu) + " %")


        dt_now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.ui.label_15.setText(str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))

        # Timer取得値を配列行としてリスト化。
        temp = (mem.percent, cpu, str(no_operation_time))
        sec_row = np.array(temp)
        sec_row = sec_row.reshape(1, 3)

        # 
        sec_json = 'json/sec_inf.json'
        sec_dict = {'cpu_usage':cpu, 'mem_usage':mem.percent, 'no_operation': is_operation} # 配列を定義 これが今後のDict.keys()
        min_num = func_time.write_json(sec_dict, sec_json)

        print('min_num:' + str(min_num))
        
        MinInterval = 59
        if (min_num)%MinInterval == 0 and min_num > 0:
            """ Calc MinArray """
            array_keys = list(sec_dict.keys())
            min_array = []
            min_array = func_time.time_matome(sec_json)

            """ Write to Widged """
            op_time_min = datetime.timedelta(seconds=round(min_array[2] * (MinInterval+1), 0))
            self.ui.label_20.setText(str(op_time_min)) #time
            self.ui.label_22.setText(str(min_array[1])) #mem
            self.ui.label_25.setText(str(min_array[0]))  #cpu
            self.ui.label_17.setText(str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))

            """ Write json """
            min_json = 'json/min_inf.json'
            min_dict = dict(zip(array_keys, min_array))
            min10num = func_time.write_json(min_dict, min_json)

            print('min10_num:' + str(min10num))
            min10Interval = 9
            if (min10num)%min10Interval == 0 and min10num > 0 :
                """ Calc Min10Array """
                min10_array = []
                min10_array = func_time.time_matome(min_json)

                """ Set to Widged """
                op_time_min10 = datetime.timedelta(seconds=round(min10_array[2] * (MinInterval+1) * (min10Interval+1), 0))
                self.ui.label_29.setText(str(op_time_min10)) #time
                self.ui.label_31.setText(str(min10_array[1])) #mem
                self.ui.label_26.setText(str(min10_array[0]))  #cpu
                self.ui.label_32.setText(str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")))

                """ Write json """
                min10_json = 'json/min10_inf.json'
                min10_dict = dict(zip(array_keys, min10_array))
                end_num = func_time.write_json(min10_dict, min10_json)
                print('end_num:'+str(end_num))

                """ send SQL """
                # record_time -> dict
                sql_dict = {'record_time':datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}
                # spec -> dict
                spec_json = 'json/spec_inf.json'
                spec_dict = func_time.read_json(spec_json)
                sql_dict.update(spec_dict)
                # print(sql_dict)
                # min10_dict
                sql_dict.update(min10_dict)
                # print(sql_dict)
                sql_dict['no_operation'] = str(op_time_min10)
                print(sql_dict)

                # send_sql
                ret = func_mysql.sql_send(sql_dict)



        # return



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    a = UISample()
    a.resize(560, 320)
    # a.windowTitle = "test"
    # a.show()
    sys.exit(app.exec_())
 