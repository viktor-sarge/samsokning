# coding=utf-8
'''
Created on 17 jan 2014

@author: PC
'''

import re
from opacparser import LibraParser, ArenaParser, MikromarcParser

QueryRegex = '@QUERY@'

class SearchJob:
    def __init__(self, parser, baseurl, searchurl, location, query):
        self.parser = parser
        self.baseurl = baseurl
        self.location = location

        if(searchurl.find(QueryRegex) >= 0):
            self.searchurl = re.sub(QueryRegex, query, searchurl)
        else:
            self.searchurl = searchurl + query

def getAssortment(query):
    result = []
    result.append(SearchJob(MikromarcParser(), 'http://webbsok.mikromarc.se/Mikromarc3/web/', 
                           'http://webbsok.mikromarc.se/Mikromarc3/web/search.aspx?Unit=6471&db=bollebygd-fb&SC=FT&SW=@QUERY@&LB=FT&IN=&SU=19116&', 
                           'Bollebygd', query))

    result.append(SearchJob(ArenaParser(), '', 
                           'http://bibliotek.mark.se/web/arena/search?p_p_state=normal&p_p_lifecycle=1&p_p_action=1&p_p_id=searchResult_WAR_arenaportlets&p_p_col_count=4&p_p_col_id=column-1&p_p_col_pos=1&p_p_mode=view&search_item_no=0&search_type=solr&search_query=', 
                           'Mark', query))
    
    result.append(SearchJob(LibraParser(), 'http://opac.laholm.axiell.com/opac/', 
                           'http://opac.laholm.axiell.com/opac/search_result.aspx?TextFritext=', 
                           'Laholm', query))

    return result

def getBollebygd(query):
    result = []
    result.append(SearchJob(MikromarcParser(), 'http://webbsok.mikromarc.se/Mikromarc3/web/', 
                           'http://webbsok.mikromarc.se/Mikromarc3/web/search.aspx?Unit=6471&db=bollebygd-fb&SC=FT&SW=@QUERY@&LB=FT&IN=&SU=19116&', 
                           'Bollebygd', query))

    return result

def getMark(query):
    result = []
    result.append(SearchJob(ArenaParser(), '', 
                           'http://bibliotek.mark.se/web/arena/search?p_p_state=normal&p_p_lifecycle=1&p_p_action=1&p_p_id=searchResult_WAR_arenaportlets&p_p_col_count=4&p_p_col_id=column-1&p_p_col_pos=1&p_p_mode=view&search_item_no=0&search_type=solr&search_query=', 
                           'Mark', query))

    return result

def getMikromarc(query):
    result = []
    mmp = MikromarcParser()
    result.append(SearchJob(mmp, 'http://webbsok.mikromarc.se/Mikromarc3/web/', 
                           'http://webbsok.mikromarc.se/Mikromarc3/web/search.aspx?Unit=6471&db=bollebygd-fb&SC=FT&SW=@QUERY@&LB=FT&IN=&SU=19116&', 
                           'Bollebygd', query))

    result.append(SearchJob(mmp, 'http://webbsok.mikromarc.se/Mikromarc3/web/', 
                           'http://webbsok.mikromarc.se/Mikromarc3/Web/search.aspx?Unit=6469&db=vargarda&SC=FT&SW=@QUERY@&LB=FT&IN=&SU=0&', 
                           'Vårgårda', query))

    return result

def getArena(query):
    result = []
    ap = ArenaParser()
    result.append(SearchJob(ap, '', 
                           'http://bibliotek.mark.se/web/arena/search?p_p_state=normal&p_p_lifecycle=1&p_p_action=1&p_p_id=searchResult_WAR_arenaportlets&p_p_col_count=4&p_p_col_id=column-1&p_p_col_pos=1&p_p_mode=view&search_item_no=0&search_type=solr&search_query=', 
                           'Mark', query))

    result.append(SearchJob(ap, '', 
                           'http://www.falkopingsbibliotek.se/web/arena/search?p_p_state=normal&p_p_lifecycle=1&p_p_action=1&p_p_id=searchResult_WAR_arenaportlets&p_p_col_count=4&p_p_col_id=column-1&p_p_mode=view&facet_queries=&search_item_no=0&search_type=solr&search_query=', 
                           'Falköping', query))

    result.append(SearchJob(ap, '', 
                           'http://biblioteken.vara.se/web/pub/search?p_p_state=normal&p_p_lifecycle=1&p_p_action=1&p_p_id=searchResult_WAR_arenaportlets&p_p_col_count=3&p_p_col_id=column-1&p_p_col_pos=1&p_p_mode=view&facet_queries=&search_item_no=0&search_type=solr&search_query=', 
                           'Vara', query))

    return result

def getLibra(query):
    result = []
    lp = LibraParser()
    result.append(SearchJob(lp, 'http://opac.laholm.axiell.com/opac/', 
                           'http://opac.laholm.axiell.com/opac/search_result.aspx?TextFritext=', 
                           'Laholm', query))

    result.append(SearchJob(lp, 'http://halmstadopac.kultur.halmstad.se/opac/', 
                           'http://halmstadopac.kultur.halmstad.se/opac/search_result.aspx?TextFritext=', 
                           'Halmstad', query))

    result.append(SearchJob(lp, 'http://www5.falkenberg.se/opac/opac/', 
                           'http://www5.falkenberg.se/opac/opac/search_result.aspx?TextFritext=', 
                           'Falkenberg', query))

    result.append(SearchJob(lp, 'http://bibold.kungsbacka.se/opac/', 
                           'http://bibold.kungsbacka.se/opac/search_result.aspx?TextFritext=', 
                           'Kungsbacka', query))

    result.append(SearchJob(lp, 'http://bib.varberg.se/opac/', 
                           'http://bib.varberg.se/opac/search_result.aspx?TextFritext=', 
                           'Varberg', query))

    return result

def getAll(query):
    return getLibra(query) + getMikromarc(query) + getArena(query)

def getSearchjobs(query):
    return getAll(query)
#    return getAssortment(query)
#    return getMark(query)
