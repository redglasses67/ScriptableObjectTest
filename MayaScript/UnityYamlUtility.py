# -*- coding: utf-8 -*-

"""
参考サイト
python - PyYAML and unusual tags - Stack Overflow
https://stackoverflow.com/questions/21473076/pyyaml-and-unusual-tags
"""

def readScriptableObjectContent(filepath):
    header   = str()
    objectID = ""
    content  = {}

    with open(filepath, "r") as rfile:
        for lineNumber, line in enumerate( rfile.readlines() ):
            #print("Num : " + str(lineNumber), line)
            if line.startswith("%YAML") or line.startswith("%TAG"): #or "!u!" in line:
            #if lineNumber == 1 or lineNumber == 2:
                header += line
            elif "!u!" in line:
                objectID = line
                content[objectID] = ""
            else:
                content[objectID] += line
                #content += line

    return header, content