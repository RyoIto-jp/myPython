# from module.getDir import getDir
# from module.getFilePath import getFilePath
from module.getPath import getPath

if __name__ == "__main__":

    cPath = getPath()
    
    myDir = cPath.getDir()
    myFullPath = cPath.getFileFullPath()
    myFileName = cPath.getFileName()

    print(myFullPath)
    print(myFileName)
    print(myDir)



