# coding=utf-8
'''
Created on 16 jan 2014

@author: PC
'''
"""
Parsers for different kinds of library systems. 

"""
import re

class MediaItem:
    """An item in a library"""
    def __init__(self, title, location, author, type, year, url):
        """Initiate
        
        Arguments
        title -- media title
        location -- library location
        author -- media author(s)
        type -- media type
        year -- year
        url -- url

        """

        self.title = title
        self.location = location
        self.author = author
        self.type = type
        self.year = year
        self.url = url

    def getLibrisQuery(self):
        """Get a Libris search string for this MediaItem"""

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
        """Compare two MediaItems and return a cmp-like result
        
        Argument
        other -- MediaItem to compare this MediaItem to

        """

        cmpres = cmp(self.title, other.title)
        
        if(0 == cmpres):
            cmpres = cmp(self.location, other.location)

        if(0 == cmpres):
            cmpres = cmp(self.author, other.author)

        if(0 == cmpres):
            cmpres = cmp(self.year, other.year)

        return cmpres

class LibraParser:
    'Knows how to parse Libra'
    def _strip_tags(raw_html):
        """Return raw_html with tags removed
        Argument
        raw_html -- text to strip
    
        """
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr,'', raw_html)
        return cleantext


    def _extractTitleAndUrl(self, baseurl, urlAndTitle):
        searchfor = 'href="'
        replace = 'href="' + baseurl
        urlfield = urlAndTitle.replace(searchfor, replace)
        urlToOpac = urlfield[urlfield.find('href=')+6:urlfield.find('">')]
        title = self._strip_tags(urlfield)
        
        return title, urlToOpac

    def parse(self,content,location,storage,baseurl):
        """Parse content, add any contained items to storage and return number of items found as a string
        
        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content

        """
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
            this_field = self._strip_tags(this_field)
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
                medietyp = self._strip_tags(medietyp)
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
    """Parse search results from Arena"""
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
        """Parse content, add any contained items to storage and return number of items found as a string
        
        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- unused

        """
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
    """Parse search results from Mikromarc"""
    def _unspan(self, str):
        return re.sub('</*a.*?>|</*span.*?>', '', str)

    def parse(self,content,location,storage,baseurl):
        """Parse content, add any contained items to storage and return number of items found as a string
        
        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content

        """
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

                if((len(value) > 0) and value.isdigit()):
                    year = value
                elif(re.search(_kwmurlregexp, value) is not None):
                    urlmatch = re.findall('href\s*=\s*".*?"', value)

                    if(len(urlmatch) > 0):
                        url = re.sub('href.*?"', '', urlmatch[0])
                        url = baseurl + url[:-1]

                    title = re.findall('<a.*?</a>', value)

                    if(len(title) > 0):
                        title = self._unspan(title[0])

                    data = re.split('<\s*br\s*/*\s*>', value)

                    if(len(data) > 2):
                        author = self._unspan(data[1])
                        type = self._unspan(data[2])

            storage.append(MediaItem(title, location, author, type, year, url))
            hitcount = hitcount + 1

            kwindex = content.find(_kwmrecord)

        return str(hitcount)
