import os,glob,shutil,time,fnmatch

import ctypes
import os
import platform
import sys

def get_free_space_mb(folder):
    """ Return folder/drive free space (in bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value/1024/1024/1024 
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize/1024/1024

def MkDir(dirList,dirPath):
    for curDir in dirList:
    	dirName="%s/%s"%(dirPath,curDir)
    	if not os.path.isdir(dirName):
        	os.makedirs(dirName)

def IsEmptyDir(dirPath):
    return len(os.listdir(dirPath)) == 0

def DeleteDir(dirPath):
    print "Remove folder: %s"%dirPath
    os.rmdir(dirPath)

def DeleteFiles(fileFilter):
    for curFile in glob.glob(fileFilter):
        print "Remove file: %s"%curFile
        os.remove(curFile)

def MakeSureDirExists(folder):
    if not os.path.isdir(folder):
        print "Make folder: %s"%folder
        os.makedirs(folder)

def IsSrcNewFile(srcFile,tarFile):
    return os.path.getmtime(srcFile) > os.path.getmtime(tarFile)

def FileTime(fileName):
    statInfo = os.stat(fileName)
    return time.localtime(statInfo.st_mtime)

def ListFile(path,symbolname):
    resultList=[]
    if os.path.isdir(path):
        fileList=os.listdir(path)
        
        for item in fileList:
            if fnmatch.fnmatch(item,symbolname):
                resultList.append(item)
        
    return resultList

def copyLatestFile(srcFile,tarFile):
    if not os.path.isfile(tarFile):
        return copyFile(srcFile,tarFile)
    elif FileTime(tarFile) < FileTime(srcFile):
        return copyFile(srcFile,tarFile)
    else:
        print "%s is the just latest file."%tarFile
    return 1

def copyFile(srcFile,tarFile):
    if srcFile == tarFile:
        print "WARNNING: copyFile srcFile %s tarFile %s are same."%(srcFile,tarFile)
        return 0
        
    if not os.path.isfile(srcFile):
        print "%s does not exist!"%srcFile
    else:
        tarFilePath,tarFileName = os.path.split(tarFile)
        if not os.path.isdir(tarFilePath):
            print "copyFile create target file path %s."%tarFilePath
            MakeSureDirExists(tarFilePath)

        srcPathAndName = os.path.split(srcFile)
        if os.path.realpath(srcPathAndName[0]) == os.path.realpath(tarFile):
            print "WARNNING: copyFile %s can not be replaced by itself."%srcFile
            return

        # ensure the folder file copyed into existent
        MakeSureDirExists(srcPathAndName[0])

        # shutil.copy(srcFile,tarFile)
        if(os.path.isdir(tarFile)):
            tarFile = os.path.join(tarFile,srcPathAndName[1])

        # if os.path.isfile(tarFile):
        #     print "copyFile delete %s"%tarFile
        #     try:
        #         os.remove(tarFile)
        #     except:
        #         print "copyFile delete Failed."
        #         return 0

        if os.path.isfile(tarFile) and not IsSrcNewFile(srcFile,tarFile):
            print "Ignore the latest file: %s"%tarFile
        else:
            copyFeadBack = "copyFile copy %s %s ... "%(srcFile,tarFile)
            # shutil.copyfile(srcFile,tarFile)
            try:
                shutil.copy2(srcFile,tarFile)
                copyFeadBack += "OK."
            except:
                copyFeadBack += "copyFile copy Failed."
                return 0

            if not (os.path.isfile(tarFile) and IsSrcNewFile(srcFile,tarFile)):
                return 0

            print copyFeadBack

        return 1

    return 0