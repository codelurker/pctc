# pctc.py: python curses twitter client

import ConfigParser
import os.path

class Config(object):
    config = ConfigParser.SafeConfigParser()

    def __init__(self, *files):
        self.files = []
        for fname in files:
            try:
                self.files.append(open(fname))
            except IOError:
                continue
        for fp in self.files:
            config.readfp(fp)

    def __getattr__(self, attr):
        try:
            return config.get('pctc', attr)
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            return ""

    def __setattr__(self, attr, val):
        config.set('pctc', attr, val)
        config.write(self.files[-1])

sys.modules[__name__] = Config('/etc/pctcrc', os.path.expanduser('~/.pctcrc'))
