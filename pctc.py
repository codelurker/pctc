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

    def change_focus(self):
        if self.focussed == 'footer':
            self.frame.set_focus('body')
        elif self.focussed == 'body':
            self.frame.set_focus('footer')

    def post(self):
        edit = self.footer.original_widget
        text = edit.get_edit_text()
        edit.set_edit_text('')
        if len(text) < 140:
            self.twitobj.post(text)

class Twitter(object):
    def __init__(self, uname, pw):
        self.api = twitter.Api(username=uname, password=pw)
        self.username = uname
        self.name = self.api.GetUser(uname).name

    def get_replies(self):
        statuses = []
        for status in self.api.GetReplies():
            text = "%s\n-- %s (@%s)" % (status.text, status.user.name,
                        status.user.screen_name)
            statuses.append(text)
        return statuses

    def get_updates(self):
        statuses = []
        for status in self.api.GetFriendsTimeline():
            text = "%s\n-- %s (@%s)" % (status.text, status.user.name,
                        status.user.screen_name)
            statuses.append(text)
        return statuses

    def post(self, text):
        self.api.PostUpdate(text)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-u', '--username', help='log in as UNAME',
                metavar='UNAME')
    parser.add_option('-p', '--password', help='use password PW',
                metavar='PW')
    options, args = parser.parse_args()
    if not options.username or not options.password:
        parser.error("must give username and password")
    UI(Twitter(options.username, options.password))
