#do pattern filtering
from FileUtil import getAllPagesInsideWebsite, readFileContentInList
from FileUtil import readPlainHtmlPageContent


#find entity set in left and right pattern.
def makeSingleObjectExtractions(pageContent, leftPattern, rightPattern):
    searchIndex = 0
    output = []
    while True:
        try:
            startL = pageContent.index(leftPattern, searchIndex)
            endL   = startL+len(leftPattern)
            end    = pageContent.index(rightPattern, endL)
            if end-endL<=1000:
                output.append(pageContent[endL:end])
            searchIndex = startL+1
        except ValueError:
            return list(set(output))
    return list(set(output))

def singleObjectPatternFiltering(patterns, websiteLocation, supervisedFileLocation):
    output = []
    for pattern in patterns:
        (lp, rp) = pattern
        pages = getAllPagesInsideWebsite(websiteLocation)
        patternScore = 0
        for page in pages:
            exactPageLocation = page + "/page.html"
            contentList = readFileContentInList(page + "/" + supervisedFileLocation)
            singleObj = ""
            if len(contentList) == 1:
                singleObj = contentList[0]
            goldContent = " ".join(singleObj.split())
            pageContent = readPlainHtmlPageContent(exactPageLocation)
            results     = makeSingleObjectExtractions(pageContent, lp, rp)
            if goldContent in results:
                patternScore+=1
        if patternScore > 0:
            output.append((lp, rp))
    return output