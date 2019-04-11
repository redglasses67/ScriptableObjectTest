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

loadSceneDir      = op.join(op.join(parentFolderPath, "Assets"), "Scenes")
loadSceneFilePath = op.join(loadSceneDir, "ReadingTest.unity")

unityStreamHeader, unityStreamContent = uyu.readUnityYamlData(loadSceneFilePath)


for objectID, objectData in unityStreamContent.items():

	loadedSceneData = yaml.safe_load(objectData)

	if "Light" in loadedSceneData:
		loadedSceneData["Light"]["m_Color"]["r"] = random.random()
		loadedSceneData["Light"]["m_Color"]["g"] = random.random()
		loadedSceneData["Light"]["m_Color"]["b"] = random.random()

	unityStreamContent[objectID] = loadedSceneData

newSceneFilePath = op.join(loadSceneDir, "ReadingTest_new.unity")
uyu.writeUnityYamlData(unityStreamHeader, unityStreamContent, newSceneFilePath)