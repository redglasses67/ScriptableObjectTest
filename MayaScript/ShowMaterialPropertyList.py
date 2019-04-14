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

	loadMatDir      = op.join(op.join(parentFolderPath, "Assets"), "Materials")
	loadMatFilePath = op.join(loadMatDir, "TestMaterial.mat")

	unityStreamHeader, unityStreamContent = uyu.readUnityYamlData(loadMatFilePath)

	print("\nunityStreamHeader ============================================")
	print(unityStreamHeader)

	print("\nunityStreamContent ===========================================")
	print(unityStreamContent)


	componentList =  uyu.getComponentList(unityStreamContent)
	print("\ncomponentList ================================================")
	for component in componentList:
		print(component)

	matPropList = uyu.getPropertiesInComponent(unityStreamContent, "Material")
	print("\nmatPropList ==================================================")
	for matProp in matPropList:
		print(matProp)

if __name__ == "__main__":
	main()