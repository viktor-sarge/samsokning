'''
Created on 16 jan 2014

@author: PC
'''
"""
Perform search. 

"""
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

def _plusifyQuery(query):
    return re.sub('\s+', '+', query)

def performSearch(query, HTMLmachine):
    """Search, sort data and print result
    
    Arguments
    query -- search query
    HTMLmachine -- html writer
    
    """
    connector = connectorclass()
    storage = []
    
    HTMLmachine.outputHitCountHeader(query)

    searchjobs = getSearchjobs(_plusifyQuery(query))

    for searchjob in searchjobs:
        page = connector.getpage(searchjob.searchurl)
        hitnumbers = searchjob.parser.parse(page, searchjob.location, storage, searchjob.baseurl, searchjob.searchurl)
        HTMLmachine.outputResultsnumbers(hitnumbers, searchjob.location)

    storage = sorted(storage, cmp = lambda a, b : a.getFirst(b))
    HTMLmachine.output2dList(storage,"list")
