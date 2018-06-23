FULL_PATTERN_LENGTH_THRESHOLD = 10

from utils import segmentPairContexts

from GeneralPatternExtractionUtil import compressLeftContexts, compressRightContexts

def learnPatterns(contexts):
    (lc, rc) = segmentPairContexts(contexts)
    print("Right contexts are:- " + str(rc))
    summarizedLeftContexts   = compressLeftContexts(lc)
    summarizedRightContexts  = compressRightContexts(rc)
    output = []
    for left in summarizedLeftContexts:
        for right in summarizedRightContexts:
            if len(left)+len(right)>FULL_PATTERN_LENGTH_THRESHOLD:
                output.append((left, right))
    return list(set(output))