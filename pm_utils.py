import maya.cmds as MC
import maya.api.OpenMaya as om
import time


def findCenter(selList):
    ''' Returns the center position of currently selected object or sub-objects
	Arguments:
		selList -- list containing names of the objects or sub-objects

	Returns:
		center -- type(float) center position of the selection

    '''
    center = [0,0,0]
    length = len(selList)
    for i in selList:
        pos = MC.xform(i, q=True, ws=True, translation=True)
        center[0] += pos[0]
        center[1] += pos[1]
        center[2] += pos[2]
    center = [center[0]/length, center[1]/length, center[2]/length]
    return center



def match_points_position(objList, worldSpace=False):
    ''' This function takes two objects and moves the vertices of
    the second object to match the shape of the first object
    
    Arguments:
        objList -- list containing names of the object to perform
                    the operation on. Order of selection matters.
                    First object will be the source and second will
                    be the target.
        worldSpace -- If True then the vertices of the target object
                    will overlap on the vertices of the first object in worldspace.
                    If False then the vertices will move in local space to match 
                    the shape of the source object.
                    
    Returns -- None
    
    '''
    if len(objList) != 2 :
        MC.error('Requires exactly two objects. Stopping execution')
    selList = om.MSelectionList()
    selList.add(objList[0])
    selList.add(objList[1])
    mDagPath_source = selList.getDagPath(0)
    mDagPath_target = selList.getDagPath(1)
    space = om.MSpace.kWorld if worldSpace else om.MSpace.kObject
    
    meshFn = om.MFnMesh( mDagPath_source )
    ppos = om.MPointArray()
    ppos = meshFn.getPoints( space=space)
    meshFn2 = om.MFnMesh( mDagPath_target)
    meshFn2.setPoints(ppos, space=space)