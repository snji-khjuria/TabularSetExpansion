supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productSpecs"
patternsOutputLocation        = "specsPatterns.tsv"

from FileUtil import getWebsiteLocations
from FileUtil import getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileContentInList
from ClusterExtractionUtil import learnPatterns
from utils import writeTripletPatternsAsCsv
from ClusterContextExtraction import getClusterContexts

websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)
for websiteLocation in websiteLocations:
    pages                = getAllPagesInsideWebsite(websiteLocation)
    contexts             = []
    for page in pages:
        exactPageLocation = page + "/page.html"
        clusterElements   = readFileContentInList(page + "/" + supervisedFileName)
        print("Specifications are:- ")
        print(clusterElements)
        pageContent = readPlainHtmlPageContent(exactPageLocation)
        contextsPerPage = getClusterContexts(pageContent, clusterElements)
        contexts.append(contextsPerPage)
    patterns = learnPatterns(contexts)
    print("Contexts are:- ")
    print(contexts)
    print("Patterns are:- ")
    print(patterns)
    writeTripletPatternsAsCsv(websiteLocation + "/" + patternsOutputLocation, patterns)
    print("Patterns written at location:- " + websiteLocation + "/" + patternsOutputLocation)