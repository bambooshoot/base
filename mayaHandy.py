import maya.cmds as cmds
import pymel.core as pm

def BatchNodeOpByTypeAndAttrName(method):
    def func(*argv):
        nodeTypeStr=argv[0]
        selList=cmds.ls(type=nodeTypeStr)
        for curSel in selList:
            argList=list(argv[:-1])
            argList.append(curSel)
            method(*argList)
    
    return func


@BatchNodeOpByTypeAndAttrName
def BatchSetAttrFloat(nodeTypeStr,attrName,value,curSel):
    cmds.setAttr("%s.%s"%(curSel,attrName),value)

@BatchNodeOpByTypeAndAttrName
def BatchConnectAttr(nodeTypeStr,attrName,outputNodeAttr,curSel):
    inputNodeAttr = "%s.%s"%(curSel,attrName)
    connList=cmds.listConnections(inputNodeAttr,s=1,d=0);
    if not connList:
        cmds.connectAttr(outputNodeAttr,inputNodeAttr)

def getImageName():
    return cmds.getAttr('defaultRenderGlobals.imageFilePrefix')

def getImagePath():
    return cmds.workspace(q=True,fullName=True)

#
def getRenderer():
    return cmds.getAttr('defaultRenderGlobals.currentRenderer')

#
def getImageWidth():
    return int(cmds.getAttr('defaultResolution.width'))

#
def getImageHeight():
    return int(cmds.getAttr('defaultResolution.height'))

#
def getStartFrame():
    return int(cmds.getAttr('defaultRenderGlobals.startFrame'))

#
def getEndFrame():
    return int(cmds.getAttr('defaultRenderGlobals.endFrame'))

def AvaliableIndexToConnect(arrayAttr):
    attr=pm.Attribute(arrayAttr)
    conIdxList = attr.getArrayIndices()
    if len(conIdxList) > 0:
        return conIdxList[-1]+1;
    return 0

# Get Render Data
def getRenderData():
    # Dict { <Render Attribute>:
    #        <Value>}
    dic = collections.OrderedDict()
    dic['renderer'] = _get.getNiceName(cmds.getAttr('defaultRenderGlobals.currentRenderer'))
    # Arnold
    if cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold':
        getMtoa()
        dic['aa'] = cmds.getAttr('defaultArnoldRenderOptions.AASamples')
        dic['diffuse'] = cmds.getAttr('defaultArnoldRenderOptions.GIDiffuseSamples')
        dic['glossy'] = cmds.getAttr('defaultArnoldRenderOptions.GIGlossySamples')
        dic['refraction'] = cmds.getAttr('defaultArnoldRenderOptions.GIRefractionSamples')
        dic['sss'] = cmds.getAttr('defaultArnoldRenderOptions.GISssSamples')
        motionBlur = 'OFF'
        motionStep = none
        motionTypeDic = {0: 'Start On Frame', 1: 'Center On Frame', 2: 'End On Frame', 3: 'Custom'}
        motionType = none
        motionFrame = none
        if cmds.getAttr('defaultArnoldRenderOptions.motion_blur_enable'):
            motionBlur = 'ON'
            motionStep = cmds.getAttr('defaultArnoldRenderOptions.motion_steps')
            motionType = motionTypeDic[cmds.getAttr('defaultArnoldRenderOptions.range_type')]
            motionFrame = '%.3f' % cmds.getAttr('defaultArnoldRenderOptions.motion_frames')
        dic['motionBlur'] = motionBlur
        if motionStep:
            dic['motionStep'] = motionStep
        if motionType:
            dic['motionType'] = motionType
        if motionFrame:
            dic['motionFrame'] = motionFrame
        dic['totalDepth'] = cmds.getAttr('defaultArnoldRenderOptions.GITotalDepth')
        dic['diffuseDepth'] = cmds.getAttr('defaultArnoldRenderOptions.GIDiffuseDepth')
        dic['glossyDepth'] = cmds.getAttr('defaultArnoldRenderOptions.GIGlossyDepth')
        dic['reflectionDepth'] = cmds.getAttr('defaultArnoldRenderOptions.GIReflectionDepth')
        dic['refractionDepth'] = cmds.getAttr('defaultArnoldRenderOptions.GIRefractionDepth')
        dic['displayMode'] = _lgtConfig.displayModeConfig()[getDisplayMode()]
        dic['lightGamma'] = '%.3f' % cmds.getAttr('defaultArnoldRenderOptions.light_gamma')
        dic['shaderGamma'] = '%.3f' % cmds.getAttr('defaultArnoldRenderOptions.shader_gamma')
        dic['textureGamma'] = '%.3f' % cmds.getAttr('defaultArnoldRenderOptions.texture_gamma')
    return dic

def GetRenderSetting():
    MaRenderOptionDic = {
        'renderer': cmds.getAttr('defaultRenderGlobals.currentRenderer'),
        'imagePrefix': cmds.getAttr('defaultRenderGlobals.imageFilePrefix'),
        'startFrame': cmds.getAttr('defaultRenderGlobals.startFrame'),
        'endFrame': cmds.getAttr('defaultRenderGlobals.endFrame'),
        'animation': cmds.getAttr('defaultRenderGlobals.animation'),
        'imageFormat': cmds.getAttr('defaultRenderGlobals.imfPluginKey'),
        'periodInExt': cmds.getAttr('defaultRenderGlobals.periodInExt'),
        'putFrameBeforeExt': cmds.getAttr('defaultRenderGlobals.putFrameBeforeExt'),
        'extensionPadding': cmds.getAttr('defaultRenderGlobals.extensionPadding'),
        'renderVersion': cmds.getAttr('defaultRenderGlobals.renderVersion'),
        #
        'imageWidth': cmds.getAttr('defaultResolution.width'),
        'imageHeight': cmds.getAttr('defaultResolution.height')
    }
    return MaRenderOptionDic
    
# BatchConnectAttr("nurbsHairOp_InGuideCurves","currentTime","time1.outTime","")