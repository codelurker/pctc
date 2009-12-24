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
        self.twitobj = twitobj

        header = urwid.Text("Welcome to PCTC. Logged in as %s (@%s)." %
                                            (twitobj.name, twitobj.username))
        header = urwid.AttrMap(header, 'header')

        self.replies = self._wrap_statuses(twitobj.get_replies())
        self.updates = self._wrap_statuses(twitobj.get_updates())
        columns = urwid.Columns([self.updates, self.replies], dividechars=2)

        self.footer = urwid.AttrMap(urwid.Edit("Tweet: "), 'footer')

        self.frame = urwid.Frame(columns, header, self.footer, focus_part='footer')
        self.focussed = 'footer'
        wrapped = urwid.AttrMap(self.frame, 'bg')
        loop = urwid.MainLoop(wrapped, UI.palette, unhandled_input=self.handle)
        try:
            loop.run()
        except KeyboardInterrupt:
            print "Keyboard interrupt received, quitting gracefully"
            raise urwid.ExitMainLoop

    def _wrap_statuses(self, statuses):
        textlist = map(urwid.Text, statuses)
        walker = urwid.SimpleListWalker(textlist)
        return urwid.ListBox(walker)

    def handle(self, keys):
        if keys == 'tab':
            self.change_focus()
            return
        if keys == 'enter':
            self.post()
            return
        if keys == 'f5':
            self.refresh()

    def change_focus(self):
        if self.focussed == 'footer':
            self.frame.set_focus('body')
            self.focussed = 'body'
        elif self.focussed == 'body':
            self.frame.set_focus('footer')
            self.focussed = 'footer'

    def post(self):
        edit = self.footer.original_widget
        text = edit.get_edit_text()
        edit.set_edit_text('')
        if len(text) < 140:
            self.twitobj.post(text)

    def refresh(self):
        for category in ('replies', 'updates'):
            walker = getattr(self, category).body
            walker[:] = map(urwid.Text, getattr(self.twitobj, 'get_%s' %
                                        category)())
