#!/bin/python

"""
Usage:
    stech <output_type> (- | <file>...)
"""

from docopt import docopt
from tech_tree import Tree
import sys
import fileinput

args = docopt(__doc__, version='0.01a')

generator = None
tree = Tree()

try:
    generator = __import__(args["<output_type>"])
except:
    print("generator not found")
    sys.exit(1)

for line in fileinput.input(args["<file>"]):
    tree.put(line)
tree.add(None)


print generator.header()
for node in tree.flatten():
    print generator.map(node)
print generator.footer()
