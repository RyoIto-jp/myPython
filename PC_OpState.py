# -*- coding: utf-8 -*-
import psutil
from socket import gethostname, gethostbyname
from platform import platform
from win32api import GetTickCount, GetLastInputInfo
import time
import threading

import numpy as np
import datetime
import func_mysql
import func_InsApp

#debug
from pprint import pprint as pp

class main_opstate:
    """PCモニタアプリの本体部分
        __init__        :初期化処理
        scheduler       :定期実行用のスケジューラ
        get_spec        :PC情報を取得
        get_lastinput   :未操作時間を取得
        get_state       :辞書形式でPC状態を取得 sec単位
        mean_dictionary :配列(Dict)の項目毎に平均値を算出
        record_sec      :1秒毎にPC状態を取得して配列(sec_table)に格納
        reset_sec       :sec_tableをリセット
        record_table    :sec_tableの平均値を取得してmin_tableを作成
        record_min      :1分毎の処理
        record_min10    :10分毎の処理
        get_sql_dict    :SQL実行用の配列を作成
        TimerProsess    :定期実行する処理を記述
        """

    def __init__(self, interval):
        self.INTERVAL = interval
        self.SEC_INTVL = (60 / self.INTERVAL)
        self.MIN_INTVL = 10
        self.sec_table = []
        self.min_table = []
        self.cnt = psutil.cpu_count()
        self.mysql = func_mysql.mysql(
            'localhost', '3306', 'root', 'root', 'admin_pc_usage')

    def scheduler(self, f, wait=True):
        """定期実行用のスケジューラ
            指定したインターバル毎に処理を実行する。
            通常のtime.sleepでは処理による遅れ時間が考慮できない。
            そのため、Loop毎にスレッドを作成してインターバルを維持する。
            INTERVAL    :インターバル(秒)
            f           :定期実行する関数
            """
        base_time = time.time()
        next_time = 0
        while True:
            t = threading.Thread(target=f)
            t.start()
            if wait:
                t.join()
            next_time = ((base_time - time.time()) %
                         self.INTERVAL) or self.INTERVAL
            time.sleep(next_time)

    def get_spec(self):
        """PC情報を取得"""
        host = gethostname()
        self.spec_dict = {
            'user_name': psutil.users()[0].name,        # ユーザー名
            'host_name': host,                          # ホスト名
            'ip_address': gethostbyname(host),          # ipアドレス
            'os_ver': platform(terse=True)              # OS
        }

    def get_lastinput(self):
        """未操作時間を取得
            ◆ 操作後 1秒以上経過していたら1(未操作)を返します。
            ------------
            GetTickCount()    :システム起動後時間
            GetLastInputInfo():最後の入力イベントの時刻
            """
        last_input = round(
            (GetTickCount() - GetLastInputInfo()) / 1000, 0)  # last_input関数
        return (last_input > 5)

    def get_state(self):
        """ 辞書形式でPC状態を取得 sec単位
            """
        sec_dict = {
            'cpu_usage': psutil.cpu_percent(),              # メモリ使用率
            'mem_usage': psutil.virtual_memory().percent,   # CPU使用率
            'no_operation': self.get_lastinput()            # 未操作判定
        }
        return sec_dict

    def mean_dictionary(self, ave_dic):
        """ 配列(Dict)の項目毎に平均値を算出
            {no：{key1:val1,key2:val2}} --> {key1:val1,key2:val2}
            row         : 1行ごとのVALUEリスト
            tmp_row     : rowをfloatに変換
            np_arr      : tmp_rowを2次元方向に結合したテーブル
            np_mean_raw : np.mean()で平均値を算出
            np_mean     : np_mean_raw を小数点以下2桁で四捨五入
            array_keys  : 辞書形式に戻すために、元配列のKeyを取得
            """
        np_arr = None
        for row in ave_dic.values():                                    # get npArray data in ave_dic
            tmp_row = np.array([float(x) for x in list(row.values())])
            try:                # Not First
                np_arr = np.append(np_arr, [tmp_row], axis=0)
            except ValueError:  # First Time is empty[np_arr]
                # 現状、3項目のみ。汎用化可能？？
                np_arr = tmp_row.reshape(1, 3)
        # Calc the average of each element in the array.
        np_mean_raw = np.mean(np_arr, axis=0)
        np_mean = [round(x, 2) for x in np_mean_raw]
        # Zip the Dictionary from Keys&Values(mean)
        array_keys = list(ave_dic['0'].keys())
        return dict(zip(array_keys, np_mean))

    def record_sec(self):
        """1秒毎にPC状態を取得して配列(sec_table)に格納
            dic_num     : 配列(sec_table)のデータ数
            sec_row     : 現在のPC状態（配列）
            dic_row     : sec_table格納用に整形 {key:val} --> {idx:{key:val}}
            """
        dic_num = len(self.sec_table)
        sec_row = self.get_state()
        dic_row = {str(dic_num): sec_row}
        # pprint(dic_row)
        try:    # not first
            self.sec_table.update(dic_row)
        except:  # For first
            self.sec_table = dic_row

    def reset_sec(self):
        """sec_tableをリセット
            sec_table:
            """
        self.sec_table = []

    def record_table(self, raw_tbl, out_dic):
        """sec_tableの平均値を取得してmin_tableを作成
            var:
            """
        raw_row = self.mean_dictionary(raw_tbl)
        dic_num = len(out_dic)
        dic_row = {str(dic_num): raw_row}
        try:
            out_dic.update(dic_row)
        except:
            out_dic = dic_row
        return out_dic

    def record_min(self):
        """1分毎の処理
            out_dic:
            """
        out_dic = self.record_table(self.sec_table, self.min_table)
        self.min_table = out_dic
        pp(self.min_table)

    def record_min10(self):
        """10分毎の処理
            min_tableの平均値とって返すだけ。
            """
        min10_data = self.mean_dictionary(self.min_table)
        return min10_data

    def get_sql_dict(self):
        """SQL実行用の配列を作成
            sql_dict            : 現在時刻 + PC情報 + PC状態(10分平均)
            ['no_operation']    : 10分間のOFF/ON比率 --> 10分間のOFF時間(hh:mm:ss)
            """
        # record_time -> dict
        sql_dict = {'record_time': datetime.datetime.now().strftime(
            "%Y/%m/%d %H:%M:%S")}
        # spec -> dict
        sql_dict.update(self.spec_dict)
        # min10_dict
        sql_dict.update(self.record_min10())
        # calc no_operation
        sql_dict['no_operation'] = datetime.timedelta(
            seconds=sql_dict['no_operation'] * 600)
        
        proc_json = self.procList()
        if proc_json:
            proc_dict = {'procList': proc_json}
            sql_dict.update(proc_dict)
        return sql_dict

    def procList(self):
        flg = 0
        pp_vals = []
        for x in psutil.process_iter({'cpu_percent', 'memory_info', 'name', 'username'}):
            if x.info['cpu_percent'] > 0.1 * self.cnt and x.info['username'] is not None:
                if 'adex' in x.info['username'] or 'yon2mk23' in x.info['username']:
                    if len(pp_vals) > 0:
                        for row in pp_vals.keys():
                            if not x.info['name'] is None:
                                if x.info['name'][:-4] in row:
                                    pp_vals[x.info['name'][:-4]]['cpu'] = round(
                                        float(pp_vals[x.info['name'][:-4]]['cpu']) + float(x.info['cpu_percent']), 1)
                                    flg = 1
                    if flg == 0:
                        s_key = ["cpu", "mem"]
                        s_val = round(
                            x.info['cpu_percent']/self.cnt, 1), round(x.info['memory_info'].rss/1024/1024, 1)
                        n_key = [x.info['name'][:-4]]
                        n_val = [dict(zip(s_key, s_val))]
                        pp_val = dict(zip(n_key, n_val))
                        try:
                            pp_vals.update(pp_val)
                        except:
                            pp_vals = pp_val
                    flg = 0
        pp(pp_vals, width=100)
        print('\n')

        proc_json = ""
        if len(pp_vals) > 0:
            proc_json = str(pp_vals).replace('\'', '"')

        return proc_json

    def TimerProsess(self):
        """定期実行する処理を記述
        """
        global recSTART                             # 処理時間の計測
        self.record_sec()                           # 1秒毎の処理
        print(time.time()-recSTART)
        if len(self.sec_table) >= self.SEC_INTVL:   # 1分毎の処理
            self.record_min()
            self.reset_sec()
        if len(self.min_table) >= self.MIN_INTVL:   # 10分毎の処理
            sql_dict = self.get_sql_dict()
            self.mysql.sql_insert(sql_dict, "pc_log") ##################################
            self.min_table = []


#-----------------
recSTART = time.time()  # 処理時間計測スタート
MAIN_APP = main_opstate(5)  # クラス定義とインターバル指定
MAIN_APP.get_spec()  # PCスペック取得
# MAIN_APP.mysql.sql_insert(  # インストールアプリ一覧の取得
#     func_InsApp.InsApps(), "installed_apps")
MAIN_APP.scheduler(MAIN_APP.TimerProsess, False)  # インターバル処理
