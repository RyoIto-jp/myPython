

import wx
import os


class getPath:
    def __init__(self):
        self.app = wx.App()
        self.ini_dir = os.getcwd()  # os.path.dirname(os.path.abspath(__file__))

    def getDir(self):

        dialog = wx.DirDialog(None, u'フォルダを選択してください', defaultPath=self.ini_dir) 
        dialog.ShowModal()  # フォルダ選択ダイアログを表示

        return dialog.Path

    def getFilePath(self):

        filter = "python file(*.py;*.pyw) | *.py;*.pyw | All file(*.*) | *.*"
        dialog = wx.FileDialog(
            None, u'ファイルを選択してください', self.ini_dir, '', filter)
        dialog.ShowModal()  # フォルダ選択ダイアログを表示

        self.myPath =  dialog.Path

    def getFileFullPath(self):
        self.getFilePath()
        return self.myPath

    def getFileName(self):
        self.getFilePath()
        return os.path.basename(self.myPath)

