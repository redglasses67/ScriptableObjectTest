import os.path as op
import yaml

"""
python - PyYAML and unusual tags - Stack Overflow
https://stackoverflow.com/questions/21473076/pyyaml-and-unusual-tags
"""
def removeUnityTagAlias(filepath):
    """
    Name:               removeUnityTagAlias()

    Description:        Loads a file object from a Unity textual scene file, which is in a pseudo YAML style, and strips the
                        parts that are not YAML 1.1 compliant. Then returns a string as a stream, which can be passed to PyYAML.
                        Essentially removes the "!u!" tag directive, class type and the "&" file ID directive. PyYAML seems to handle
                        rest just fine after that.

    Returns:            String (YAML stream as string)  


    """
    header = str()
    fileID = str()
    result = str()
    
    sourceFile = open(filepath, 'r')

    for lineNumber, line in enumerate( sourceFile.readlines() ):
        if line.startswith('--- !u!'):
            print("!u!    " + line)
            #result += '--- ' + line.split(' ')[2] + '\n'   # remove the tag, but keep file ID
            header += line
            fileID = line.split(' ')[2]
        elif line.startswith("%YAML") or line.startswith("%TAG"):
            header += line
        else:
            result += line

    sourceFile.close()  

    return header, fileID, result

#print('basename:    ', op.basename(__file__))
thisFilePath = op.dirname(__file__)
print('thisFilePath:     ', thisFilePath)

testFilePath = op.join(thisFilePath, "ExampleTestScriptableObject.asset")

UnityStreamHeader, UnityStreamFileID, UnityStreamNoTags = removeUnityTagAlias(testFilePath)

print("UnityStreamHeader ============================================")
print(UnityStreamHeader)
print("==============================================================")

print("UnityStreamNoTags ============================================")
print(UnityStreamNoTags)
print("==============================================================")

# ListOfNodes = list()

# for data in yaml.load_all(UnityStreamNoTags, Loader=yaml.FullLoader):
#     ListOfNodes.append( data )

# # Example, print each object's name and type
# for node in ListOfNodes:
#     if 'm_Name' in node[ node.keys()[0] ]:
#         print( 'Name: ' + node[ node.keys()[0] ]['m_Name']  + ' NodeType: ' + node.keys()[0] )
#     else:
#         print( 'Name: ' + 'No Name Attribute'  + ' NodeType: ' + node.keys()[0] )

exportUnityPath = "E:\works\ScriptableObjectTest\Assets"
exportScriptableObjectPath = op.join(exportUnityPath, "TestScriptableObject_1.asset")

hoge = yaml.safe_load(UnityStreamNoTags)
print(hoge)
print("")
#print(hoge["MonoBehaviour"]["BaseName"])
hoge["MonoBehaviour"]["BaseName"] = "hogehoge"
#print(hoge["MonoBehaviour"]["SubDataArray"])
hoge["MonoBehaviour"]["SubDataArray"] = [
    {
        "SubName" : "sub1",
        "SubValue" : 12
    },
    {
        "SubName" : "sub2",
        "SubValue" : 37
    }]

print(hoge)

with open(exportScriptableObjectPath, "w") as wf:
    wf.write(UnityStreamHeader)
    yaml.dump(hoge, wf)