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

for fname in fnames:
    if not os.path.exists(fname):
        continue
    with open(fname) as f:
        walker.visit(ast.parse(f.read(), fname))
