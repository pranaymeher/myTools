import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds

context = 'centerHandler'
def onPress():
    vpX, vpY, _ = cmds.draggerContext(context, query=True, dragPoint=True)
    pos = om.MPoint()
    dir = om.MVector()
    omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
    for mesh in cmds.ls(type='mesh'):
        selectionList = om.MSelectionList()
        selectionList.add(mesh)
        dagPath = selectionList.getDagPath(0)
        fnMesh = om.MFnMesh(dagPath)
        hit = fnMesh.allIntersections(
            om.MFloatPoint(pos),
            om.MFloatVector(dir),
            om.MSpace.kWorld, 99999, False)
        if hit:
            try:
                hit1 = hit[0][0]
                hit2 = hit[0][1]
                mySel = cmds.ls(sl=True)[-1]
                pos = [(hit1[0]+hit2[0])/2, (hit1[1]+hit2[1])/2, (hit1[2]+hit2[2])/2]
                cmds.setAttr(mySel+'.translate', pos[0], pos[1], pos[2], type='double3')
            except:
                pass
            
       
if cmds.draggerContext(context, exists=True):
    cmds.deleteUI(context)
cmds.draggerContext(context, dragCommand=onPress, name=context, cursor='crossHair', ds="Yeah Drag Me")
cmds.setToolTo(context)