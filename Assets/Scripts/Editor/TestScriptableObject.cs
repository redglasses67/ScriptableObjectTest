using UnityEngine;
using UnityEditor;
using System;
using System.Collections.Generic;

public class TestScriptableObject : ScriptableObject
{
    [System.Serializable]
    public class SubData
    {
        public string SubName = "";
        public float SubValue = 0;
    }

    public string BaseName = "";
    public SubData[] SubDataArray;


    [MenuItem ("Tools/Create ExampleAsset Instance")]
    static void CreateExampleAssetInstance ()
    {
        var exampleAsset = CreateInstance<TestScriptableObject>();

        AssetDatabase.CreateAsset (exampleAsset, "Assets/ExampleTestScriptableObject.asset");
        AssetDatabase.Refresh ();
    }
}