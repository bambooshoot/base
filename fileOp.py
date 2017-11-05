import os

def MkDir(dirList,dirPath):
    for curDir in dirList:
        os.makedirs("%s/%s"%(dirPath,curDir))

def IsEmptyDir(dirPath):
    return len(os.listdir(dirPath)) == 0

def DeleteDir(dirPath):
    os.rmdir(dirPath)
