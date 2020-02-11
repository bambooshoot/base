import maya.api.OpenMaya as om
import pymel.core as mel
import maya.cmds as cmds

def nameToNode( name ):
    selectionList=om.MSelectionList()
    selectionList.add(name)
    depNodeObj = selectionList.getDependNode(0)
    return depNodeObj

def depNodeToTransform( depName ):
    parentNode = cmds.listRelatives(depName,fullPath=True,parent=True)[0]
    return nameToNode(parentNode)

def getMatrixAttrByShape(nodeName,attr):
    obj = depNodeToTransform(nodeName)
    
    transNode = om.MFnTransform(obj)

    matPlug = transNode.findPlug(attr,0)
    mat0Plug = matPlug.elementByLogicalIndex(0)
    matObj = mat0Plug.asMObject()
    fnRootMatrix = om.MFnMatrixData(matObj)
    return fnRootMatrix.matrix()

def getMatrixAttrByNode(nodeName,attr):
    obj = nameToNode(nodeName)
    transNode = om.MFnDependencyNode(obj)
    matPlug = transNode.findPlug(attr,0)
    mat0Plug = matPlug.elementByLogicalIndex(0)
    matObj = mat0Plug.asMObject()
    fnRootMatrix = om.MFnMatrixData(matObj)
    return fnRootMatrix.matrix()

def createFollicleByMeshAndCurves(mesh,curves):
    follicleNodeList=[]
    for curveName in curves:
        follicleNode = createFollicleByMeshAndCurve(mesh,curveName)
        follicleNodeList.append(follicleNode)

    return follicleNodeList

def createFollicleByMeshAndCurve(mesh,curveName):
    fnMesh = om.MFnMesh(nameToNode(mesh))
    obj = nameToNode(curveName)
    fnCurve = om.MFnNurbsCurve(obj)
    curveWorldMatrix = getMatrixAttrByShape(curveName,"worldMatrix")

    param = fnCurve.findParamFromLength(0)
    p0 = fnCurve.getPointAtParam(param)
    p0 *= curveWorldMatrix

    oP = om.MPoint(p0)

    meshInvWorldMatrix = getMatrixAttrByShape(mesh,"worldInverseMatrix")

    oP *= meshInvWorldMatrix
    uvAndFaceId = fnMesh.getUVAtPoint(oP)

    follicleNode = cmds.createNode("follicle")
    cmds.setAttr("%s.parameterU"%follicleNode,uvAndFaceId[0])
    cmds.setAttr("%s.parameterV"%follicleNode,uvAndFaceId[1])
    cmds.setAttr("%s.startDirection"%follicleNode,1)

    cmds.connectAttr("%s.local"%curveName,"%s.startPosition"%follicleNode)
    cmds.connectAttr("%s.outMesh"%mesh,"%s.inputMesh"%follicleNode)
    cmds.connectAttr("%s.worldMatrix[0]"%mesh,"%s.inputWorldMatrix"%follicleNode)

    curveTransNode = cmds.listRelatives(curveName,p=True)[0]
    cmds.connectAttr("%s.worldMatrix[0]"%curveTransNode,"%s.startPositionMatrix"%follicleNode)

    follicleTransNode = cmds.listRelatives(follicleNode,p=True)[0]
    cmds.connectAttr("%s.outRotate"%follicleNode,"%s.rotate"%follicleTransNode)
    cmds.connectAttr("%s.outTranslate"%follicleNode,"%s.translate"%follicleTransNode)
    return follicleNode