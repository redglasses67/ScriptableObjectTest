# -*- coding: utf-8 -*-

import os
import os.path as op
import random
import yaml
import UnityYamlUtility as uyu

thisFilePath = op.dirname(__file__)

# thisFilePath にディレクトリを移動
os.chdir(thisFilePath)
# １つ上の階層に移動
os.chdir("..")
# このスクリプトファイルの１つ上のディレクトリのパスを取得
parentFolderPath = os.getcwd()
# print("parentFolderPath", parentFolderPath)

loadSceneDir      = op.join(op.join(parentFolderPath, "Assets"), "Scenes")
loadSceneFilePath = op.join(loadSceneDir, "ReadingTest.unity")

unityStreamHeader, unityStreamContent = uyu.readUnityYamlData(loadSceneFilePath)

print("YAML 3 ", uyu.YAML_Class_ID_Dict[3])
uyu.showComponents(unityStreamContent)

print("unityStreamHeader ============================================")
print(unityStreamHeader)
print("==============================================================")

print("unityStreamContent ============================================")
# print(unityStreamContent)
for objectID, objectData in unityStreamContent.items():
    print(objectID)
    # print(objectData)
    loadedSceneData = yaml.safe_load(objectData)
    print(loadedSceneData)
    if "Light" in loadedSceneData:
        # print("m_Color", loadedSceneData["Light"]["m_Color"])
        loadedSceneData["Light"]["m_Color"]["r"] = random.random()
        loadedSceneData["Light"]["m_Color"]["g"] = random.random()
        loadedSceneData["Light"]["m_Color"]["b"] = random.random()

    unityStreamContent[objectID] = loadedSceneData
print("==============================================================")

newSceneFilePath = op.join(loadSceneDir, "ReadingTest_new.unity")
uyu.writeUnityYamlData(unityStreamHeader, unityStreamContent, newSceneFilePath)