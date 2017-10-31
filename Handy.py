import os,fnmatch,re

def ListFile(path,symbolname):
    fileList=os.listdir(path)
    resultList=[]
    for item in fileList:
        if fnmatch.fnmatch(item,symbolname):
            resultList.append(item)
    return resultList

def PadNum(n,padNum):
    numStr='%(num)0'+padNum+'d'
    numStr=numStr % {'num':int(n,10)}
    return numStr

def GetStrNumPadList(strList):
    numRe=re.compile('[0-9]+')
    numList=[]
    for curStr in strList:
        curNum=numRe.findall(curStr)
        numList.append(int(curNum[-1],10))
    return numList

def ReplaceStrListNumPad(strList,padNum):
    numRe=re.compile('[0-9]+')
    newList=[]
    for curStr in strList:
        curNum=numRe.findall(curStr)
        newNum=PadNum(curNum[-1],padNum)
        numPadPos=curStr.rfind(curNum[-1])
        newList.append(curStr[:numPadPos]+curStr[numPadPos:].replace(curNum[-1],newNum,1))
    return newList

def TakeOutStrSeq(strList,startNum,gapStep,endNum):
    startFrame=startNum
    endFrame=endNum

    fileNameList=strList
    numList=GetStrNumPadList(fileNameList)
    fileNum=len(fileNameList)
    numAndFileDict={}
    for i in range(0,fileNum,1):
        numAndFileDict[numList[i]]=fileNameList[i]

    resultStrList=[]
    for i in range(startFrame,endFrame,gapStep):
        if numAndFileDict.has_key(i):
            resultStrList.append(numAndFileDict[i])
    return resultStrList
