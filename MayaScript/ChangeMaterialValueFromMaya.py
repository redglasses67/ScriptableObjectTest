# -*- coding: utf-8 -*-

import os
import os.path as op
import random
import yaml
import UnityYamlUtility as uyu

def main():
	thisFilePath = op.dirname(__file__)

	# thisFilePath にディレクトリを移動
	os.chdir(thisFilePath)
	# １つ上の階層に移動
	os.chdir("..")
	# このスクリプトファイルの１つ上のディレクトリのパスを取得
	parentFolderPath = os.getcwd()

	loadMatDir      = op.join(op.join(parentFolderPath, "Assets"), "Materials")
	loadMatFilePath = op.join(loadMatDir, "TestMaterial.mat")

	unityStreamHeader, unityStreamContent = uyu.readUnityYamlData(loadMatFilePath)

	# m_TexEnvs や m_Floats がリストである点に注意！！！
	for objectID, objectData in unityStreamContent.items():
		loadMatData = yaml.safe_load(objectData)

		if "Material" in loadMatData:
			texEnvsList = loadMatData["Material"]["m_SavedProperties"]["m_TexEnvs"]
			for t in range(len(texEnvsList)):
				if "_MainTex" in texEnvsList[t]:
					texEnvsList[t]["_MainTex"]["m_Offset"]["x"] = random.random()
					texEnvsList[t]["_MainTex"]["m_Offset"]["y"] = random.random()

			floatsList = loadMatData["Material"]["m_SavedProperties"]["m_Floats"]
			for f in range(len(floatsList)):
				if "_Glossiness" in floatsList[f]:
					floatsList[f]["_Glossiness"] = random.random()

		unityStreamContent[objectID] = loadMatData

	newMatFilePath = op.join(loadMatDir, "TestMaterial_new.mat")
	uyu.writeUnityYamlData(unityStreamHeader, unityStreamContent, newMatFilePath)

if __name__ == "__main__":
	main()
