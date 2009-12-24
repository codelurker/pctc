#!/usr/bin/env python
# pctc: python curses twitter client

from pctclib import ui, backend
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u', '--username', help='log in as UNAME',
            metavar='UNAME')
parser.add_option('-p', '--password', help='use password PW',
            metavar='PW')
options, args = parser.parse_args()
if not options.username or not options.password:
    parser.error("must give username and password")
ui.UI(backend.Twitter(options.username, options.password))
