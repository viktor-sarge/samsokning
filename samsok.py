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

import cgi  
import cgitb

from html import HTMLwriter
from search import performSearch
        

cgitb.enable()     
HTMLmachine = HTMLwriter()
HTMLmachine.startBasicPage()
HTMLmachine.outputSearchbox()
storage = []
connector = connectorclass()
form = cgi.FieldStorage()

if "search" in form:
    performSearch(form['search'].value, HTMLmachine)

HTMLmachine.closeBasicPage()
