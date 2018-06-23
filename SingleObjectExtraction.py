supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productTitle"
patternsOutputLocation        = "titlePatterns.tsv"
from utils import getLeftIndex, getRightIndex, revStrInList
from utils import segmentPairContexts

def getPatternScore(output, gold):
    # scoreAssigned = 100
    oSet = set(output)
    gSet = set(gold)
    cSet = oSet & gSet
    cSetSize = len(cSet)
    if cSetSize==0:
        return -100
    scoreAssigned = cSetSize*10
    return scoreAssigned





from PatternsFilteringModule import singleObjectPatternFiltering
from FileUtil import getWebsiteLocations
from FileUtil import getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileContentInList
from utils import getSingleObjectContexts, writePairPatternsAsCsv
from SingleObjectPatternsLearningUtil import  learnPatterns
websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)
for websiteLocation in websiteLocations:
    pages                = getAllPagesInsideWebsite(websiteLocation)
    singleObjectContexts = []
    singleObjList        = []
    for page in pages:
        exactPageLocation = page + "/page.html"
        contentList       = readFileContentInList(page + "/" + supervisedFileName)
        singleObj         = ""
        if len(contentList)==1:
            singleObj = contentList[0]
        #so that multiple spaces in product title are being removed
        singleObj       = " ".join(singleObj.split())
        pageContent     = readPlainHtmlPageContent(exactPageLocation)
        contextsPerPage = getSingleObjectContexts(pageContent, singleObj)
        if len(contextsPerPage)>0:
            singleObjectContexts.append(contextsPerPage)
        singleObjList.append(singleObj)
    print("You know what...")
    print("Single object contexts are:- ")
    print(singleObjectContexts)
    patterns         = learnPatterns(singleObjectContexts)
    print("Finally we have learnt the patterns...")
    filteredPatterns = singleObjectPatternFiltering(patterns, websiteLocation, supervisedFileName)
    print("Patterns are:- ")
    print(patterns)
    print("FilteredPatterns are:- ")
    print(filteredPatterns)
    # filteredPatterns = patterns
    writePairPatternsAsCsv(websiteLocation+"/" + patternsOutputLocation, filteredPatterns)
    print("Patterns written at:- " + websiteLocation + "/" + patternsOutputLocation)

