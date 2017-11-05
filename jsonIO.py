import os,json

def LoadJson(jsonFile):
    if not os.path.isfile(jsonFile):
        return
        
    fileP=open(jsonFile,'r')
    data=json.load(fileP)
    fileP.close()
    return data
    
def DumpJson(jsonFile,data):
    fileP=open(jsonFile,'w')
    json.dump(data,fileP)
    fileP.close()