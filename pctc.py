#!/usr/bin/env python
# pctc: python curses twitter client

from pctclib import ui, backend, config
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u', '--username', help='log in as UNAME',
            metavar='UNAME')
parser.add_option('-p', '--password', help='use password PW',
            metavar='PW')
options, args = parser.parse_args()
if not options.username or not options.password:
    try:
        username, password = config.username, config.password
    except AttributeError:
        parser.error("must give username and password")
else:
    username, password = options.username, options.password

ui.UI(backend.Twitter(username, password))
