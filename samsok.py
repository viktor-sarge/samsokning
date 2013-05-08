#!/usr/local/bin/python

# -*- coding: utf-8 -*-

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
        #print "Inside outputResultnumbers"
        #print "Numbers innehaller:" #+ numbers
        import cgi

        form = cgi.FieldStorage()
        if "search" in form:
            #print '"Search" was in form - if statement filled'
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
            print '<ul data-role="listview" data-filter="true" data-filter-placeholder="Filtrera tr&auml;fflistan">'
            for row in storage:
                print "<li>"
                #print '<h2>' + row[0] +'</h2>'
                #print '<p>' + row[1] + ', ' + row[2] + ', ' + row[3] + '</p>'
                for field in row: 
                    print field 
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
        
        #print "Closing in on the parsing of the hitlist<br>\n"
        line = hitlist
        # Strip the first row with headers
        hitlist = hitlist[hitlist.find('</tr>')+5:]
        hitlist = hitlist.replace('<td >','<td>')
        # The loop to parse the full table with info 
        while len(hitlist) > 0:
            #print "Inside the while loop for parsing the hitlist!<br>\n"
            temprow = [location]
            #print temprow
            thisrow = hitlist[:hitlist.find('</tr>')+5]
            #print thisrow
            thiscell = thisrow
            for i in range(0,4,1): 
                #print "Inside for loop<br>\n"
                cellvalue = thiscell[thiscell.find('<td>')+4:thiscell.find('</td>')]
                #print "Denna cell:" + cellvalue + "<br>\n"
                thiscell = thiscell[thiscell.find('</td>')+5:]
                temprow.append(cellvalue)
            #print "Outside the for loop now"
            storage.append(temprow)
            #print "Appeding temprow to storage was ok"
            hitlist = hitlist[hitlist.find('</tr>')+5:]
        #print storage
        
        # Cleaning up the contents a bit and removing remaining html
        for row in storage:
            # Stripping away relative links and changing from icons to text representations. 
            #mediatype = row.pop(5)
            #mediatype = mediatype[mediatype.find('alt="')+5:]
            #mediatype = mediatype[:mediatype.find('"')]
            #row.insert(4,mediatype)
            #print row[2]
            
            # Making the relative URLs from the source point at the right source. 
            urlfield = row.pop(2)
            urlfield = urlfield.replace('href="','href='+baseurl)
            row.insert(2,urlfield)
         
        
        #print hitlist
        return storage, hitnumbers
        
class metadataSortmachine: 
    
    def groupByTitle(self,list):
        for row in list: 
            title = row.pop(2)
            row.insert(0,title)
        list.sort()
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

