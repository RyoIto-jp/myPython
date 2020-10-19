# -*- coding: utf-8 -*-
"""
参考サイト様
https://skill-sharing.info/archives/143
"""

#
# 標準ライブラリ
#
#ファイルパスの確認
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
from module.getPath import getPath #Path取得クラス

import hashlib
hashes = {}

#イベントハンドラ
class ChangeHandler(FileSystemEventHandler):
    #ファイルやフォルダが作成された場合
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        # print('%sを作成しました。' % filename)
        os.system(os.path.join(ini_dir, 'on_created.bat') +
                  " " + filename + " を作成しました。")

    #ファイルやフォルダが更新された場合
    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        try:
            with open(filepath, 'rb') as f:
                checksum = hashlib.md5(f.read()).hexdigest()
            if filename not in hashes or (hashes[filename] != checksum):
                hashes[filename] = checksum
                # print('%sを変更しました' % filename)
                os.system(os.path.join(ini_dir, 'on_modified.bat') +
                          " " + filename + " を変更しました。")
            else:
                # ハッシュが既存のものと変更していない
                pass
        except:
            os.system(os.path.join(ini_dir, 'on_modified.bat') +
                      " " + filename + " を変更しました。(NoChkHsh)")

    #ファイルやフォルダが移動された場合
    def on_moved(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        # print('%sを移動しました。' % filename)
        os.system(os.path.join(ini_dir, 'on_moved.bat') +
                  " " + filename + " を移動しました。")

    #ファイルやフォルダが削除された場合
    def on_deleted(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        # print('%sを削除しました。' % filename)
        os.system(os.path.join(ini_dir, 'on_deleted.bat') +
                  " " + filename + "を削除しました。")


#メイン処理
if __name__ == '__main__':

    #起動ログ
    print('フォルダ・ファイル監視スクリプトを起動します。')

    #Pathの取得
    cPath = getPath()
    myDir = cPath.getDir()
    ini_dir = cPath.ini_dir
    print('監視フォルダを' + myDir + 'に設定します')

    #インスタンス作成
    event_handler = ChangeHandler()
    observer = Observer()

    #フォルダの監視
    observer.schedule(event_handler, myDir, recursive=True)

    #監視の開始
    observer.start()

    try:
        #無限ループ
        while True:
            #待機
            time.sleep(5.00)

    except KeyboardInterrupt:

        #監視の終了
        observer.stop()

        #スレッド停止を待つ
        observer.join()

        #終了ログ
        print('フォルダ・ファイル監視スクリプトを終了します。')
