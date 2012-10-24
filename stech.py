import fileinput
import json
from copy import deepcopy

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

def parse_line(line):
    trimed = line.strip()

    indent_level = 0
    for char in line:
        if char is ' ' or char is "\t":
            indent_level += 1
        else:
            break

    if trimed[0] is '"':
        return Node("paragraph", trimed[1:], line, indent_level)

    elif trimed[0] is '$':
        return Node("math", trimed[1:], line, indent_level)

    elif trimed[0] is '#':
        return Node("comment", trimed[1:], line, indent_level)

    elif trimed[0] is '*':
        return Node("bulleted_list", trimmed[1:], line,indent_level);

    elif trimmed[0:trimmed.find('.')].isdigit():
        return Node("numeric_list", trimmed[trimmed.find('.')+1:),
                    line,indent_level)

    else:
        return Node("title", trimed, line, indent_level)

class Tree():

    def __init__(self):
        self.root = Node("ROOT", "", "", -1)
        self.head = self.root

    def add(self, node):
        if node.indent > self.head.indent:
            self.head.children.append(node)
            node.parent = self.head
            self.head = node
        else:
            self.head = self.head.parent
            self.add(node)

    def __str__(self):
        return self.root.to_str(0)
def main():
    tree = Tree()

    for line in fileinput.input():
        tree.add(parse_line(line))

    print(str(tree))

main()
