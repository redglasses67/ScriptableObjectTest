# -*- coding: utf-8 -*-

import os
import os.path as op
import UnityYamlUtility as uyu

def main():
	thisFilePath = op.dirname(__file__)
	# print("thisFilePath", thisFilePath)

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

	print("\nunityStreamHeader ============================================")
	print(unityStreamHeader)

	print("\nunityStreamContent ===========================================")
	print(unityStreamContent)


	componentList =  uyu.getComponentList(unityStreamContent)
	print("\ncomponentList ================================================")
	for component in componentList:
		print(component)

	lightPropList = uyu.getPropertiesInComponent(unityStreamContent, "Light")
	print("\nlightPropList ================================================")
	for lightProp in lightPropList:
		print(lightProp)

if __name__ == "__main__":
	main()