#!/bin/python

import re
from s_tech import *
import sys

def countParentTitles(node, count):
    if node.parent:
        if node.parent.node_type == "title":
            return countParentTitles(node.parent, count+1)
        else:
            return countParentTitles(node.parent,count)
    else:
        return count

def transform(tree):
    errors = set()
    for node in tree.flatten(tree.root):
        node_type = node.node_type.strip()

        if node_type == "ROOT":
            header = file("./latex_files/latex_header.latex")
            yield header.read()

        elif node_type == "title":
            dec = str(countParentTitles(node,0)+1)
            if dec == 0:
                yield "\section{}["+node.node.parsed_text+"]"

        elif node_type == "paragraph_start":
            yield"\n"
        elif node_type == "paragraph":
            yield node.parsed_text+" "
        elif node_type == "paragraph_end":
            yield "\n"

        elif node_type == "bulleted_list_start":
            yield "\\begin{itemize}"
        elif node_type is "bulleted_list":
            yield "\\item "+node.parsed_text
        elif node_type == "bulleted_list_end":
            yield "\\end{itemize}"

        elif node_type == "numbered_list_start":
            yield "\\begin{enumerate}\n"
        elif node_type == "numbered_list":
            yield "\\item "+node.parsed_text+"\n"
        elif node_type == "numbered_list_end":
            yield "\\end{enumerate}"
        else:
            errors.add(node.node_type)

    for error in errors:
        sys.stderr.write("Node \""+error+"\" not found!\n")
    yield "</body></html>"

def main():
    tree = Tree()

    for line in fileinput.input():
        tree.add(parse_line(line))

    for line in transform(tree):
        print line

if __name__ == "__main__":
    main()
