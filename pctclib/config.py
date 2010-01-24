# pctc.py: python curses twitter client
"""Provide the configuration aspects for PCTC.

The files listed in fnames are read in at import time. Further files can be
read or re-read by use of the read function.

Classes:
    ConfigWalker: internally-used class to walk the config file
    Settings:     empty class to hold settings

Functions:
    read:       read a config file
    read_files: read a list of config files in order

Variables:
    fnames:   list of config files to read (/etc/pctcrc and ~/.pctcrc by
              default)
    walker:   instance of ConfigWalker to read the files
    settings: object to hold all the settings
"""


import ast
import os.path

fnames = ['/etc/pctcrc', os.path.expanduser('~/.pctcrc')]

class Settings(object):
    """Hold settings defined in config files (empty class)."""
    pass
settings = Settings()

class ConfigWalker(ast.NodeVisitor):
    """Parse a config file.

    Config files are in Python syntax. Currently, only assignments of strings
    to variables are supported. Any such assignments are converted to
    attributes on the settings object.
    """
    def visit_Assign(self, node):
        """Callback for when an assignment statement is encountered."""
        target = node.targets[0].id
        value = node.value.s
        setattr(settings, target, value)

walker = ConfigWalker()

def read(filename):
    """Read the configuration held in filename."""
    try:
        with open(filename) as f:
            walker.visit(ast.parse(f.read(), filename))
    except IOError:
        pass

def read_files(filenames):
    """Read the filenames given in the iterable filenames."""
    for name in filenames:
        read(name)

read_files(fnames)
