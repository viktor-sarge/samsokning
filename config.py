# -*- coding: utf-8 -*-

import ConfigParser

_defaults = {
    'searchSources': '*',
    'localLibFolders': '["../../lib/python2.7/site-packages/lxml-3.3.1-py2.7-freebsd-9.2-RELEASE-p3-amd64.egg"]',
    'connectorTimeoutSeconds': '10',
    'showTimeElapsed': 'False'
}

defaultSection = 'Samsok'

parser = ConfigParser.RawConfigParser(_defaults)
parser.read('samsok.cfg')
if not parser.has_section(defaultSection):
    parser.add_section(defaultSection)
