# coding=utf-8
'''
Created on 16 jan 2014

@author: PC
'''

"""
Parsers for different kinds of library systems. 

"""
import re
from lxml import etree
from StringIO import StringIO
import urlparse
import json
import cgi

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

_kwlsingle = 'Tillbaka till resultatlista'
_kwlsinglestart = 'listline2'
_kwlsingleend = '/table'
_kwlauthor = 'Författare:'
_kwltitle = 'Titel:'
_kwlyear = 'Förlag/år:'
_kwlurlstart = '<table'
_kwlurlend = 'Utförlig kataloginfo'

class LibraParser:
    'Knows how to parse Libra'
    def _strip_tags(self, raw_html):
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

    def _parseMultiple(self,content,location,storage,baseurl):
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
            location = temprow.pop(0)
            
            if 'F\xc3\xb6rfattare' in headers_key:
                author = temprow[headers_key['F\xc3\xb6rfattare']]
            else:
                author = ''
            if 'Titel' in headers_key:
                urlAndTitle = temprow[headers_key['Titel']]
                title, url = self._extractTitleAndUrl(baseurl, urlAndTitle)
            else:
                title = ''
                url = ''
            if 'Medietyp' in headers_key:
                medietyp = temprow[headers_key['Medietyp']]
                medietyp = self._strip_tags(medietyp)
            else:
                medietyp = ''
            if '\xc3\x85r' in headers_key:
                year = temprow[headers_key['\xc3\x85r']]
            else:
                year = ''

            item = MediaItem(title, location, author, medietyp, year, url)
            storage.append(item)
            hitlist = hitlist[hitlist.find('</tr>')+5:]

        return str(len(storage))

    def _parseOne(self,content,location,storage,baseurl, searchurl):
            start = content.find(_kwlsinglestart)
            content = content[start:]
            stop = content.find(_kwlsingleend)
            data = content[:stop]
            urldata = content[stop + 2:]
            start = urldata.find(_kwlurlstart)
            stop = urldata.find(_kwlurlend)
            urldata = content[start:stop]
            title = ''
            author = ''
            year = ''

            trs = re.findall('<tr.*?</tr>', data)

            for tr in trs:
                tds = re.findall('<td.*?</td>', tr)

                if(len(tds) > 1):
                    if(tds[0].find(_kwlauthor) >= 0):
                        author = re.sub('</*.*?>', '', tds[1])
                    elif(tds[0].find(_kwltitle) >= 0):
                        title = re.sub('</*.*?>', '', tds[1])
                    elif(tds[0].find(_kwlyear) >= 0):
                        year = re.sub('</*.*?>', '', tds[1])
                        years = re.findall('[0-9]{4}', year)
                        
                        if(len(years) > 0):
                            year = years[0]
                        else:
                            year = ''

#This url goes to a search for the author
#            urls = re.findall('<a.*?>', urldata)
#            
#            if(len(urls) > 0):
#                url = re.sub('<a.*?"', '', urls[0])
#                url = baseurl + re.sub('">', '', url)
#            else:
#                url = ''

            item = MediaItem(title, location, author, '', year, searchurl)
            storage.append(item)

            return str(len(storage))

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string
        
        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        # Extract the relevant metadata using some string magic
        
        #First get the total number of hits through slicing the code
        hitnumbers = content[content.find("<b>Resultat"):]
        hitnumbers = hitnumbers[:hitnumbers.find("</b>")]
        hitnumbers = hitnumbers[hitnumbers.find("av")+3:]
        #hitnumbers = hitnumbers.strip()
        #hitnumbers = int(hitnumbers)
        #print "Hitnumbers eftr slicing inuti parseLibra" + hitnumbers
        
        if(content.find(_kwlsingle) >= 0):
            return (self._parseOne(content,location,storage,baseurl, searchurl), '1')
        else:
            return (self._parseMultiple(content,location,storage,baseurl), hitnumbers)

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

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string
        
        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- unused
        searchurl -- search url

        """
        totalmatch = re.search('<span class="feedbackPanelINFO">.*?(\d+).*?</span>', content)
        if totalmatch:
            totalhits = totalmatch.group(1)
        else:
            totalhits = '0'


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

        return (str(hitcount), totalhits)

_kwmrecord = 'ctl00_PageContent_Control_hitlist1_RadGridHitList_ctl00__'
_kwmurlregexp = 'ctl00_PageContent_Control_hitlist1_RadGridHitList_ctl00_ctl[0-9]+_lHyper'

class MikromarcParser:
    """Parse search results from Mikromarc"""
    def _unspan(self, str):
        return re.sub('</*a.*?>|</*span.*?>', '', str)

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string
        
        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        hitcount = 0
        kwindex = content.find(_kwmrecord)

        totalmatch = re.search('<span id="ctl00_PageContent_Control_hitlist1_LabelSearchHeader">.*?<B>(\d+)</B>.*?</span>', content, re.IGNORECASE)
        if totalmatch:
            totalhits = totalmatch.group(1)
        else:
            totalhits = '0'

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
                else:
                    if(value.find('<img') >= 0):
                        imgs = re.findall('<img.*?/>', value)

                        if(len(imgs) > 0):
                            imgs = re.findall('alt\s*=\s*".*?"', imgs[0])

                            if(len(imgs) > 0):
                                img = re.sub('alt\s*=\s*"', '', imgs[0])
                                type = img[:-1]

            storage.append(MediaItem(title, location, author, type, year, url))
            hitcount = hitcount + 1

            kwindex = content.find(_kwmrecord)

        return (str(hitcount), totalhits)

class BaseXmlParser:
    encoding = 'utf-8'

    def _getInnerText(self, element):
        s = ''.join([x.strip() for x in element.itertext(etree.Element)])
        if isinstance(s, unicode):
            s = s.encode(self.encoding)
        return s

    def _getElementText(self, element):
        s = element.text.strip()
        if isinstance(s, unicode):
            s = s.encode(self.encoding)
        return s

class GotlibParser(BaseXmlParser):

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)

        totalhitsspan = tree.xpath("//span[@class='noResultsHideMessage']")
        if totalhitsspan and len(totalhitsspan) > 0:
            spantext = self._getInnerText(totalhitsspan[0])
            totalmatch = re.search('\d+ - \d+ .*? (\d+)', spantext)
            if totalmatch:
                totalhits = totalmatch.group(1)
            else:
                totalhits = '0'
        else:
            totalhits = '0'

        results = tree.xpath("//table[@class='browseResult']/tr")
        for result in results:
            isProgram = result.xpath('.//span[contains(@id, "programMediaTypeInsertComponent")]')
            if len(isProgram) > 0:
                # Program item, skip this
                continue

            title = self._getInnerText(result.xpath(".//div[@class='dpBibTitle']")[0])
            author = self._getInnerText(result.xpath(".//div[@class='dpBibAuthor']")[0])
            type = self._getInnerText(result.xpath(".//span[@class='itemMediaDescription']")[0])
            year = self._getInnerText(result.xpath(".//span[@class='itemMediaYear']")[0])
            url = urlparse.urljoin(baseurl, result.xpath(".//div[@class='dpBibTitle']/a/@href")[0])
            storage.append(MediaItem(title, location, author, type, year, url))

        return (str(len(storage)), totalhits)

class MalmoParser(BaseXmlParser):
    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        self.encoding = 'latin-1'
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)
        results = tree.xpath("//tr[@class='briefCitRow']")

        totalhitsspan = tree.xpath("//td[@class='browseHeaderData']")
        if totalhitsspan and len(totalhitsspan) > 0:
            spantext = self._getInnerText(totalhitsspan[0])
            totalmatch = re.search('\d+-\d+ .*? (\d+)', spantext)
            if totalmatch:
                totalhits = totalmatch.group(1)
            else:
                totalhits = '0'
        else:
            totalhits = '0'


        hits = []
        for result in results:
            titletags = result.xpath(".//span[@class='briefcitTitle']/../a")
            if len(titletags) == 0:
                continue
            title = self._getInnerText(titletags[0])
            author = self._getInnerText(result.xpath(".//span[@class='briefcitTitle']")[0])
            type = result.xpath(".//span[@class='briefcitMedia']/img[1]/@alt")[0]
            year = self._getInnerText(result.xpath(".//table/tr/td[5]")[0])[-4:]
            if not year.isdigit():
                year = ''
            url = urlparse.urljoin(baseurl, titletags[0].xpath("@href")[0])
            hits.append(MediaItem(title, location, author, type, year, url))

        # Special case for only one hit
        if len(results) == 0:
            results = tree.xpath("//tr[@class='bibInfoEntry']")
            if len(results) > 0:
                result = results[0]
                title = self._getInnerText(result.xpath(".//td[@class='bibInfoLabel' and text() = 'Titel']/../td[@class='bibInfoData']")[0])
                author = self._getInnerText(result.xpath(".//td[@class='bibInfoLabel' and text() = 'Namn']/../td[@class='bibInfoData']")[0])
                type = result.xpath("//td[@class='media']/img[1]/@alt")[0]
                year = self._getInnerText(result.xpath(".//td[@class='bibInfoLabel' and text() = 'Utgivning']/../td[@class='bibInfoData']")[0])
                year = year[-4:]
                if not year.isdigit():
                    year = ""
                url = searchurl
                hits.append(MediaItem(title, location, author, type, year, url))

        storage.extend(hits)
        return (str(len(hits)), totalhits)

class OlaParser(BaseXmlParser):

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)

        totalhitsspan = tree.xpath("//span[@class='result-text']")
        if totalhitsspan and len(totalhitsspan) > 0:
            spantext = self._getInnerText(totalhitsspan[0])
            totalmatch = re.search('(\d+)', spantext)
            if totalmatch:
                totalhits = totalmatch.group(1)
            else:
                totalhits = '0'
        else:
            totalhits = '0'


        results = tree.xpath("//ol[@class='search-result clearfix']/li[@class='work-item clearfix']")
        for result in results:
            title = self._getInnerText(result.xpath(".//h3[@class='work-details-header']/a")[0])
            try:
                author = self._getInnerText(result.xpath(".//div[@class='work-details']/p")[0])
                if author.lower().startswith("av:"):
                    author = author[len("av:"):]
            except IndexError:
                author = ''
            type = " / ".join([self._getElementText(x) for x in result.xpath(".//ol[@class='media-type-list']/li/a/span")])
            year = self._getInnerText(result.xpath(".//h3[@class='work-details-header']/small")[0])[1:-1]
            url = urlparse.urljoin(baseurl, result.xpath(".//h3[@class='work-details-header']/a/@href")[0])
            storage.append(MediaItem(title, location, author, type, year, url))

        return (str(len(results)), totalhits)

class KohaParser(BaseXmlParser):

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)

        totalhitsspan = tree.xpath("//p[@id='numresults']")
        if totalhitsspan and len(totalhitsspan) > 0:
            spantext = self._getInnerText(totalhitsspan[0])
            totalmatch = re.search('(\d+)', spantext)
            if totalmatch:
                totalhits = totalmatch.group(1)
            else:
                totalhits = '0'
        else:
            totalhits = '0'

        results = tree.xpath("//td[@class='bibliocol']")
        i = 1
        for result in results:
            i += 1
            title = self._getInnerText(result.xpath(".//a[@class='title']")[0])
            try:
                author = self._getInnerText(result.xpath(".//span[@class='author']")[0])
            except IndexError:
                author = ''
            type = self._getInnerText(result.xpath(".//span[@class='results_summary type']")[0])
            try:
                publisher = self._getInnerText(result.xpath(".//span[@class='results_summary publisher']")[0])
                if len(publisher) >= 4 and publisher[-4:].isdigit():
                    year = publisher[-4:]
                else:
                    year = ""
            except IndexError:
                year = ""
            url = urlparse.urljoin(baseurl, result.xpath(".//a[@class='title']/@href")[0])
            storage.append(MediaItem(title, location, author, type, year, url))

        return (str(len(results)), totalhits)

class MinabibliotekParser(BaseXmlParser):

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)

        totalhitsspan = tree.xpath("//form[@id='SearchResultForm']/p[@class='information']")
        if totalhitsspan and len(totalhitsspan) > 0:
            spantext = self._getInnerText(totalhitsspan[0])
            totalmatch = re.search('(\d+)', spantext)
            if totalmatch:
                totalhits = totalmatch.group(1)
            else:
                totalhits = '0'
        else:
            totalhits = '0'


        results = tree.xpath("//form[@id='MemorylistForm']/ol[@class='CS_list-container']/li")
        for result in results:
            title = self._getInnerText(result.xpath(".//h3[@class='title']/a")[0])
            try:
                author = self._getInnerText(result.xpath(".//p[@class='author']")[0])
                if author.lower().startswith("av:"):
                    author = author[len("av:"):]
            except IndexError:
                author = ''
            type = " / ".join(self._getElementText(x) for x in result.xpath(".//ol[@class='media-type CS_clearfix']/li/a/span"))
            year = self._getInnerText(result.xpath(".//span[@class='date']")[0])
            url = urlparse.urljoin(baseurl, result.xpath(".//h3[@class='title']/a/@href")[0])
            storage.append(MediaItem(title, location, author, type, year, url))

        return (str(len(results)), totalhits)


class SsbParser(BaseXmlParser):
    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(content), parser)

        totalhitsspan = tree.xpath("//div[@id='results-filter']/p[@class='total']/em[3]")
        if totalhitsspan and len(totalhitsspan) > 0:
            totalhits = self._getInnerText(totalhitsspan[0])
        else:
            totalhits = '0'


        # The search result HTML is malformed and the list elements do not get properly parsed
        # as siblings, so we have to use this slightly more complicated expression to get the right
        # divs from within the list items instead.
        results = tree.xpath("//ol[@class='results-icon']//div[string(number(@id)) != 'NaN' and @class='row-fluid']")
        for result in results:
            title = self._getInnerText(result.xpath(".//div[@class='title']/h2/a/b")[0])
            author = self._getInnerText(result.xpath(".//span[@class='author']")[0])
            type = self._getInnerText(result.xpath(".//span[@class='mediatype']")[0])
            if type.startswith("(") and type.endswith(")"):
                type = type[1:-1]
            year = self._getInnerText(result.xpath(".//span[@class='year']")[0])
            if (year.endswith(",")):
                year = year[0:-1]
            url = urlparse.urljoin(baseurl, result.xpath(".//div[@class='title']/h2/a/@href")[0])
            storage.append(MediaItem(title, location, author, type, year, url))

        return (str(len(storage)), totalhits)

class XsearchParser:
    def htmlCode(self, s):
        return cgi.escape(s).encode('ascii', 'xmlcharrefreplace')

    def parse(self,content,location,storage,baseurl, searchurl):
        """Parse content, add any contained items to storage and return number of items found as a string

        Arguments
        content -- (html-)content to parse
        location -- library location
        storage -- list to which MediaItems will be added as they are found in content
        baseurl -- base url to media content
        searchurl -- search url

        """

        js = json.loads(content, 'utf-8')['xsearch']

        totalhits = str(js['records'])

        for result in js['list']:
            title = self.htmlCode(result['title']) if result.has_key('title') else ''
            author = self.htmlCode(result['creator']) if result.has_key('creator') else ''
            type = self.htmlCode(result['type']) if result.has_key('type') else ''
            year = self.htmlCode(result['date']) if result.has_key('date') else ''
            url = self.htmlCode(result['identifier']) if result.has_key('identifier') else ''
            storage.append(MediaItem(title, location, author, type, year, url))

        return (str(len(storage)), totalhits)
