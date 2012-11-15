import re

# Counts the amount of title elements up the chain from this.
def countParentTitles(node, count):
    if node.parent:
        if node.parent.node_type == "title":
            return countParentTitles(node.parent, count+1)
        else:
            return countParentTitles(node.parent,count)
    else:
        return count

alreadyAdded = set()
def escape(string):
    test = string.replace(" ","_").replace("\t","-")
    test = re.sub(r'[^\w]', '_', test)
    if test not in alreadyAdded:
        alreadyAdded.add(test)
        return test
    else:
        return escape(test+"_")

mapping = {}

mapping["title_start"] = lambda x: "<div style='padding-left:40px;'>"
mapping["title"]       = lambda x: ("<h" + str(countParentTitles(x,0)+1) +
                                   " id='" + escape(x.parsed_text) + "'>" +
                                   x.parsed_text + "</h" + str(countParentTitles(x,0)+1) + ">")
mapping["title_end"]   = lambda x: "</div>"

mapping["paragraph_start"] = lambda x: "<p>"
mapping["paragraph"]       = lambda x: x.parsed_text + " "
mapping["paragraph_end"]   = lambda x: "</p>"

mapping["bulleted_list_start"] = lambda x: "<ul>"
mapping["bulleted_list"]       = lambda x: "<li>" + x.parsed_text + "</li>"
mapping["bulleted_list_end"]   = lambda x: "</ul>"

mapping["numbered_list_start"] = lambda x: "<ol>"
mapping["numbered_list"]       = lambda x: "<li>" + x.parsed_text + "</li>"
mapping["numbered_list_end"]   = lambda x: "</ol>"

def map(node):
    try:
        return mapping[node.node_type](node)
    except:
        return "<!-- " + node.orig_text + " -->"

def header():
    return "<html><body>"

def footer():
    return "</body></html>"
