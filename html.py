'''
Created on 16 jan 2014

@author: PC
'''
"""
Print html page.

"""
class HTMLwriter:
    'A class to handle output of HTML'
    
    def __init__(self):
        self._prioroutput = False

    def startBasicPage(self):
        """Print the start of the page"""
        print 'Content-type: text/html'
        print
        print '<!DOCTYPE html>'
        print '<html>'
        print '<head>'
        print '<meta charset="UTF-8">'
        print '<meta name="viewport" content="width=device-width, initial-scale=1">'
        print '<title>' + 'Sams&ouml;k Halland' + '</title>'
        print '<link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.1/jquery.mobile-1.3.1.min.css" />'
        print '<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>'
        print '<script src="http://code.jquery.com/mobile/1.3.1/jquery.mobile-1.3.1.min.js"></script>'
        print '</head>'
        print '<body>'
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
        """Print the end of the page"""
        print '</div>'
        print '</div>'
        print '</body>'
        print '</html>'
        
    def outputSearchbox(self):
        """Print searchbox"""
        print '<form name="input" action="samsok.py" method="get">'
        print '<input type="text" name="search">'
        print '<input type="submit" value="S&ouml;k" data-role="button" data-inline="true">'
        print '</form>'

    def outputResultsnumbers(self,numbers, location):
        """Print the number of hits at a library
        
        Arguments
        numbers -- hit count
        location -- library

        """

        if numbers:
            print 'Din s&ouml;kning gav ' + numbers + ' tr&auml;ffar i ' + location + '<br>\n'
        else: 
            print 'Din s&ouml;kning gav 0 tr&auml;ffar i ' + location + '<br>\n'

    def _tdPrint(self, str):
        print '<td>'
        print str
        print '</td>'

    def _initPrintIfDefined(self):
        self._prioroutput = False

    def _printIfDefined(self, str):
        if(str):
            if(self._prioroutput):
                print('<br/>')

            print(str)
            self._prioroutput = True

    def output2dList(self, storage, mode):
        """Print a list of MediaItems

        Arguments
        storage -- list of MediaItems
        mode -- select output type; 'table' or 'list' are supported

        """
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

            for item in storage:
                print '<tr>'
                self._tdPrint(item.title)
                self._tdPrint(item.location)
                self._tdPrint(item.author)
                self._tdPrint(item.type)
                self._tdPrint(item.year)
                self._tdPrint(item.url)
                print '</tr>'
            print '</tbody></table>'
        else: 
            print '<p>'
            print '<ul data-role="listview" data-filter="true" data-filter-placeholder="S&ouml;k i tr&auml;fflistan" data-autodividers="true">'
            for item in storage:
                print '<li>'
                print '<a href="' + item.url + '">'+ item.title + '</a>'
                print '<p style="padding-left:2em;">'
                self._initPrintIfDefined()
                self._printIfDefined(item.author)
                self._printIfDefined(item.year)
                self._printIfDefined(item.type)
                print '</p>'
                print '<p style="padding-left:2em;">' + item.location + '</p>'
                print '<a href="http://libris.kb.se/hitlist?d=libris&q=' + item.getLibrisQuery() + '">S&ouml;k i Libris</a>'
                print "</li>"               
            print '</ul>'
            print '</p>'

    def outputHitCountHeader(self, query):
        """Print hit count header"""
        print '<h1>Resultat f&ouml;r "' + query +  '"</h1>'
