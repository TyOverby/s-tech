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


mapping = {}

mapping["title"] = lambda x: "\\section{"+x.parsed_text+"}\n"

mapping["paragraph_start"] = lambda x: "\n"
mapping["paragraph"]       = lambda x: x.parsed_text
mapping["paragraph_end"]   = lambda x: "\n"

mapping["bulleted_list_start"] = lambda x: "\\begin{itemize}\n"
mapping["bulleted_list"]       = lambda x: "\\item " + x.parsed_text + "\n"
mapping["bulleted_list_end"]   = lambda x: "\\end{itemize}"

mapping["numbered_list_start"] = lambda x: "\\begin{enumerate}\n"
mapping["numbered_list"]       = lambda x: "\\item " + x.parsed_text + "\n"
mapping["numbered_list_end"]   = lambda x: "\\end{enumerate}"

def map(node):
    try:
        return mapping[node.node_type](node)
    except:
        return "%" + node.orig_text

def header():
    return """
    \\documentclass[12pt]{article}
    \\usepackage{amsmath}
    \\title{\LaTeX}
    \\date{}
    \\begin{document}
      \\maketitle
    """

def footer():
    return "\\end{document}"
