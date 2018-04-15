import os

def MkDir(dirList,dirPath):
    for curDir in dirList:
    	dirName="%s/%s"%(dirPath,curDir)
    	if not os.path.isdir(dirName):
        	os.makedirs(dirName)

def IsEmptyDir(dirPath):
    return len(os.listdir(dirPath)) == 0

def DeleteDir(dirPath):
    os.rmdir(dirPath)

def DeleteFiles(fileFilter):
    for curFile in glob.glob(fileFilter):
        os.remove(curFile)