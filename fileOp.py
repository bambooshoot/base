import os,glob,shutil

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

def MakeSureDirExists(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)

def copyFile(srcFile,tarFile):
    if os.path.isfile(srcFile):
        print "copy %s %s"%(srcFile,tarFile)
        srcPathAndName = os.path.split(srcFile)
        if os.path.realpath(srcPathAndName[0]) == os.path.realpath(tarFile):
            print "WARNNING: %s can not be replaced by itself.\n"%srcFile
            return

        # shutil.copy(srcFile,tarFile)
        if(os.path.isdir(tarFile)):
            tarFile = os.path.join(tarFile,srcPathAndName[1])

        if os.path.isfile(tarFile):
            print "delete %s"%tarFile
            os.remove(tarFile)

        # shutil.copyfile(srcFile,tarFile)
        shutil.copy(srcFile,tarFile)