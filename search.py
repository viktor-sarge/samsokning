# -*- coding: utf-8 -*-

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
import socket
from multiprocessing import Pool
import urllib2
import urllib
import time
import config
from sourceselector import sourceselector

class connectorclass: 
    'Knows how to fetch the different library opacs'
    
    def getpage(self, url):
        page = urllib2.urlopen(url, timeout = config.parser.getfloat(config.defaultSection, 'connectorTimeoutSeconds'))
        content = page.read()
        page.close()
        
        file = open('searchpage.htm', 'w')
        file.write(content)
        file.close()
        
        return content 

def _plusifyQuery(query):
    return urllib.quote(query)

def _executeSearchJob(searchjob):
    startTime = time.time()

    connector = connectorclass()
    storage = []

    hitnumbers = None
    totalhits = None
    try:
        page = connector.getpage(searchjob.searchurl)
        (hitnumbers, totalhits) = searchjob.parser.parse(page, searchjob.location, storage, searchjob.baseurl, searchjob.searchurl)
    except:
        pass

    return (searchjob.location, hitnumbers, totalhits, storage, time.time() - startTime, searchjob.getSearchurl())

def performSearch(query, HTMLmachine):
    """Search, sort data and print result
    
    Arguments
    query -- search query
    HTMLmachine -- html writer
    
    """
    HTMLmachine.outputHitCountHeader(query)

    searchjobs = [job for job in getSearchjobs(_plusifyQuery(query)) if sourceselector.isSourceSelected(job.location)]

    storage = []

    p = Pool(len(searchjobs))
    results = p.map(_executeSearchJob, searchjobs)

    for result in results:
        if (result[1]):
            HTMLmachine.outputResultsnumbers(result[1], result[2], result[0], result[5], result[4])
            storage.extend(result[3])
        else:
            HTMLmachine.outputError(result[0])


    storage = sorted(storage, cmp = lambda a, b : a.getFirst(b))
    HTMLmachine.output2dList(storage,"list")
