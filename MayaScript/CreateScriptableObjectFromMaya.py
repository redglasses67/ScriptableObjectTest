# -*- coding: utf-8 -*-

import maya.cmds as mc
import os.path as op
import yaml

"""
python - PyYAML and unusual tags - Stack Overflow
https://stackoverflow.com/questions/21473076/pyyaml-and-unusual-tags
"""
def removeUnityTagAlias(filepath):
    header = str()
    result = str()
    print("header : ", header)

    sourceFile = open(filepath, 'r')

    for lineNumber, line in enumerate( sourceFile.readlines() ):
        if line.startswith("%YAML") or line.startswith("%TAG") or line.startswith("!u!"):
            header += line
        else:
            result += line

    sourceFile.close()  

    return header, result


curFileFullPath = mc.file(q=True, sceneName=True)

curFileName     = op.basename(curFileFullPath)
print('curFileName:     ', curFileName)

thisFilePath = op.dirname(__file__)
print('thisFilePath:     ', thisFilePath)

testFilePath = op.join(thisFilePath, "ExampleTestScriptableObject.asset")

UnityStreamHeader, UnityStreamNoTags = removeUnityTagAlias(testFilePath)

print("UnityStreamHeader ============================================")
print(UnityStreamHeader)
print("==============================================================")

print("UnityStreamNoTags ============================================")
print(UnityStreamNoTags)
print("==============================================================")

exportUnityPath = "E:\works\ScriptableObjectTest\Assets"
exportScriptableObjectPath = op.join(exportUnityPath, "TestScriptableObject_" + curFileName + ".asset")

hoge = yaml.safe_load(UnityStreamNoTags)
print(hoge)
print("")
#print(hoge["MonoBehaviour"]["MayaSceneName"])
hoge["MonoBehaviour"]["MayaSceneName"] = curFileName

selList = mc.ls(sl=True)

tmpObjectData = {}
for sel in selList:
    objTranslate = mc.getAttr("%s.translate" % sel)
    objRotate    = mc.getAttr("%s.rotate" % sel)
    objScale     = mc.getAttr("%s.scale" % sel)
    tmpObjectData["ObjectName"]      = sel
    tmpObjectData["ObjectTranslate"] = objTranslate
    tmpObjectData["ObjectRotate"]    = objRotate
    tmpObjectData["ObjectScale"]     = objScale
    hoge["MonoBehaviour"]["ObjectDataArray"].append(tmpObjectData)
    
print(hoge["MonoBehaviour"]["ObjectDataArray"])
# hoge["MonoBehaviour"]["ObjectDataArray"] = [
#     {
#         "ObjectName" : "sub1",
#         "SubValue" : 12
#     },
#     {
#         "ObjectName" : "sub2",
#         "SubValue" : 37
#     }]

#print(hoge)

with open(exportScriptableObjectPath, "w") as wf:
    wf.write(UnityStreamHeader)
    yaml.dump(hoge, wf)