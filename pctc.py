#!/usr/bin/env python
# pctc: python curses twitter client

import urwid

class UI(object):
    palette = [
            ('header', 'light green', 'dark blue'),
            ('footer', 'header'),
            ('bg', 'white', 'dark gray'),
        ]

    def __init__(self, twitobj):
        header = urwid.Text(('header', "Welcome to PCTC"))

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
        pass

    def get_replies(self):
        return ["A sample reply"]

    def get_updates(self):
        return ["A sample update"]

if __name__ == "__main__":
    UI(Twitter('', ''))
