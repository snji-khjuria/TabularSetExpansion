supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productSpecs"
patternsOutputLocation        = "specsPatterns.tsv"

from FileUtil import getWebsiteLocations
from FileUtil import getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileContentInList
from ClusterExtractionUtil import learnPatterns
from utils import writeTripletPatternsAsCsv
from ClusterContextExtraction import getClusterContexts
from utils import appendPreprocessType, processNumInContext
websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)
for websiteLocation in websiteLocations:
    pages                = getAllPagesInsideWebsite(websiteLocation)
    contexts             = []
    for page in pages:
        exactPageLocation = page + "/page.html"
        clusterElements   = readFileContentInList(page + "/" + supervisedFileName)
        pageContent = readPlainHtmlPageContent(exactPageLocation)
        contextsPerPage = getClusterContexts(pageContent, clusterElements)
        contexts.append(contextsPerPage)
    patterns = learnPatterns(contexts)
    patterns = appendPreprocessType(patterns, "None")

    numProcessedContexts = processNumInContext(contexts)
    numProcessedPatterns = learnPatterns(numProcessedContexts)
    numProcessedPatterns = appendPreprocessType(numProcessedPatterns, "NUM")

    print("Contexts are:- ")
    print(contexts)
    print("Patterns are:- ")
    print(patterns)
    patterns.extend(numProcessedPatterns)
    writeTripletPatternsAsCsv(websiteLocation + "/" + patternsOutputLocation, patterns)
    print("Patterns written at location:- " + websiteLocation + "/" + patternsOutputLocation)