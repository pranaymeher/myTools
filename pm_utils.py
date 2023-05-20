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
    the second object to match the shape of the first object.
    This methos id 320 times faster than using normal maya.cmds script
    
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



def project_mesh(objList):
    '''
    This function projects the target mesh onto the source mesh
    objList[0] = sourcemesh
    objList[1] = targetmesh

    Arguments:
        objList -- [string] list containing exactly two names of meshes

    Returns:
        None
    '''
    
    if len(objList) != 2:
        MC.error('The objList needs to have exactly two objects')
    else:
        selList = om.MSelectionList()
        selList.add(objList[0])
        selList.add(objList[1])

        target_dpath = selList.getDagPath(1)
        geoIter = om.MItGeometry(target_dpath)
        
        source_dpath = selList.getDagPath(0)
        mfnMesh_source = om.MFnMesh(source_dpath)
        
        pointArray = om.MPointArray()

        while not geoIter.isDone():
            pos = (geoIter.position())
            c_pos,_ = mfnMesh_source.getClosestPoint(pos, om.MSpace.kWorld)
            pointArray.append( [ c_pos[0], c_pos[1], c_pos[2] ])

            geoIter.next()
        
        mfnMesh_target = om.MFnMesh(target_dpath)
        mfnMesh_target.setPoints( pointArray, om.MSpace.kWorld )
        
        
        
def align_to_vector( in_object, primary_axis, up_axis, up_vec ):
    '''
        This function orients the in_object such that the up_axis
        aligns with the up_vec while the primary axis maintains its direction
        
        Arguments:
            in_object -- string - The object to be aligned
            primary_axis -- string - The values can only be x, y or z. The primary
                            axis will maintain its direction after the alignment
            up_axis -- string - The values can only be x, y or z. The up_axis will
                                orient itself to match as closely as possible to the
                                provided up_vec
            up_vec -- vector - The up axis will align itself to match with this vector
            
        Returns:
            float_seg -- [float_list] - This is a float list of 16 values. Can be used as
                                a vector in the xform command
                                
        Example :
            align_to_vector( 'locator1', 'z', 'y', [0, 0, -1])
    '''
    
    primary_axis = primary_axis.lower()
    up_axis = up_axis.lower()
    assert primary_axis in 'xyz', 'Primary axis value can not be other than x,y or z'
    assert up_axis in 'xyz', 'Up axis value can not be other than x,y or z'
    
    in_obj_pos = MC.xform( in_object, q=True, ws=True, translation=True)
    
    vec_dict = {    'x' : [1, 0, 0],
                    'y' : [0, 1, 0],
                    'z' : [0, 0, 1]
            }
            
    vec_pair = f'{primary_axis}{up_axis}'
    flip_vec_pair = [ 'xz', 'yx', 'zy' ]
    
    obj_mat = om.MMatrix( MC.xform( in_object, q=True, ws=True, matrix=True ) )
    prim_vec = om.MVector( vec_dict[ primary_axis ] ) * obj_mat
    
    sec_vec_temp = om.MVector( up_vec )
    
    if vec_pair in flip_vec_pair:
        third_vec = sec_vec_temp ^ prim_vec
    else:
        third_vec = prim_vec ^ sec_vec_temp
    third_vec.normalize()
    
    if vec_pair in flip_vec_pair:
        sec_vec = prim_vec ^ third_vec 
    else:
        sec_vec = third_vec ^ prim_vec
    sec_vec.normalize()
    
    match vec_pair:
        case 'zy':
            float_seq = [ *third_vec, 0, *sec_vec, 0, *prim_vec, 0, *in_obj_pos, 1]
        case 'zx':
            float_seq = [ *sec_vec, 0, *third_vec, 0, *prim_vec, 0, *in_obj_pos, 1]
        case 'xy':
            float_seq = [ *prim_vec, 0, *sec_vec, 0, *third_vec, 0, *in_obj_pos, 1]
        case 'xz':
            float_seq = [ *prim_vec, 0, *third_vec, 0, *sec_vec, 0, *in_obj_pos, 1]
        case 'yx':
            float_seq = [ *sec_vec, 0, *prim_vec, 0, *third_vec, 0, *in_obj_pos, 1]
        case 'yz':
            float_seq = [ *third_vec, 0, *prim_vec, 0, *sec_vec, 0, *in_obj_pos, 1]
    
    return float_seq
