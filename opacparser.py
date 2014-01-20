# coding=utf-8
'''
Created on 16 jan 2014

@author: PC
'''

import re

def strip_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    return cleantext

class MediaItem:
    def __init__(self, title, location, author, type, year, url):
        self.title = title
        self.location = location
        self.author = author
        self.type = type
        self.year = year
        self.url = url

    def getLibrisQuery(self):
        libris_query = ""
        continued_string = 0
        if self.author:
            libris_query = libris_query + self.author
            continued_string = 1
        if self.title:
            if continued_string: 
                libris_query = libris_query + '+' + self.title
                continued_string = 1
            else: 
                libris_query = libris_query + self.title
                continued_string = 1
        if self.year:
            if continued_string:
                libris_query = libris_query + '+' + self.year
                continued_string = 1
            else: 
                libris_query = libris_query + self.year
                continued_string = 1

        return libris_query

    def getFirst(self, other):
        cmpres = cmp(self.title, other.title)
        
        if(0 == cmpres):
            cmpres = cmp(self.location, other.location)

        if(0 == cmpres):
            cmpres = cmp(self.author, other.author)

        if(0 == cmpres):
            cmpres = cmp(self.year, other.year)

        return cmpres

class LibraParser:
    'Knows how to parse the different library opacs'

    def _extractTitleAndUrl(self, baseurl, urlAndTitle):
        searchfor = 'href="'
        replace = 'href="' + baseurl
        urlfield = urlAndTitle.replace(searchfor, replace)
        urlToOpac = urlfield[urlfield.find('href=')+6:urlfield.find('">')]
        title = strip_tags(urlfield)
        
        return title, urlToOpac

    def parse(self,content,location,storage,baseurl):
        # Extract the relevant metadata using some string magic
        
        #First get the total number of hits through slicing the code
        hitnumbers = content[content.find("<b>Resultat"):]
        hitnumbers = hitnumbers[:hitnumbers.find("</b>")]
        hitnumbers = hitnumbers[hitnumbers.find("av")+3:]
        #hitnumbers = hitnumbers.strip()
        #hitnumbers = int(hitnumbers)
        #print "Hitnumbers eftr slicing inuti parseLibra" + hitnumbers
        
        #Second - take apart the results list and put the parts into the storage
        
        # Slicing away the html surrounding the list with the info we want
        hitlist = content[content.find('<table class="list"'):]
        hitlist = hitlist[:hitlist.find('</table>')]
        
        line = hitlist
        
        # Creates a key for how the table is structured 
        header_row = hitlist[hitlist.find('<tr>')+4:hitlist.find('</tr>')]
        headers_key = {}
        ordercount = 0
        while len(header_row) > 0:
            this_field = header_row[header_row.find('<th'):header_row.find('</th>')]
            header_row = header_row[header_row.find('</th>')+5:]
            this_field = strip_tags(this_field)
            headers_key[this_field] = ordercount
            ordercount = ordercount + 1         
            
        # Strip the first row with headers
        hitlist = hitlist[hitlist.find('</tr>')+5:]
        hitlist = hitlist.replace('<td >','<td>')

        # The loop to parse the full table with info 
        while len(hitlist) > 0:
            temprow = [location]
            thisrow = hitlist[:hitlist.find('</tr>')+5]
            thiscell = thisrow
            for i in range(0,thisrow.count('<td>'),1): 
                cellvalue = thiscell[thiscell.find('<td>')+4:thiscell.find('</td>')]
                thiscell = thiscell[thiscell.find('</td>')+5:]
                temprow.append(cellvalue.strip())
                
            # Ordering the temprow to a standardised form with the use of headers_key
            # Adding city to target row (also corrects the index numbers s
#            target_row = [temprow.pop(0)]
            location = temprow.pop(0)
            
            if 'F\xc3\xb6rfattare' in headers_key:
#                target_row.append(temprow[headers_key['F\xc3\xb6rfattare']])
                author = temprow[headers_key['F\xc3\xb6rfattare']]
            else:
#                target_row.append('')
                author = ''
            if 'Titel' in headers_key:
#                target_row.append(temprow[headers_key['Titel']])
                urlAndTitle = temprow[headers_key['Titel']]
                title, url = self._extractTitleAndUrl(baseurl, urlAndTitle)
            else:
#                target_row.append('')
                title = ''
                url = ''
            if 'Medietyp' in headers_key:
                medietyp = temprow[headers_key['Medietyp']]
                medietyp = strip_tags(medietyp)
#                target_row.append(medietyp)
            else:
#                target_row.append('')
                medietyp = ''
            if '\xc3\x85r' in headers_key:
#                target_row.append(temprow[headers_key['\xc3\x85r']])
                year = temprow[headers_key['\xc3\x85r']]
            else:
#                target_row.append('')
                year = ''
    
            item = MediaItem(title, location, author, medietyp, year, url)
#            storage.append(target_row)
            storage.append(item)
            hitlist = hitlist[hitlist.find('</tr>')+5:]

        return hitnumbers

_kwarecord = 'arena-record-details'

def findDivs(text, elements):
    divstart = text.find('<div')
    divend = text.find('</div')
    
    if((divstart >= 0) and (divstart < divend)):
        while((divstart >= 0) and (divstart < divend)):
            text = findDivs(text[divstart + 4:], elements)
            divstart = text.find('<div')
            divend = text.find('</div')
    else:
        elements.append(text[:divend]) 

    return text[divend + 5:]

class ArenaParser:
    def _appendToText(self, starttext, newtext):
        if('' == starttext):
            return newtext
        else:
            return starttext + ', ' + newtext

    def _appendArenaValue(self, text, origtext):
        start = text.find('"arena-value"')
        text = text[start:]
        start = text.find('>')
        stop = text.find('</span>')
        return self._appendToText(origtext, text[start + 1:stop])

    def parse(self,content,location,storage,baseurl):
        kwindex = content.find(_kwarecord)
        content = content[kwindex:]

        #Find the start of the first record
        kwindex = content.find('arena-record-details')
        content = content[kwindex:]
        hitcount = 0
        
        while(kwindex >= 0):
            records = []
            content = findDivs(content, records)
            title = ''
            url = ''
            author = ''
            type = ''
            year = ''
            
            #Extract the data in the record
            for record in records:
                if(record.find("arena-record-title") > 0):
                    linkpos = record.find('<a href')
                    record = record[linkpos:]
                    linkpos = record.find('"')
                    record = record[linkpos + 1:]
                    linkpos = record.find('"')
                    url = record[:linkpos]
                    record = record[linkpos + 1:]
                    start = record.find('<span>')
                    end = record.find('</span>')
                    title = record[start + 6:end]
                elif(record.find("arena-record-author") > 0):
                    author = self._appendArenaValue(record, author)
                elif(record.find("arena-record-year") > 0):
                    year = self._appendArenaValue(record, year)
                elif(record.find("arena-record-media") > 0):
                    type = self._appendArenaValue(record, type)

            storage.append(MediaItem(title, location, author, type, year, url))
            hitcount = hitcount + 1
            
            #Find the start of the next record
            kwindex = content.find('arena-record-details')
            content = content[kwindex:]

        return str(hitcount)

_kwmrecord = 'ctl00_PageContent_Control_hitlist1_RadGridHitList_ctl00__'
_kwmurlregexp = 'ctl00_PageContent_Control_hitlist1_RadGridHitList_ctl00_ctl[0-9]+_lHyper'

class MikromarcParser:
    def parse(self,content,location,storage,baseurl):
        hitcount = 0
        kwindex = content.find(_kwmrecord)

        while(kwindex >= 0):
            title = ''
            url = ''
            author = ''
            type = ''
            year = ''

            content = content[kwindex:]
            stop = content.find('</tr>')
            record = content[:stop]
            content = content[stop:]

            tds = re.findall('<td.*?</td>', record)

            for td in tds:
                value = re.sub('</*td.*?>', '', td)

                if((len(value) > 0) and unicode(value).isnumeric()):
                    year = value
                elif(re.search(_kwmurlregexp, value) is not None):
                    urlmatch = re.findall('href\s*=\s*".*?"', value)

                    if(len(urlmatch) > 0):
                        url = re.sub('href.*?"', '', urlmatch[0])
                        url = baseurl + url[:-1]

                    title = re.findall('<a.*?</a>', value)

                    if(len(title) > 0):
                        title = re.sub('</*a.*?>|</*span.*?>', '', title[0])

                    data = re.split('<\s*br\s*/*\s*>', value)

                    if(len(data) > 2):
                        author = data[1]
                        type = data[2]

            storage.append(MediaItem(title, location, author, type, year, url))
            hitcount = hitcount + 1

            kwindex = content.find(_kwmrecord)

        return str(hitcount)

_hugeText = u"""
 class="arena-record-details">
                <img class="arena-media-class-icon" alt="Bok:Baskervilles hund:1984" id="id__searchResult__WAR__arenaportlets____14" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/org.apache.wicket.Application/book" title="Bok:Baskervilles hund:1984"/>    <div class="arena-record-title">
                    <a href="http://bibliotek.mark.se/web/arena/results?p_p_state=normal&amp;p_p_lifecycle=1&amp;p_p_action=1&amp;p_p_id=crDetailWicket_WAR_arenaportlets&amp;p_p_col_count=4&amp;p_p_col_id=column-2&amp;p_p_mode=view&amp;back_url=http%3A%2F%2Fbibliotek.mark.se%2Fweb%2Farena%2Fsearch%3Bjsessionid%3DC28087E01863D0D5DC93FD595721207E%3Fp_p_id%3DsearchResult_WAR_arenaportlets%26p_p_lifecycle%3D1%26p_p_state%3Dnormal%26p_p_mode%3Dview%26p_p_col_id%3Dcolumn-2%26p_p_col_count%3D4%26facet_queries%3D%26search_item_no%3D0%26sort_advice%3Dfield%253DRelevance%2526direction%253DDescending%26arena_member_id%3D187406501%26agency_name%3DASE514631%26search_type%3Dsolr%26search_query%3DBaskervilles%2Bhund&amp;facet_queries=&amp;search_item_no=0&amp;sort_advice=field%3DRelevance%26direction%3DDescending&amp;search_type=solr&amp;search_query=Baskervilles+hund&amp;arena_member_id=187406501&amp;search_item_id=73447&amp;agency_name=ASE514631" target="_self"><span>Baskervilles hund</span></a>
                </div><div class="arena-record-author">
                    <span class="arena-field">Av:</span>
                    <span class="arena-value">Doyle, Arthur Conan</span>
                </div><div class="arena-record-year">
                    <span class="arena-field">Utgivnings�r:</span>
                    <span class="arena-value">1984</span>
                </div><div class="arena-record-media">
                    <span class="arena-field">Medietyp:</span>
                    <span class="arena-value">Bok</span>
                </div><div class="arena-record-rating">
                <div class="arena-record-year">
                    <span class="arena-field">Utgivnings�r:</span>
                    <span class="arena-value">1984</span>
                </div>
            <img alt="Markerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-yellow.png"/>
            <img alt="Markerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-yellow.png"/>
            <img alt="Markerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-yellow.png"/>
            <img alt="Markerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-yellow.png"/>
            <img alt="Omarkerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-silver.png"/>
            <img alt="Omarkerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-silver.png"/>
            <img alt="Omarkerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-silver.png"/>
            <img alt="Omarkerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-silver.png"/>
            <img alt="Omarkerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-silver.png"/>
            <img alt="Omarkerad betygsstj&auml;rna" src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/com.axiell.arena.wicket.components.panels.ratingdecor.RatingDecorPanel/star-silver.png"/>
            <div>
                
                
            </div></div><div class="arena-record-tags">
</div></div><div class="arena-record-right">
                <div class="arena-record-availability">
                    <span><em></em></span>
                </div></div><div class="arena-record-button">
                <a id="id__searchResult__WAR__arenaportlets____15" style="display:none"></a>
                <span>    <a class="arena-link-button arena-add-basket" id="id__searchResult__WAR__arenaportlets____16" href="http://bibliotek.mark.se/web/arena/search;jsessionid=C28087E01863D0D5DC93FD595721207E?p_p_id=searchResult_WAR_arenaportlets&amp;p_p_lifecycle=1&amp;p_p_state=normal&amp;p_p_mode=view&amp;p_p_col_id=column-2&amp;p_p_col_count=4&amp;_searchResult_WAR_arenaportlets__wu=%2FsearchResult%2F%3Fwicket%3Ainterface%3D%3A0%3AsearchResultPanel%3AdataContainer%3AdataView%3A1%3AcontainerItem%3Aitem%3AindexedRecordPanel%3AaddToMyMediaListPanel%3AaddToMyMediaLink%3A%3AILinkListener%3A%3A" onclick="if (function(){return Wicket.$('id__searchResult__WAR__arenaportlets____16') != null;}.bind(this)()) { Wicket.showIncrementally('id__searchResult__WAR__arenaportlets____16--ajax-indicator');}var wcall=wicketAjaxGet('http://bibliotek.mark.se/web/arena/search;jsessionid=C28087E01863D0D5DC93FD595721207E?p_p_id=searchResult_WAR_arenaportlets&amp;p_p_lifecycle=2&amp;p_p_state=normal&amp;p_p_mode=view&amp;p_p_resource_id=%2FsearchResult%2F%3Fwicket%3Ainterface%3D%3A0%3AsearchResultPanel%3AdataContainer%3AdataView%3A1%3AcontainerItem%3Aitem%3AindexedRecordPanel%3AaddToMyMediaListPanel%3AaddToMyMediaLink%3A%3AIBehaviorListener%3A0%3A&amp;p_p_cacheability=cacheLevelPage&amp;p_p_col_id=column-2&amp;p_p_col_count=4',function() { ;Wicket.hideIncrementally('id__searchResult__WAR__arenaportlets____16--ajax-indicator');}.bind(this),function() { ;Wicket.hideIncrementally('id__searchResult__WAR__arenaportlets____16--ajax-indicator');}.bind(this), function() {return Wicket.$('id__searchResult__WAR__arenaportlets____16') != null;}.bind(this));return !wcall;">    <span>Lägg i minneslista</span>    </a><span style="display:none;" class="wicket-ajax-indicator" id="id__searchResult__WAR__arenaportlets____16--ajax-indicator"><img src="/arena-portlets/searchResult/ps:searchResult_WAR_arenaportlets_LAYOUT_16308/resources/org.apache.wicket.ajax.AbstractDefaultAjaxBehavior/indicator.gif" alt=""/></span>
        </span>
                <!-- AR-426 <span wicket:id="addToMyCollectionPanel"></span> -->
                <span>
            <a class="arena-link-button" href="http://bibliotek.mark.se/web/arena/search;jsessionid=C28087E01863D0D5DC93FD595721207E?p_p_id=searchResult_WAR_arenaportlets&amp;p_p_lifecycle=1&amp;p_p_state=normal&amp;p_p_mode=view&amp;p_p_col_id=column-2&amp;p_p_col_count=4&amp;_searchResult_WAR_arenaportlets__wu=%2FsearchResult%2F%3Fwicket%3Ainterface%3D%3A0%3AsearchResultPanel%3AdataContainer%3AdataView%3A1%3AcontainerItem%3Aitem%3AindexedRecordPanel%3ArecommendThisPanel%3ArecommendThisLink%3A%3AILinkListener%3A%3A"><span>Tipsa</span></a>
        </span>
            </div><div class="arena-review">
</div></div><div>"""

if __name__ == "__main__":
    list = []
    theRest = findDivs(_hugeText, list)

    for l in list:
        print(l)
        print('********************************************')

    print('           ********************************************')
    print(theRest)
