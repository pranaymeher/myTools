def findCenter(selList):
    ''' Returns the center position of currently selected object'''
    center = [0,0,0]
    length = len(selList)
    for i in selList:
        pos = MC.xform(i, q=True, ws=True, translation=True)
        center[0] += pos[0]
        center[1] += pos[1]
        center[2] += pos[2]
    center = [center[0]/length, center[1]/length, center[2]/length]
    return center


