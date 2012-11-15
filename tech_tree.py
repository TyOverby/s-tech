#!/bin/python

import fileinput
import json

class Node:
    def __init__(self, node_type, parsed_text, orig_text, indent_level):
        self.node_type = node_type
        self.parsed_text = parsed_text
        self.orig_text = orig_text
        self.indent= indent_level

        self.parent = None
        self.children = []

    def to_str(self, indent_level):
        toreturn = " "*4*indent_level
        toreturn += "type {0} | indent {1}".format(self.node_type, self.indent)
        toreturn += "\n"
        for child in self.children:
            toreturn += child.to_str(indent_level + 1)
        return toreturn

    def add(self, newNode):
        self.children.append(newNode)
        newNode.parent = self

def parse_line(line):
    trimed = line.strip()

    # Find out what the indent_level is
    indent_level = 0
    for char in line:
        if char is ' ' or char is "\t":
            indent_level += 1
        else:
            break

    # Try to find out what kind of line it is.
    if len(trimed) is 0:
        return Node("blank", "", line, 0)

    elif trimed[0] is '"':
        return Node("paragraph", trimed[1:], line, indent_level)

    elif trimed[0] is '$':
        return Node("math", trimed[1:], line, indent_level)

    elif trimed[0] is '#':
        return Node("comment", trimed[1:], line, indent_level)

    elif trimed[0] is '*':
        return Node("bulleted_list", trimed[1:], line,indent_level);

    elif trimed[0:trimed.find('.')].isdigit():
        return Node("numeric_list", trimed[trimmed.find('.')+1:],
                    line,indent_level)

    else:
        return Node("title", trimed, line, indent_level)

def gen_start(node):
    return Node(node.node_type+"_start","","",node.indent)

def gen_end(node):
    return Node(node.node_type+"_end","","",node.indent)

class Tree():

    def __init__(self):
        self.root = Node("ROOT", "", "", -1)
        self.head = self.root

    def put(self, text):
        self.add(parse_line(text))

    def add(self, node):
        if node == None:
            if self.head.parent:
                self.head.parent.add(gen_end(self.head))
                self.head = self.head.parent
                self.add(None)
            return

        if node.node_type == "blank":
            node.indent = self.head.indent

        if node.indent > self.head.indent:
            self.head.add(gen_start(node))
            self.head.add(node)
            self.head = node
        elif node.indent == self.head.indent:
            if self.head.node_type != node.node_type:
                self.head.parent.add(gen_end(self.head))
                self.head.parent.add(gen_start(node))
            self.head.parent.add(node)
            self.head = node
        elif node.indent < self.head.indent:
            self.head.parent.add(gen_end(self.head))
            self.head = self.head.parent
            self.add(node)


    def flatten(self,node=None):
        if not node:
            node = self.root
        yield node
        for n in node.children:
            for nn in self.flatten(n):
                yield nn

    def __str__(self):
        return self.root.to_str(0)

def main():


    tree = Tree()
    for line in fileinput.input():
        tree.add(parse_line(line))
    tree.add(None)

    print str(tree)

if __name__ == "__main__":
    main()

