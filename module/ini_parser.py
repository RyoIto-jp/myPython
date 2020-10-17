
import urllib.request
import os
import os.path
import configparser
import pprint

class ini_parse:
    def __init__(self, url, path):
        """
        URLのみの指定ならPATH取得関数を実行
        そうでなれけばPATH引数をそのまま使用
        """
        self.url = url
        if path == '' and self.url != '':
            self.path = self.getSeverINI()
            self.err = None
        else:
            self.err = 'err' if not os.path.exists(path) else None
            self.path = path
        self.loadFile()

    def loadFile(self):
        if self.err:
            print('Pathが取得できませんでした。\n処理を中断します。')
            os._exit(0)
        self.ini = configparser.ConfigParser()
        self.ini.read(self.path, 'UTF-8')
    
    def getSection(self):
        # self.sections_list = ini.sections()
        return self.ini.sections()

    def getItems(self,mySection):
        items = self.ini.items(mySection)
        return items

    def getAllItems(self):
        section_list = self.getSection()
        items = [dict(self.ini.items(item)) for item in section_list]
        return items

    def getVersion(self):
        if self.err:
            ini_version = '0.0'
        else:
            ini = configparser.ConfigParser()
            ini.read(self.path, 'UTF-8')
            ini_version = ini['default']['version']
            urllib.request.urlcleanup()
        return ini_version

    def getSeverINI(self):
        # Download files from the server at a specified URL.
            ## 1st argument : Source URL
            ## 2nd argument : Send Path (If it is omitted, send it to a temporary folder.)
            ## 1st return : path
            ## 2nd return : header
        path, headers = urllib.request.urlretrieve(self.url)
        return path


# """ Path情報はここに集約"""
# # INI
# LOCAL_INI = "C:/System_Apps/app/Releases.ini"
# # UPDATE
# UPDATE_LST = 'http://tcs1262/test/ryoito/pc_opstate/update_app.php'
# UPDATE_DST = 'C:/System_Apps/Update'
# UPDATE_APP = 'mod02_upd.exe'

# '''2.ローカルのVersion情報(iniファイル)'''
# lcl_chk = ini_parse("", LOCAL_INI)
# lcl_ver = lcl_chk.getVersion()
# print("lcl:"+lcl_ver)


