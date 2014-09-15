#!/usr/local/bin/python2.7

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
cgitb.enable()

# First off, modify the path to allow any locally installed packages
import config
import sys
import os
import json
for folder in json.loads(config.parser.get(config.defaultSection, 'localLibFolders')):
    sys.path.append(os.path.abspath(folder))

from html import HTMLwriter
from search import performSearch

if __name__ == '__main__':
    HTMLmachine = HTMLwriter()
    HTMLmachine.startBasicPage()
    HTMLmachine.outputSearchbox()
    storage = []
    form = cgi.FieldStorage()

    if "search" in form:
        performSearch(form['search'].value, HTMLmachine)

    HTMLmachine.closeBasicPage()
