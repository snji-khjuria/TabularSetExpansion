import os.path
CONTEXT_LIMIT                 = 100

def getLeftIndex(l):
    return max(0, l)

def getRightIndex(r, limit):
    return min(r, limit)

#reverse all strings present in list
def revStrInList(l):
    output = []
    for item in l:
        output.append(item[::-1])
    return output

def getCommonPrefix(s1, s2):
    l = [s1, s2]
    return os.path.commonprefix(l)


import csv
def writeTripletPatternsAsCsv(outputLocation, patterns):
    l = []
    l.append(["LeftPattern", "MiddlePattern", "RightPattern"])
    for pattern in patterns:
        (lp, mp, rp) = pattern
        l.append([lp, mp, rp])
    with open(outputLocation, "w") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(l)


def separateLeftMiddleRightContexts(multipleRelationContexts):
    lcs = []
    mcs = []
    rcs = []
    for context in multipleRelationContexts:
        lc = []
        mc = []
        rc = []
        for (a, b, c) in context:
            lc.append(a)
            mc.append(b)
            rc.append(c)
        lcs.append(lc)
        mcs.append(mc)
        rcs.append(rc)
    return (lcs, mcs, rcs)


#get all contexts for key value pair
def getAllContextsForKV(pageContent, key, value, KEY_VALUE_AWAY_LIMIT=100):
    contexts = []
    rightContextRangeLimit = len(pageContent)-1
    leftKeyLength          = len(key)
    rightKeyLength         = len(value)
    searchLocation         = 0
    while(True):
        leftLoc = pageContent.find(key, searchLocation)
        if leftLoc == -1:
            break
        leftContext     = pageContent[getLeftIndex(leftLoc-CONTEXT_LIMIT):leftLoc].strip()
        searchLocation  = leftLoc+1
        rightLocStart   = leftLoc + leftKeyLength
        rightLoc        = pageContent.find(value, rightLocStart)
        if rightLoc==-1:
            break
        rightLocEnd = rightLoc + rightKeyLength
        rightContext = pageContent[rightLocEnd:getRightIndex(rightLocEnd + CONTEXT_LIMIT, rightContextRangeLimit)].strip()
        middleContext = pageContent[rightLocStart:rightLoc].strip()
        if len(middleContext)<=KEY_VALUE_AWAY_LIMIT:
            contexts.append((leftContext, middleContext, rightContext))
    return contexts