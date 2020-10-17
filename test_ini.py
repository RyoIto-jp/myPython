# -*- coding: utf-8 -*-
from module.ini_parser import ini_parse  # INIデータの取り扱いクラス

""" Path情報はここに集約"""
# INI
LOCAL_INI = "C:/temp/10_python_201017/test/myInfo.ini"

'''2.ローカルのiniファイル'''
myINI = ini_parse("", LOCAL_INI)

# 全セクション取得
print(myINI.ini.sections())

# 全データ取得
allINI = myINI.getAllItems()
print(allINI)

# [database]セクションのデータを取得
print(dict(myINI.getItems('database')))

# [default]セクションの version情報を取得
print(myINI.ini['default']['version'])
