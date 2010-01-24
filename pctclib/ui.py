# pctc: python curses twitter client
"""Control the UI for PCTC.

Classes:
    Tweet: represent a tweet as an urwid widget
    UI:    run the UI
"""

import urwid
import re

class Tweet(urwid.Text):
    """Represent a tweet.

    Minimal implementation to make tweets selectable and pass keypresses up the
    widget hierarchy.
    """
    def selectable(self):
        """Return True to allow selection."""
        return True

    def keypress(self, size, key):
        """Do nothing.

        Return the key to propagate it to a widget that can handle it.
        """
        return key

class UI(object):
    """Control the UI for PCTC.

    Public methods:
        change_focus: switch the focus to the next area of the window
        handle:       handle a keypress
        post:         post a tweet
        refresh:      check for new updates and replies
        reply:        start replying to a tweet
        scroll:       move to the top or bottom of a column on home or end

    Class constants:
        palette: colour settings for the UI

    Instance variables:
        self.columns:  urwid.Columns holding self.updates and self.replies
        self.footer:   urwid.Edit for entering updates to post
        self.focussed: variable to keep track of the currently focussed area
        self.frame:    top level urwid.Frame widget
        self.replies:  list of Tweet objects for replies
        self.twitobj:  the pctclib.backend.twitter object passed to the
                       constructor
        self.updates:  list of Tweet objects for updates
    """

    palette = [
            ('header', 'light green', 'dark blue'),
            ('footer', 'header'),
            ('bg', 'white', 'dark gray'),
            ('in focus', 'dark gray', 'white'),
        ]

    def __init__(self, twitobj):
        """Start the PCTC UI running with the twitobj passed in."""
        self.twitobj = twitobj

        header = urwid.Text("Welcome to PCTC. Logged in as %s (@%s)." %
                                            (twitobj.name, twitobj.username))
        header = urwid.AttrMap(header, 'header')

        self.replies = self._wrap_statuses(twitobj.get_replies())
        self.updates = self._wrap_statuses(twitobj.get_updates())
        self.columns = urwid.Columns([self.updates, self.replies], dividechars=2)

        self.footer = urwid.AttrMap(urwid.Edit("Tweet: "), 'footer')

        self.frame = urwid.Frame(self.columns, header, self.footer, focus_part='footer')
        self.focussed = 'footer'
        wrapped = urwid.AttrMap(self.frame, 'bg')
        loop = urwid.MainLoop(wrapped, UI.palette, unhandled_input=self.handle)
        loop.set_alarm_in(300, self._wrapped_refresh)
        try:
            loop.run()
        except KeyboardInterrupt:
            print "Keyboard interrupt received, quitting gracefully"
            raise urwid.ExitMainLoop

    def _wrap_statuses(self, statuses):
        """Prepare a list of strings for use in self.columns.

        The strings are turned into Tweet objects, given an urwid.AttrMap to
        colour them when focussed, then built into an urwid.ListBox.
        """
        textlist = map(Tweet, statuses)
        walker = urwid.SimpleListWalker([
                urwid.AttrMap(w, None, 'in focus') for w in textlist
            ])
        return urwid.ListBox(walker)

    def handle(self, keys):
        """Handle keypresses.

        Current bindings:
            tab:   change focus
            enter: post a tweet
            f5:    refresh the screen
            home:  scroll the current column to the top
            end:   scroll the current column to the bottom
            r:     reply (see docs for self.reply)
        """
        methdict = {
                'tab'   : self.change_focus,
                'enter' : self.post,
                'f5'    : self.refresh,
                'home'  : lambda: self.scroll('home'),
                'end'   : lambda: self.scroll('end'),
                'r'     : self.reply,
            }
        try:
            methdict[keys]()
        except KeyError:
            pass

    def change_focus(self):
        """Switch focus between the footer and the body."""
        if self.focussed == 'footer':
            self.frame.set_focus('body')
            self.focussed = 'body'
        elif self.focussed == 'body':
            self.frame.set_focus('footer')
            self.focussed = 'footer'

    def post(self):
        """Post the currently entered text to Twitter.

        Silently fails if the text is too long.
        """
        edit = self.footer.original_widget
        text = edit.get_edit_text()
        edit.set_edit_text('')
        if len(text) < 140:
            self.twitobj.post(text)

    def refresh(self):
        """Update the updates and replies."""
        for category in ('replies', 'updates'):
            walker = getattr(self, category).body
            statuses = getattr(self.twitobj, 'get_%s' % category)()
            statuses = map(urwid.Text, statuses)
            statuses = [urwid.AttrMap(s, None, ('in focus')) for s in statuses]
            walker[:] = statuses

    def scroll(self, key):
        """Move the currently focussed column to the top or the bottom."""
        widget = self.columns.get_focus()
        if key == "home":
            widget.set_focus(0)
        elif key == "end":
            widget.set_focus(len(widget.body))

    def reply(self):
        """Begin a reply to the currently selected tweet.

        This method moves the focus from the columns to the footer and adds
        @user_who_posted_selected_tweet to the beginning.
        """
        listbox = self.columns.get_focus()
        tweet, pos = listbox.get_focus()
        tweettext = tweet.original_widget.text
        edit = self.footer.original_widget
        matches = re.findall(r'@\w+', tweettext)
        edit.insert_text(matches[-1])
        edit.insert_text(' ')
        self.frame.set_focus('footer')

    def _wrapped_refresh(self, loop, *args):
        """Refresh and set the loop to refresh again in 300 secs."""
        self.refresh()
        loop.set_alarm_in(300, self._wrapped_refresh)
