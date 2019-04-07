# -*- coding: utf-8 -*-

import maya.cmds as mc
import os
import os.path as op

import UnityYamlUtility as uyu

curFileFullPath = mc.file(q=True, sceneName=True)

# op.basename だけだと拡張子も入っているので、op.splitext で名前と拡張子に分ける
curFileName, _  = op.splitext(op.basename(curFileFullPath))

thisFilePath = op.dirname(__file__)

# thisFilePath にディレクトリを移動
os.chdir(thisFilePath)
# １つ上の階層に移動
os.chdir("..")
# このスクリプトファイルの１つ上のディレクトリのパスを取得
parentFolderPath = os.getcwd()

exportUnityPath = op.join(parentFolderPath, "Assets")
sampleFilePath  = op.join(exportUnityPath, "TestScriptableObject_Sample.asset")

unityStreamHeader, unityStreamContent = uyu.readUnityYamlData(sampleFilePath)

print("unityStreamHeader ============================================")
print(unityStreamHeader)
print("==============================================================")

print("unityStreamContent ============================================")
print(unityStreamContent)
print("==============================================================")

# exportScriptableObjectPath = op.join(exportUnityPath, "TestScriptableObject_" + curFileName + ".asset")

# loadedScriptableData = yaml.safe_load(unityStreamContent)

# loadedScriptableData["MonoBehaviour"]["MayaSceneName"] = curFileName

# selList = mc.ls(sl=True)

# tmpObjectDataList = []

# for sel in selList:
#     objTranslate = mc.getAttr("%s.translate" % sel)[0]
#     objRotate    = mc.getAttr("%s.rotate" % sel)[0]
#     objScale     = mc.getAttr("%s.scale" % sel)[0]

#     tmpObjectData                         = {}
#     tmpObjectData["ObjectName"]           = sel

#     tmpObjectData["ObjectTranslate"]      = {}
#     tmpObjectData["ObjectTranslate"]["x"] = objTranslate[0]
#     tmpObjectData["ObjectTranslate"]["y"] = objTranslate[1]
#     tmpObjectData["ObjectTranslate"]["z"] = objTranslate[2]
    
#     tmpObjectData["ObjectRotate"]         = {}
#     tmpObjectData["ObjectRotate"]["x"]    = objRotate[0]
#     tmpObjectData["ObjectRotate"]["y"]    = objRotate[1]
#     tmpObjectData["ObjectRotate"]["z"]    = objRotate[2]

#     tmpObjectData["ObjectScale"]          = {}
#     tmpObjectData["ObjectScale"]["x"]     = objScale[0]
#     tmpObjectData["ObjectScale"]["y"]     = objScale[1]
#     tmpObjectData["ObjectScale"]["z"]     = objScale[2]
    
#     tmpObjectDataList.append(tmpObjectData)

# loadedScriptableData["MonoBehaviour"]["ObjectDataArray"] = tmpObjectDataList

# # 書き込みの処理
# with open(exportScriptableObjectPath, "w") as wfile:
#     # file.write でまずはヘッダーを書く
#     wfile.write(unityStreamHeader)
#     # yaml.dump でMaya側から書き出したい内容を書く
#     yaml.dump(loadedScriptableData, wfile)