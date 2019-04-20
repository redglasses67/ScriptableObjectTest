# -*- coding: utf-8 -*-
import os
import os.path as op
import ruamel.yaml as yaml
from collections import OrderedDict

"""

参考サイト

python - PyYAML and unusual tags - Stack Overflow
https://stackoverflow.com/questions/21473076/pyyaml-and-unusual-tags

フォーマットに関する説明 - Unity マニュアル
https://docs.unity3d.com/ja/current/Manual/FormatDescription.html

YAML クラス ID リファレンス - Unity マニュアル
https://docs.unity3d.com/ja/current/Manual/ClassIDReference.html

Python - Pythonの複雑にネストされた辞書の全てのKeyへのアクセス｜teratail
https://teratail.com/questions/16535

"""

def readUnityYamlData(filePath):
	"""
	filePath で指定したファイルの Unityのファイルとして不可欠な topHeader部分と\n
	objectHeaderの行をKey・内容をValueとしたcontentsDictを返す
	"""
	topHeader    = str()
	objectHeader = str()
	contentsDict = OrderedDict()

	with open(filePath, "r") as rfile:
		for lineNumber, line in enumerate( rfile.readlines() ):
			#print("Num : " + str(lineNumber),line)
			if line.startswith("%YAML") or line.startswith("%TAG"):
			#if lineNumber == 1 or lineNumber == 2:
				topHeader += line
			elif "!u!" in line:
				objectHeader = line
				contentsDict[objectHeader] = str()
			else:
				contentsDict[objectHeader] += line
				#contentsDict += line

	return topHeader, contentsDict


def writeUnityYamlData(topHeader, contentsDict, filePath):
	"""
	topHeader, contentsDictの内容を filePath で指定したファイルに出力する
	"""

	# 書き込みの処理
	with open(filePath, "w") as wfile:
		# file.write でまずはヘッダーを書く
		wfile.write(topHeader)

		for objectHeader in contentsDict.keys():
			wfile.write(objectHeader)
			# yaml.dump でMaya側から書き出したい内容を書く
			yaml.dump(contentsDict[objectHeader], wfile, Dumper=yaml.RoundTripDumper)


def getComponent(objectHeader):
	"""
	objectHeaderの後半の&以降のオブジェクトIDを取り除き,先頭の--- !u!も削除した整数を取得\n
	objectHeader の例 : --- !u!1 &1876223296
	"""
	classID = int(objectHeader[0 : objectHeader.find("&") - 1].replace("--- !u!", ""))

	yamlClassIdDict = readYamlClassIdList()
	if yamlClassIdDict is None:
		return None
	return yamlClassIdDict[classID]


def getComponentList(contentsDict):
	"""
	指定したcontentsDict内を検索して,\n
	何のコンポーネント or オブジェクトのリストを取得
	"""
	componentList = []

	for objectHeader in contentsDict.keys():
		# print("classID", objectHeader, getComponent(objectHeader))
		componentList.append(getComponent(objectHeader))

	return componentList


def getPropertiesInComponent(contentsDict, classType):
	"""
	contentsDict内にある指定したclassTypeのプロパティリストを取得
	"""

	yamlClassIdDict = readYamlClassIdList()
	if yamlClassIdDict is None:
		return

	classID = getKeyFromValue(yamlClassIdDict, classType)

	if classID is None:
		return

	propertyList = []

	loadData = None

	for objectHeader, objectData in contentsDict.items():
		if "--- !u!%s" % classID in objectHeader:
			loadData = yaml.load(objectData, Loader=yaml.RoundTripLoader)
			break

	propDict = loadData[classType]

	return getPropertiesRecursively("", propDict)


def getKeyFromValue(dictionary, value):
	"""
	dictionary内に指定したvalueを持つKeyを検索して取得
	"""
	keys = [key for key, val in dictionary.items() if val == value]
	if len(keys) > 0:
		return keys[0]
	return None


def getPropertiesRecursively(parentProp, props):
	"""
	指定したprops内のKeyを再帰的取得していく.\n
	辞書の関係の場合は | で、リストの関係の場合は - で親子階層を表現
	"""
	propList = []
	for prop in props:
		propStr = str(prop)
		# print("prop type", prop, type(prop), props[prop], type(props[prop]))
		if isinstance(prop, dict):
			propList.extend( getPropertiesRecursively(parentProp, prop) )

		elif isinstance(prop, list):
			propList.extend( getPropertiesRecursively(parentProp, prop) )

		elif isinstance(props[prop], dict):
			if not parentProp == "":
				propStr = parentProp + " | " + propStr
			propList.extend( getPropertiesRecursively(propStr, props[prop]) )

		elif isinstance(props[prop], list):
			if not parentProp == "":
				propStr = parentProp + " - " + propStr
			propList.extend( getPropertiesRecursively(propStr, props[prop]) )

		else:
			if not parentProp == "":
				propStr = parentProp + " | " + propStr + " | " + str(props[prop])
			propList.append(propStr)

	return propList


def readYamlClassIdList():
	"""
	Unity側で生成した YAML_ClassID_List.txt を読み込んで,\n
	idをKeyにした辞書を作って返す
	"""
	thisFilePath = op.dirname(__file__)

	# thisFilePath にディレクトリを移動
	os.chdir(thisFilePath)
	# １つ上の階層に移動
	os.chdir("..")
	# このスクリプトファイルの１つ上のディレクトリのパスを取得
	parentFolderPath = os.getcwd()

	loadYamlClassIdListPath = op.join(parentFolderPath, "YAML_ClassID_List.txt")

	if not op.exists(loadYamlClassIdListPath):
		print("YAML_ClassID_List.txt is not found... Please create it in Unity")
		return None

	classIdDict = OrderedDict()

	with open(loadYamlClassIdListPath, "r") as rfile:
		for line in rfile.read().splitlines():
			# line内に : がなければパス
			if not ":" in line:
				continue

			id, classType = line.split(":", 2)
			
			# classTypeが空の場合もパス
			if classType == "":
				continue

			classIdDict[ int(id) ] = classType
			# print(int(id), classType)

	return classIdDict


