import maya.cmds as mc
import maya.mel as mm

def Swing_MenuItem_Exists(label):
    if mc.menu('swingKits',q=True,numberOfItems=True) > 0:
        for curItem in mc.menu('swingKits',q=True,itemArray=True):
            if mc.menuItem(curItem,q=True,label=True) == label:
                return True
    return False

def Swing_CreateUI(labelList=[],commandList=[]):
    gMainWindow = mm.eval('$tmpVar=$gMainWindow')
    mc.setParent(gMainWindow)
    if mc.menu('swingKits',q=True,exists=True)==1:
        mc.setParent('swingKits',menu=True)
    else:
        mc.menu('swingKits',label="swingKits",tearOff=True,allowOptionBoxes=True)
        
    
    if True in [Swing_MenuItem_Exists(curLabel) for curLabel in labelList]:
        return

    mc.menuItem(divider=True)
    sizeOfLabelList=len(labelList)
    i=0
    for i in range(0,sizeOfLabelList,1):
        mc.menuItem(label=labelList[i],command=commandList[i])

def Swing_DeleteUI():
    mc.deleteUI('swingKits')