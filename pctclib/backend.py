# pctc: python curses twitter client

import twitter

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
        statuses = [s.replace('&lt;', '<') for s in statuses]
        statuses = [s.replace('&gt;', '>') for s in statuses]
        return statuses

    def get_updates(self):
        statuses = []
        for status in self.api.GetFriendsTimeline():
            text = "%s\n-- %s (@%s)" % (status.text, status.user.name,
                        status.user.screen_name)
            statuses.append(text)
        statuses = [s.replace('&lt;', '<') for s in statuses]
        statuses = [s.replace('&gt;', '>') for s in statuses]
        return statuses

    def post(self, text):
        self.api.PostUpdate(text)
