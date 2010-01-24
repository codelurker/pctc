# pctc.py: python curses twitter client

import sys
import ast
import os.path

fnames = ['/etc/pctcrc', os.path.expanduser('~/.pctcrc')]

# object to hold attributes reflecting the settings
class Settings(object):
    pass
settings = Settings()

class ConfigWalker(ast.NodeVisitor):
    def visit_Assign(self, node):
        target = node.targets[0].id
        value = node.value.s
        setattr(settings, target, value)

walker = ConfigWalker()

def read(filename):
    try:
        with open(filename) as f:
            walker.visit(ast.parse(f.read(), filename))
    except IOError:
        pass

def read_files(filenames):
    for name in filenames:
        read(name)

read_files(fnames)
