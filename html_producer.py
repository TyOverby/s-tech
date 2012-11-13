#!/bin/python

from s_tech import *
import sys

def prepare_html(tree):
    root = tree.root
    traverse(root)

    return tree


# Counts the amount of title elements up the chain from this.
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
            yield "<html><body>"

        elif node_type == "title":
            dec = str(countParentTitles(node,0)+1)
            yield "<h"+dec+">"+node.parsed_text+"</h"+dec+">"

        elif node_type == "paragraph_start":
            yield"<p>"
        elif node_type == "paragraph":
            yield node.parsed_text+" "
        elif node_type == "paragraph_end":
            yield "</p>"

        elif node_type == "bulleted_list_start":
            yield "<ul>"
        elif node_type is "bulleted_list":
            yield "<li>"+node.parsed_text+"</li>"
        elif node_type == "bulleted_list_end":
            yield "</ul>"

        elif node_type == "numbered_list_start":
            yield "<ol>"
        elif node_type == "numbered_list":
            yield "<li>"+node.parsed_text+"</li>"
        elif node_type == "numbered_list_end":
            yield "</ol>"
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
