# -*- coding: utf-8 -*-

import yaml
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

	with open(filePath,"r") as rfile:
		for lineNumber,line in enumerate( rfile.readlines() ):
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
	with open(filePath,"w") as wfile:
		# file.write でまずはヘッダーを書く
		wfile.write(topHeader)

		for objectHeader in contentsDict.keys():
			wfile.write(objectHeader)
			# yaml.dump でMaya側から書き出したい内容を書く
			yaml.dump(contentsDict[objectHeader], wfile)


def getComponent(objectHeader):
	"""
	objectHeaderの後半の&以降のオブジェクトIDを取り除き、先頭の--- !u!も削除した整数を取得\n
	objectHeader の例 : --- !u!1 &1876223296
	"""
	classID = int(objectHeader[0 : objectHeader.find("&") - 1].replace("--- !u!", ""))

	return YAML_Class_ID_Dict[classID]


def getComponentList(contentsDict):
	"""
	指定したcontentsDict内を検索して、何のコンポーネント or オブジェクトのリストを取得
	"""
	componentList = []

	for objectHeader in contentsDict.keys():
		#print("classID", getComponent)
		componentList.append(getComponent(objectHeader))

	return componentList


def getPropetyListInComponent(contentsDict, classType):
	"""
	contentsDict内にある指定したclassTypeのプロパティリストを取得
	"""

	classID = getKeyFromValue(YAML_Class_ID_Dict, classType)

	if classID is None:
		return

	propertyList = []

	loadedData = None

	for objectHeader, objectData in contentsDict.items():
		if "--- !u!%s" % classID in objectHeader:
			loadedData = yaml.safe_load(objectData)
			break

	propDict = loadedData[classType]

	return getDictKeysRecursively("", propDict)


def getKeyFromValue(dict, value):
	"""
	dict内に指定したvalueを持つKeyを検索して取得
	"""
	keys = [key for key, val in dict.items() if val == value]
	if len(keys) > 0:
		return keys[0]
	return None


def getDictKeysRecursively(parentKey, dict):
	"""
	指定したdict内のKeyを再帰的取得していく. なんとなくMaya風に|(縦線)で親子階層を表現
	"""
	keyList = []
	for key in dict.keys():
		if isinstance(dict[key], dict):
			childrenValList = getDictKeysRecursively(str(key), dict[key])
			keyList.extend(childrenValList)
		else:
			keyStr = str(key)
			if not parentKey == "":
				keyStr = parentKey + "|" + keyStr
			keyList.append(keyStr)

	return keyList


YAML_Class_ID_Dict = {
	1 : "GameObject",
	2 : "Component",
	3 : "LevelGameManager",
	4 : "Transform",
	5 : "TimeManager",
	6 : "GlobalGameManager",
	# 7 :
	8 : "Behaviour",
	9 : "GameManager",
	# 10 :
	11 : "AudioManager",
	12 : "ParticleAnimator",
	13 : "InputManager",
	# 14 :
	15 : "EllipsoidParticleEmitter",
	# 16 :
	17 : "Pipeline",
	18 : "EditorExtension",
	19 : "Physics2DSettings",
	20 : "Camera",
	21 : "Material",
	# 22 :
	23 : "MeshRenderer",
	# 24 :
	25 : "Renderer",
	26 : "ParticleRenderer",
	27 : "Texture",
	28 : "Texture2D",
	29 : "SceneSettings",
	30 : "GraphicsSettings",
	# 31 :
	# 32 :
	33 : "MeshFilter",
	# 34 :
	# 35 :
	# 36 :
	# 37 :
	# 38 :
	# 39 :
	# 40 :
	41 : "OcclusionPortal",
	# 42 :
	43 : "Mesh",
	# 44 :
	45 : "Skybox",
	# 46 :
	47 : "QualitySettings",
	48 : "Shader",
	49 : "TextAsset",
	50 : "Rigidbody2D",
	51 : "Physics2DManager",
	# 52 :
	53 : "Collider2D",
	54 : "Rigidbody",
	55 : "PhysicsManager",
	56 : "Collider",
	57 : "Joint",
	58 : "CircleCollider2D",
	59 : "HingeJoint",
	60 : "PolygonCollider2D",
	61 : "BoxCollider2D",
	62 : "PhysicsMaterial2D",
	# 63 :
	64 : "MeshCollider",
	65 : "BoxCollider",
	66 : "SpriteCollider2D",
	# 67 :
	68 : "EdgeCollider2D",
	# 69 :
	# 70 :
	# 71 :
	72 : "ComputeShader",
	# 73 :
	74 : "AnimationClip",
	75 : "ConstantForce",
	76 : "WorldParticleCollider",
	78 : "TagManager",
	# 79 :
	# 80 :
	81 : "AudioListener",
	82 : "AudioSource",
	83 : "AudioClip",
	84 : "RenderTexture",
	# 85 :
	# 86 :
	87 : "MeshParticleEmitter",
	88 : "ParticleEmitter",
	89 : "Cubemap",
	90 : "Avatar",
	91 : "AnimatorController",
	92 : "GUILayer",
	93 : "RuntimeAnimatorController",
	94 : "ScriptMapper",
	95 : "Animator",
	96 : "TrailRenderer",
	# 97 :
	98 : "DelayedCallManager",
	# 99 :
	# 100 :
	# 101 :
	102 : "TextMesh",
	# 103 :
	104 : "RenderSettings",
	# 105 :
	# 106 :
	# 107 :
	108 : "Light",
	109 : "CGProgram",
	110 : "BaseAnimationTrack",
	111 : "Animation",
	# 112 :
	# 113 :
	114 : "MonoBehaviour",
	115 : "MonoScript",
	116 : "MonoManager",
	117 : "Texture3D",
	118 : "NewAnimationTrack",
	119 : "Projector",
	120 : "LineRenderer",
	121 : "Flare",
	122 : "Halo",
	123 : "LensFlare",
	124 : "FlareLayer",
	125 : "HaloLayer",
	126 : "NavMeshAreas",
	127 : "HaloManager",
	128 : "Font",
	129 : "PlayerSettings",
	130 : "NamedObject",
	131 : "GUITexture",
	132 : "GUIText",
	133 : "GUIElement",
	134 : "PhysicMaterial",
	135 : "SphereCollider",
	136 : "CapsuleCollider",
	137 : "SkinnedMeshRenderer",
	138 : "FixedJoint",
	# 139 :
	140 : "RaycastCollider",
	141 : "BuildSettings",
	142 : "AssetBundle",
	143 : "CharacterController",
	144 : "CharacterJoint",
	145 : "SpringJoint",
	146 : "WheelCollider",
	147 : "ResourceManager",
	148 : "NetworkView",
	149 : "NetworkManager",
	150 : "PreloadData",
	# 151 :
	152 : "MovieTexture",
	153 : "ConfigurableJoint",
	154 : "TerrainCollider",
	155 : "MasterServerInterface",
	156 : "TerrainData",
	157 : "LightmapSettings",
	158 : "WebCamTexture",
	159 : "EditorSettings",
	160 : "InteractiveCloth",
	161 : "ClothRenderer",
	162 : "EditorUserSettings",
	163 : "SkinnedCloth",
	164 : "AudioReverbFilter",
	165 : "AudioHighPassFilter",
	166 : "AudioChorusFilter",
	167 : "AudioReverbZone",
	168 : "AudioEchoFilter",
	169 : "AudioLowPassFilter",
	170 : "AudioDistortionFilter",
	171 : "SparseTexture",
	# 172 :
	# 173 :
	# 174 :
	# 175 :
	# 176 :
	# 177 :
	# 178 :
	# 179 :
	180 : "AudioBehaviour",
	181 : "AudioFilter",
	182 : "WindZone",
	183 : "Cloth",
	184 : "SubstanceArchive",
	185 : "ProceduralMaterial",
	186 : "ProceduralTexture",
	# 187 :
	# 188 :
	# 189 :
	# 190 :
	191 : "OffMeshLink",
	192 : "OcclusionArea",
	193 : "Tree",
	194 : "NavMeshObsolete",
	195 : "NavMeshAgent",
	196 : "NavMeshSettings",
	197 : "LightProbesLegacy",
	198 : "ParticleSystem",
	199 : "ParticleSystemRenderer",
	200 : "ShaderVariantCollection",
	# 201 :
	# 202 :
	# 203 :
	# 204 :
	205 : "LODGroup",
	206 : "BlendTree",
	207 : "Motion",
	208 : "NavMeshObstacle",
	# 209 :
	210 : "TerrainInstance",
	# 211 :
	212 : "SpriteRenderer",
	213 : "Sprite",
	214 : "CachedSpriteAtlas",
	215 : "ReflectionProbe",
	216 : "ReflectionProbes",
	# 217 :
	218 : "Terrain",
	# 219 :
	220 : "LightProbeGroup",
	221 : "AnimatorOverrideController",
	222 : "CanvasRenderer",
	223 : "Canvas",
	224 : "RectTransform",
	225 : "CanvasGroup",
	226 : "BillboardAsset",
	227 : "BillboardRenderer",
	228 : "SpeedTreeWindAsset",
	229 : "AnchoredJoint2D",
	230 : "Joint2D",
	231 : "SpringJoint2D",
	232 : "DistanceJoint2D",
	233 : "HingeJoint2D",
	234 : "SliderJoint2D",
	235 : "WheelJoint2D",
	238 : "NavMeshData",
	# 239 :
	240 : "AudioMixer",
	241 : "AudioMixerController",
	# 242 :
	243 : "AudioMixerGroupController",
	244 : "AudioMixerEffectController",
	245 : "AudioMixerSnapshotController",
	246 : "PhysicsUpdateBehaviour2D",
	247 : "ConstantForce2D",
	248 : "Effector2D",
	249 : "AreaEffector2D",
	250 : "PointEffector2D",
	251 : "PlatformEffector2D",
	252 : "SurfaceEffector2D",
	# 253 :
	# 254 :
	# 255 :
	# 256 :
	# 257 :
	258 : "LightProbes",
	# 259 :
	# 260 :
	# 261 :
	# 262 :
	# 263 :
	# 264 :
	# 265 :
	# 266 :
	# 267 :
	# 268 :
	# 269 :
	# 270 :
	271 : "SampleClip",
	272 : "AudioMixerSnapshot",
	273 : "AudioMixerGroup",
	# 274 :
	# 275 :
	# 276 :
	# 277 :
	# 278 :
	# 279 :
	# 280 :
	# 281 :
	# 282 :
	# 283 :
	# 284 :
	# 285 :
	# 286 :
	# 287 :
	# 287 :
	# 289 :
	290 : "AssetBundleManifest",

	1001 : "Prefab",
	1002 : "EditorExtensionImpl",
	1003 : "AssetImporter",
	1004 : "AssetDatabase",
	1005 : "Mesh3DSImporter",
	1006 : "TextureImporter",
	1007 : "ShaderImporter",
	1008 : "ComputeShaderImporter",
	# 1009 :
	# 1010 :
	1011 : "AvatarMask",
	# 1012 :
	# 1013 :
	# 1014 :
	# 1015 :
	# 1016 :
	# 1017 :
	# 1018 :
	# 1019 :
	1020 : "AudioImporter",
	# 1021 :
	# 1022 :
	# 1023 :
	# 1024 :
	# 1025 :
	1026 : "HierarchyState",
	1027 : "GUIDSerializer",
	1028 : "AssetMetaData",
	1029 : "DefaultAsset",
	1030 : "DefaultImporter",
	1031 : "TextScriptImporter",
	1032 : "SceneAsset",
	# 1033 :
	1034 : "NativeFormatImporter",
	1035 : "MonoImporter",
	# 1036 :
	1037 : "AssetServerCache",
	1038 : "LibraryAssetImporter",
	# 1039 :
	1040 : "ModelImporter",
	1041 : "FBXImporter",
	1042 : "TrueTypeFontImporter",
	1044 : "MovieImporter",
	1045 : "EditorBuildSettings",
	1046 : "DDSImporter",
	# 1047 :
	1048 : "InspectorExpandedState",
	1049 : "AnnotationManager",
	1050 : "PluginImporter",
	1051 : "EditorUserBuildSettings",
	1052 : "PVRImporter",
	1053 : "ASTCImporter",
	1054 : "KTXImporter",


	1101 : "AnimatorStateTransition",
	1102 : "AnimatorState",
	# 1103 :
	# 1104 :
	1105 : "HumanTemplate",
	# 1106 :
	1107 : "AnimatorStateMachine",
	1108 : "PreviewAssetType",
	1109 : "AnimatorTransition",
	1110 : "SpeedTreeImporter",
	1111 : "AnimatorTransitionBase",
	1112 : "SubstanceImporter",
	1113 : "LightmapParameters",
	# 1114 :
	# 1115 :
	# 1116 :
	# 1117 :
	# 1118 :
	# 1119 :
	1120 : "LightmapSnapshot",
}