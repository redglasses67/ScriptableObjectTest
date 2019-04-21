# ScriptableObjectTest
Scriptable Object in Unity create with python from Maya

MayaからPythonを使って、UnityのScriptable Objectを生成します。

***

## はじめに ruamel.yaml について

**© Copyright 2017-2018, Anthon van der Neut, Ruamel bvba Revision 80876ef99969.**

https://pypi.org/project/ruamel.yaml/

* License : MIT License (MIT license)
* Author  : Anthon van der Neut

***
## 使い方
### Unity側

* Maya側で使うために **YAML_ClassID_List.txt** を参照しています。

	このテキストファイルはUnity側の Tools > YAML Class ID Listup で生成できます。

* また、Mayaから書き出すScriptable Objectのベースとなるファイルを

	Unity側の Tools > Create TestScriptableObject Sample から生成できます。


### Maya側
※下記のスクリプトを使うためには

DLしてZIPを解凍してもらった置き場所の  **MayaScript** フォルダまでのパスを通してもらうか、

もしくは各スクリプトの実行文の前に下記の２行を付け足してから実行して下さい。
```python
import sys
sys.path.append(r"MayaScript フォルダまでのフルパス")
```

* CreateScriptableObjectFromMaya.py

	Unity側から書き出した *TestScriptableObject_Sample.asset* を一度読み込んで、
	
	Maya上で選択しているオブジェクトの名前と移動・回転・スケールの値を書き込み、
	
	*TestScriptableObject_ + シーン名 .asset* のScriptableObjectを生成します。

	実行文

	```python
	import CreateScriptableObjectFromMaya
	CreateScriptableObjectFromMaya.main()
	```

* ShowMaterialPropertyList.py

	Assets/Materialsにある *TestMaterial.mat* を参照して、プロパティの一覧をprintします。

	実行文

	```python
	import ShowMaterialPropertyList
	ShowMaterialPropertyList.main()
	```

* ShowScenePropertyList.py

	Assets/Scenesにある *ReadingTest.unity* を参照して、プロパティの一覧をprintします。

	実行文

	```python
	import ShowScenePropertyList
	ShowScenePropertyList.main()
	```

* ChangeMaterialValueFromMaya.py

	Assets/Materialsにある *TestMaterial.mat* を参照して、
	
	MainTexのOffsetやGlossinessの値をrandom.random()を使って適当な値に書き換え、
	
	*TestMaterial_new.mat* として書き出します。

	実行文

	```python
	import ChangeMaterialValueFromMaya
	ChangeMaterialValueFromMaya.main()
	```

* ChangeSceneSettingsFromMaya.py

	Assets/Scenesにある *ReadingTest.unity* を参照して、
	
	シーン内のDirectional LightのColor値をrandom.random()を使って適当な値に書き換え、
	
	*ReadingTest_new.unity* として書き出します。

	実行文

	```python
	import ChangeSceneSettingsFromMaya
	ChangeSceneSettingsFromMaya.main()
	```

***
## 更新履歴

2019.04.21 リリース