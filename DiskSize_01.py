# -*- coding: utf-8 -*-

"""
ACS様提供の各サーバーのドライブ容量情報(.txt)をパースして、
MySQLへINSERTする。
"""

from pprint import pprint as pp
import func_mysql
import datetime


def getText(f_path, sql_statement):
    i = 1
    with open(f_path, encoding='sjis') as f:  # テキストファイルの読み込み
        for s in f.readlines():
            if i == 1:
                header = ["`" + x + "`" for x in list(s.split())]
                sql_statement += ','.join(header) + ' ) VALUES '
            else:
                temp_row = s.replace(' GB', 'GB').replace(
                    ' MB', 'MB').replace(' TB', 'TB').replace(' KB', 'KB')
                data_row = "','".join(temp_row.split())
                sql_statement += "('" + record_time + "','" + data_row + "'),"
            i += 1
    return sql_statement[:-1]  # 最後の「,」消す


if __name__ == "__main__":
    # Init Variables
    # Set Const
    data_row = []
    record_time = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
    sql_statement = 'INSERT INTO `disk_size` ( `record_time`,'
    sql_statement = getText(
        "C:\\gitwork\\24_DiskSize_ACS\\ShareStatus20200907.txt", sql_statement)

    mysql = func_mysql.mysql('172.16.77.103', '3306',
                             'aisan', 'aisan', 'manage_app')
    mysql.mult_insert(sql_statement, 'disk_size')  # Table Name未使用
