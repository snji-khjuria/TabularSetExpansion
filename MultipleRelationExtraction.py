#global variables section
supervisedDataLocation        = "./supervisedData"
supervisedFileName            = "productTables"
patternsOutputLocation        = "tablePatterns.tsv"
KEY_VALUE_AWAY_LIMIT          = 100


#essential imports
from utils    import writeTripletPatternsAsCsv, getAllContextsForKV
from FileUtil import getWebsiteLocations, getAllPagesInsideWebsite, readPlainHtmlPageContent
from FileUtil import readFileRelationContentInList
from RelationPatternsLearningUtil import learnPatterns

#get all the locations for website so that we can start extracting the patterns for them.
websiteLocations = getWebsiteLocations(supervisedDataLocation)
print(websiteLocations)


#work for each website independently
for websiteLocation in websiteLocations:
    pages                    = getAllPagesInsideWebsite(websiteLocation)
    corpusLevelRelationContext = []
    for page in pages:
        exactPageLocation = page + "/page.html"
        print("Exact page location:- ")
        print(exactPageLocation)
        #also can be called as supervision of relations
        supervisedRelationList        = readFileRelationContentInList(page+"/"+supervisedFileName)
        allRelationContextsPerPage    = []
        pageContent = readPlainHtmlPageContent(exactPageLocation)
        for supervisedRelation in supervisedRelationList:
            (key, value)        = supervisedRelation
            contextsPerRelation = getAllContextsForKV(pageContent, key, value, KEY_VALUE_AWAY_LIMIT)
            allRelationContextsPerPage.append(contextsPerRelation)
        corpusLevelRelationContext.extend(allRelationContextsPerPage)
    print("Multiple relation contexts are:- ")
    print("This is design choice to keep tables from all the pages belong to big table set")
    print("At this stage we have all the relation contexts present...")
    print("Relation contexts are list of lists per tuple....")
    #[[(left, middle, right)], [(l, m, r), (l, m, r)]]
    print(corpusLevelRelationContext)
    print("We are gonna learn patterns for this set of contexts...")
    patterns = learnPatterns(corpusLevelRelationContext)
    print("Patterns learnt are:- ")
    print(patterns)
    print("We are gonna write patterns to file now...")
    writeTripletPatternsAsCsv(websiteLocation + "/" + patternsOutputLocation, patterns)
    print("Patterns written at location:- " + websiteLocation + "/" + patternsOutputLocation)
