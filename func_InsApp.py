import subprocess
import platform
import numpy as np
import codecs
# import os.path
# import sys
import os

import datetime  # For PC judgment. (Hostname,RecordTime)
import socket

import json  # For Editting to json file.
import func_mysql  # Insert for MySQL


def res_cmd(cmd):
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        shell=True).communicate()[0]


def get_app_list():
    App_List = []
    cmd_List = []
    item2 = []
    cmd_List.append(
        r"""reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /reg:64 /s | findstr "\<DisplayName" """)
    cmd_List.append(
        r"""reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /reg:64 /s | findstr "\<DisplayName" """)
    cmd_List.append(
        r"""reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /reg:32 /s | findstr "\<DisplayName" """)
    cmd_List.append(
        r"""reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /reg:32 /s | findstr "\<DisplayName" """)

    is_win64 = platform.machine() == "AMD64"
    if is_win64:
        cmd_List.append(
            r"""reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall" /reg:64 /s | findstr "\<DisplayName" """)
        cmd_List.append(
            r"""reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall" /reg:32 /s | findstr "\<DisplayName" """)

    for cmd in cmd_List:
        b = res_cmd(cmd)
        buf = b.decode("cp932")
        sp_str = "\r\n"
        buf2 = buf.split(sp_str)

        b = [s.replace('    DisplayName    REG_SZ    ', '') for s in buf2]
        c = [s.replace('    DisplayName_Localized    REG_SZ    ', '')
             for s in b]
        c = np.array(c)
        App_List = np.append(App_List, c, axis=0)

    Unique_Apps = App_List  # np.unique(App_List)
    Unique_Apps = np.sort(Unique_Apps)

    return Unique_Apps


def make_app_dic(item):
    """
    ListをDictに変換する。
        -----Parameters-----
        app_list : List
            ['apps1','apps2'...]
        -----Returns-----
        ret_dict : Dict
            {'host_name':host,'record_time':record,'apps1':app_list(1)}
    """
    # Init
    host = socket.gethostname()  # ホスト名を取得
    now_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    test_dict = {'host_name': host, 'record_time': now_time}

    item = sorted(list(set(item)))  # setで重複削除→Listでリスト化→sortedで並び替え。
    item = np.array(item)
    # item2 =[]

    i = 0
    for app in item:
        print(app)
        if 'Microsoft' in app or 'Windows' in app or 'C++' in app or 'Runtime_MSI' in app:
            item = np.delete(item, i, 0)
        else:
            i += 1

    item2 = np.array([buf for buf in item if not buf == ''])

    # Loop
    # i > len(item) then value = ''
    for i in range(190):
        print(i)
        if i >= len(item2):
            now_row = {'x_app' + str(i+1): ''}
        else:
            now_row = {'x_app' + str(i+1): item2[i]}

        test_dict.update(now_row)
        # print(test_dict)

    return test_dict


def write_json(r_array, f_json):
    """
    指定したjsonに配列を書き込み

        Parameters
        ----------
        r_array : Dictionary
            {cpu:0.0,mem:0.0,'time':'00:00:0'}
            書き込む配列
        f_json : String
            jsonファイルPath

        Returns
        -------
        json_num : Integer
            書き込みしたjsonの配列数
            次のIntervalに向けてデータ数を返す
            例)1分のデータを10個返したら次のInterval条件が成立

        Notes
        -----
            r_arrayは事前にDict形式にしておく。
    """
    # load json
    try:  # 初回は読み込めないのでエラー
        fw = open(f_json, 'r')
        json_data = json.load(fw)  # JSON形式で読み込む
        json_num = len(json_data)  # 要素数取得
        flg_json_update = 1  # error(初回)でないときはjson_dataのUPDATE(後述)
    except:  # 初回はID0で設定
        flg_json_update = 0  # errorはjson_dataのUPDATEをしない
        json_num = 0

    dic_row = {str(json_num): r_array}

    # loadしたjson_data配列にdic_row行を結合する
    if flg_json_update == 1:
        json_data.update(dic_row)
    else:  # 初回はjson_dataがないのでdic_rowをjson_dataとする
        json_data = dic_row

    # json_data(sec)をjsonに書き込み
    fw = codecs.open(f_json, 'w', 'utf-8')
    # json.dump関数でファイルに書き込む
    json.dump(json_data, fw, indent=4, ensure_ascii=False)

    return json_num


def InsApps():
    """
    A process that summarizes each process.
        -----Notes-----
            1. Get the installed apps in list format.
            2. Convert List to Dict.
            3. Define and initialize the json file.
            4. Write the installed apps to json file.
    """
    # Get the installed apps in list format.
    app_list = get_app_list()
    # Convert List to Dict.
    ret_dict = make_app_dic(app_list)
    # # Insert Database
    # ret = func_mysql.sql_send_apps(ret_dict)
    return ret_dict


if __name__ == '__main__':
    # execute only if run as a script
    InsApps()
    print('end')
