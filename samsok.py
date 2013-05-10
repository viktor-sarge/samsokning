#!/usr/local/bin/python

# -*- coding: utf-8 -*-

#    Copyright 2013 Viktor Sarge
#    This file is part of Samsok.
#
#    Samsok is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Samsok is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import re

class HTMLwriter:
    'A class to handle output of HTML'
    
    def startBasicPage(self):
        print "Content-type: text/html"
        print
        print "<!DOCTYPE html>"
        print "<html>"
        print "<head>"
        print '<meta charset="UTF-8">'
        print '<meta name="viewport" content="width=device-width, initial-scale=1">'
        print "<title>" + "Sams&ouml;k Halland" + "</title>"
        print '<link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.1/jquery.mobile-1.3.1.min.css" />'
        print '<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>'
        print '<script src="http://code.jquery.com/mobile/1.3.1/jquery.mobile-1.3.1.min.js"></script>'
        print "</head>"
        print "<body>"
        print '<div data-role="page">'
        print '<div data-role="panel" id="infopanel">'
        print '<p>Sams&ouml;k Halland &auml;r en tj&auml;nst fr&aring;n <a href="http://www.regionhalland.se/regionbibliotek">Kultur i Halland - Regionbibliotek</a> t&auml;nkt att fungera som ers&auml;ttare f&ouml;r Bibliotek24 i fj&auml;rrl&aring;earbetet.</p>'
        print '<p>Tj&auml;nsten &auml;r under uppbyggnad och synpunkter mottages tacksamt till viktor [punkt] sarge [snabela] regionhalland [punkt] se</p>'
        print '<p>K&auml;llkoden finns p&aring; <a href="http://github.com/regionbibliotekhalland/samsokning">regionbibliotekets Github-konto</a></p>'
        print '</div><!-- /panel -->'
        print '<div data-role="header">'
        print '<a href="#infopanel">Info</a><h1>Sams&ouml;k Halland</h1>'
        print '</div>'
        print '<div data-role="content">'
    
    def closeBasicPage(self):
        print '</div>'
        print '</div>'
        print "</body>"
        print "</html>"
        
    def outputSearchbox(self):
        print '<form name="input" action="samsok.py" method="get">'
        print '<input type="text" name="search">'
        print '<input type="submit" value="S&ouml;k" data-role="button" data-inline="true">'
        print '</form>'

    def outputResultsnumbers(self,numbers, location):

        import cgi
        form = cgi.FieldStorage()
        if "search" in form:
            if numbers:
                print "Din s&ouml;kning gav " + numbers + " tr&auml;ffar i " + location + "<br>\n"
            else: 
                print "Din s&ouml;kning gav 0 tr&auml;ffar i " + location + "<br>\n"
          
    def output2dList(self, storage, mode):
        if mode == "table":
            print '<table>'
            print '<thead>'
            print '<tr>'
            print '<th>Titel</th>'
            print '<th>Bibliotek</th>'
            print '<th>Klassning</th>'
            print '<th>Typ</th>'
            print '</tr>'
            print '</thead>'
            print '<tbody>'
            for row in storage:
                print "<tr>"
                for field in row: 
                    print "<td>"
                    print field
                    print "</td>"
                print "</tr>"
            print "</tbody></table>"
        else: 
            print "<p>"
            print '<ul data-role="listview" data-filter="true" data-filter-placeholder="S&ouml;k i tr&auml;fflistan" data-autodividers="true">'
            for row in storage:
                print "<li>"
                print '<a href="' + row[5] + '">'+ row[0] + '</a>'
                print '<p style="padding-left:2em;">'
                if row[2]:
                    print row[2] 
                if row[3]:
                    print row[3]
                if row[4]:
                    print row[4]
                print '</p>'
                print '<p style="padding-left:2em;">' + row[1] + '</p>'
                print '<a href="http://libris.kb.se/hitlist?d=libris&q=">S&ouml;k i Libris</a>'
                print "</li>"               
            print "</ul>"
            print "</p>"

class connectorclass: 
    'Knows how to fetch the different library opacs'
    
    def __init__(self):
        import urllib
        
    def getpage(self, url):
        import urllib
        page = urllib.urlopen(url)
        content = page.read()
        page.close()     
        return content 
 
from HTMLParser import HTMLParser
import htmlentitydefs

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)
 
def strip_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html)
    return cleantext
 
 
        
class opacParser:
    'Knows how to parse the different library opacs'
    
    def parseLibra(self,content,location,storage,baseurl):
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
            for i in range(0,5,1): 
                cellvalue = thiscell[thiscell.find('<td>')+4:thiscell.find('</td>')]
                thiscell = thiscell[thiscell.find('</td>')+5:]
                temprow.append(cellvalue.strip())
                
            # Ordering the temprow to a standardised form with the use of headers_key
            # Adding city to target row (also corrects the index numbers s
            target_row = [temprow.pop(0)]
            if 'F\xc3\xb6rfattare' in headers_key:
                target_row.append(temprow[headers_key['F\xc3\xb6rfattare']])
            else:
                target_row.append('')
            if 'Titel' in headers_key:
                target_row.append(temprow[headers_key['Titel']])
            else:
                target_row.append('')
            if 'Medietyp' in headers_key:
                medietyp = temprow[headers_key['Medietyp']]
                medietyp = strip_tags(medietyp)
                target_row.append(medietyp)
            else:
                target_row.append('')
            if '\xc3\x85r' in headers_key:
                target_row.append(temprow[headers_key['\xc3\x85r']])
            else:
                target_row.append('')
    
            storage.append(target_row)
            hitlist = hitlist[hitlist.find('</tr>')+5:]
        
        # Cleaning up the contents a bit and removing remaining html
        for row in storage:
            # Making the relative URLs from the source point at the right source. 
            urlfield = row.pop(2)
            searchfor = 'href="'
            replace = 'href="' + baseurl
            urlfield = urlfield.replace(searchfor, replace)
            urlToOpac = urlfield[urlfield.find('href=')+6:urlfield.find('">')]
            title = strip_tags(urlfield)
            row.insert(2,title)
            row.append(urlToOpac)
            
        return storage, hitnumbers
        
class metadataSortmachine: 
    
    def groupByTitle(self,list):
        for row in list: 
            title = row.pop(2)
            row.insert(0,title)
        list = sorted(list)
        return list  
            
        
import cgi  
import cgitb

cgitb.enable()     
HTMLmachine = HTMLwriter()
HTMLmachine.startBasicPage()
HTMLmachine.outputSearchbox()
storage = []
connector = connectorclass()
form = cgi.FieldStorage()

#totalhits = 0
if "search" in form:
    # Searching Laholm
    page = connector.getpage('http://laholmopac.kultur.halmstad.se/opac/search_result.aspx?TextFritext=' + form['search'].value) 
    parser = opacParser()
    storage, hitnumbers = parser.parseLibra(page,"Laholm", storage,'http://laholmopac.kultur.halmstad.se/opac/')
    #print "Calculating number of total hits" 
    #totalhits = totalhits + hitnumbers
    print '<h1>Resultat f&ouml;r "' + form['search'].value +  '"</h1>'
    HTMLmachine.outputResultsnumbers(hitnumbers,"Laholm")
    
    # Searching Halmstad
    page = connector.getpage('http://halmstadopac.kultur.halmstad.se/opac/search_result.aspx?TextFritext=' + form['search'].value) 
    storage, hitnumbers = parser.parseLibra(page,"Halmstad", storage,'http://halmstadopac.kultur.halmstad.se/opac/')
    #print "Calculating number of total hits" 
    #totalhits = totalhits + hitnumbers
    HTMLmachine.outputResultsnumbers(hitnumbers,"Halmstad")
    
    # Searching Falkenberg
    page = connector.getpage('http://www5.falkenberg.se/opac/opac/search_result.aspx?TextFritext=' + form['search'].value) 
    storage, hitnumbers = parser.parseLibra(page,"Falkenberg", storage,'http://www5.falkenberg.se/opac/opac/')
    #print "Calculating number of total hits" 
    #totalhits = totalhits + hitnumbers
    HTMLmachine.outputResultsnumbers(hitnumbers,"Falkenberg")
    
    # Searching Kungsbacka
    page = connector.getpage('http://bibold.kungsbacka.se/opac/search_result.aspx?TextFritext=' + form['search'].value) 
    storage, hitnumbers = parser.parseLibra(page,"Kungsbacka", storage,'http://bibold.kungsbacka.se/opac/')
    #print "Calculating number of total hits" 
    #totalhits = totalhits + hitnumbers
    HTMLmachine.outputResultsnumbers(hitnumbers,"Kungsbacka")    
    
    # Searching Varberg
    page = connector.getpage('http://bib.varberg.se/opac/search_result.aspx?TextFritext=' + form['search'].value) 
    storage, hitnumbers = parser.parseLibra(page,"Varberg", storage,'http://bib.varberg.se/opac/')
    #print "Calculating number of total hits" 
    #totalhits = totalhits + hitnumbers
    HTMLmachine.outputResultsnumbers(hitnumbers,"Varberg")
    
    sorter = metadataSortmachine()
    storage = sorter.groupByTitle(storage)
    HTMLmachine.output2dList(storage,"list")

HTMLmachine.closeBasicPage()

