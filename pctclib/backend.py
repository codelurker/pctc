# pctc: python curses twitter client
"""Provide the backend interface to a Twitter account.

Classes:
    Twitter: represent a connection to a Twitter account
"""

import twitter

class Twitter(object):
    """Represent a connection to a Twitter account.

    Public methods:
        get_replies(self): return a list of replies to the current account
        get_updates(self): return a list of updates by followees
        post(self, text):  post an update

    Instance variables:
        self.username: the username of the current account
        self.name:     the "real name" of the current account
        self.api:      the underlying twitter.Api object
    """

    def __init__(self, uname, pw):
        """Connect to a Twitter account using uname and pw."""
        self.api = twitter.Api(username=uname, password=pw)
        self.username = uname
        self.name = self.api.GetUser(uname).name

    def get_replies(self):
        """Return a list of replies to the current user.

        The replies are given along with the originating user's real name and
        Twitter account name.
        """
        statuses = []
        for status in self.api.GetReplies():
            text = "%s\n-- %s (@%s)" % (status.text, status.user.name,
                        status.user.screen_name)
            statuses.append(text)
        statuses = [s.replace('&lt;', '<') for s in statuses]
        statuses = [s.replace('&gt;', '>') for s in statuses]
        return statuses

    def get_updates(self):
        """Return a list of updates from followed accounts.

        The updates are given along with the originating user's real name and
        Twitter account name.
        """
        statuses = []
        for status in self.api.GetFriendsTimeline():
            text = "%s\n-- %s (@%s)" % (status.text, status.user.name,
                        status.user.screen_name)
            statuses.append(text)
        statuses = [s.replace('&lt;', '<') for s in statuses]
        statuses = [s.replace('&gt;', '>') for s in statuses]
        return statuses

    def post(self, text):
        """Post an update from the current user.

        May raise urllib2.HTTPError if the current user is not properly
        authenticated.
        """
        self.api.PostUpdate(text)
