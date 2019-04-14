using UnityEngine;
using UnityEditor;

using System.IO;
using System.Reflection;
using System.Collections.Generic;

/*
参考サイト

【Unity】コードから最新のYAMLクラスIDリファレンスを取得する方法 - へくれすブログ
http://hecres.hatenablog.com/entry/2018/03/17/152620

※上記サイトに書いてくださっているコードを参考にしましたが、
FindTypeByPersistentTypeID
と書くべきところが
FindTypeByPresistentTypeID
と書かれていてそのままだとエラーになってしまう点にご注意を
*/

public class ListUpClassID
{
	[MenuItem ("Tools/YAML Class ID Listup")]
	static void WriteClassIdList ()
	{
		var classIdText = "";
		
		/*
		2019/04/14現在リファレンスに書かれているIDの最後が 1120 : LightmapSnapshot で、
		1500でforを回して試してみたが 1127 : VideoClipImporter が最後のようなので
		とりあえず1200でも大丈夫そう
		https://docs.unity3d.com/Manual/ClassIDReference.html
		*/
		for (var i = 0; i < 1200; i++)
		{
			// classIdDict[i] = GetClassName(i);
			Debug.Log(i + " : " + GetClassName(i));
			classIdText += i + ":" + GetClassName(i) + "\n";
		}

		var sw = new StreamWriter("YAML_ClassID_List.txt", false);
		sw.WriteLine(classIdText);
		sw.Flush();
		sw.Close();
	}

	public static string GetClassName (int classId)
	{
		var assembly = Assembly.GetAssembly(typeof(MonoScript));
		var unityType = assembly.GetType("UnityEditor.UnityType");
		var classObject = unityType.InvokeMember(
							"FindTypeByPersistentTypeID",
							BindingFlags.InvokeMethod,
							null,
							null,
							new object[] { classId });
		if (classObject == null)
		{
			return string.Empty;
		}

		var nameProperty = classObject.GetType().GetProperty("name");
		return nameProperty == null ? string.Empty : (string)nameProperty.GetValue(classObject, null);
	}
}