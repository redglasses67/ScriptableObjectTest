# -*- coding: utf-8 -*-

import os
import os.path as op
import UnityYamlUtility as uyu
import ruamel.yaml as yaml

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

	print("\n unityStreamHeader ============================================")
	print(unityStreamHeader)

	print("\n unityStreamContent ===========================================")
	print(unityStreamContent)

	componentList =  uyu.getComponentList(unityStreamContent)
	print("\n componentList ================================================")
	for component in componentList:
		print(component)

	for objectID, objectData in unityStreamContent.items():
		loadMatData = yaml.load(objectData, Loader=yaml.RoundTripLoader)
		if "MeshFilter" in loadMatData: 
			print("MeshFilter", loadMatData["MeshFilter"]["m_Mesh"]) 

	lightPropList = uyu.getPropertiesInComponent(unityStreamContent, "Light")
	print("\n lightPropList ================================================")
	for lightProp in lightPropList:
		print(lightProp)

	meshFilterPropList = uyu.getPropertiesInComponent(unityStreamContent, "MeshFilter")
	print("\n meshFilterPropList ================================================")
	for meshFilterProp in meshFilterPropList:
		print(meshFilterProp)

if __name__ == "__main__":
	main()