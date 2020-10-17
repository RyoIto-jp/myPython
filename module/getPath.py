

import wx
import os


class getPath:
    def __init__(self):
        self.app = wx.App()
        self.ini_dir = os.getcwd()  # os.path.dirname(os.path.abspath(__file__))

    def getDir(self):
        dialog = wx.DirDialog(None, u'フォルダを選択してください', defaultPath=self.ini_dir) 
        if dialog.ShowModal() == wx.ID_CANCEL:
            wx.MessageBox(u'ファイルが選択されていません。\n処理を中断します。', u'ファイル選択エラー')
            os._exit(0)
        return dialog.GetPath()

    def getFilePath(self):
        filter = "text file(*.txt) | *.txt; | python file(*.py;*.pyw) | *.py;*.pyw | All file(*.*) | *.*"
        dialog = wx.FileDialog(
            None, u'ファイルを選択してください', self.ini_dir, '', filter)
        
        if dialog.ShowModal() == wx.ID_CANCEL:
            wx.MessageBox(u'ファイルが選択されていません。\n処理を中断します。', u'ファイル選択エラー')
            os._exit(0)
        self.myPath = dialog.GetPath()
            

    def getFileFullPath(self):
        self.getFilePath()
        return self.myPath

    def getFileName(self):
        self.getFilePath()
        return os.path.basename(self.myPath)

