#!/usr/bin/env python
# pctc: python curses twitter client

import urwid
import twitter

class UI(object):
    palette = [
            ('header', 'light green', 'dark blue'),
            ('footer', 'header'),
            ('bg', 'white', 'dark gray'),
        ]

    def __init__(self, twitobj):
        header = urwid.AttrMap(urwid.Text("Welcome to PCTC"), 'header')

        replies = self._wrap_statuses(twitobj.get_replies())
        updates = self._wrap_statuses(twitobj.get_updates())
        columns = urwid.Columns([replies, updates])

        footer = urwid.AttrMap(urwid.Edit("Tweet: "), 'footer')

        frame = urwid.Frame(columns, header, footer, focus_part='footer')
        wrapped = urwid.AttrMap(frame, 'bg')
        loop = urwid.MainLoop(wrapped, UI.palette, unhandled_input=self.handle)
        loop.run()

    def _wrap_statuses(self, statuses):
        textlist = map(urwid.Text, statuses)
        walker = urwid.SimpleListWalker(textlist)
        return urwid.ListBox(walker)

    def handle(self, keys):
        pass

class Twitter(object):
    def __init__(self, uname, pw):
        self.api = twitter.Api(username=uname, password=pw)

    def get_replies(self):
        return [s.text for s in self.api.GetReplies()]

    def get_updates(self):
        return [s.text for s in self.api.GetFriendsTimeline()]

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-u', '--username', help='log in as UNAME',
                metavar='UNAME')
    parser.add_option('-p', '--password', help='use password PW',
                metavar='PW')
    options, args = parser.parse_args()
    if not options.username or not options.password:
        parser.error("Error: must give username and password")
    UI(Twitter(options.username, options.password))
