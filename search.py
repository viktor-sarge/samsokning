'''
Created on 16 jan 2014

@author: PC
'''
import re
from html import HTMLwriter
from sources import getSearchjobs


class connectorclass: 
    'Knows how to fetch the different library opacs'
    
    def __init__(self):
        import urllib
        
    def getpage(self, url):
        import urllib
        page = urllib.urlopen(url)
        content = page.read()
        page.close()
        
        file = open('searchpage.htm', 'w')
        file.write(content)
        file.close()
        
        return content 
    
class metadataSortmachine: 
    
    def groupByTitle(self,list):
        for row in list: 
            title = row.pop(2)
            row.insert(0,title)
        list = sorted(list)
        return list

def _plusifyQuery(query):
    return re.sub('\s+', '+', query)

def performSearch(query, HTMLmachine):
    connector = connectorclass()
    storage = []
    
    HTMLmachine.outputHitCountHeader(query)

    searchjobs = getSearchjobs(_plusifyQuery(query))

    for searchjob in searchjobs:
        page = connector.getpage(searchjob.searchurl)
        hitnumbers = searchjob.parser.parse(page, searchjob.location, storage, searchjob.baseurl)
        HTMLmachine.outputResultsnumbers(hitnumbers, searchjob.location)

#    sorter = metadataSortmachine()
#    storage = sorter.groupByTitle(storage)
    storage = sorted(storage, cmp = lambda a, b : a.getFirst(b))
#    sorted(storage, key = lambda item : item.title)
    HTMLmachine.output2dList(storage,"list")
