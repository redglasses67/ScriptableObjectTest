using UnityEngine;
using UnityEditor;
using System;
using System.Collections.Generic;

public class TestScriptableObject : ScriptableObject
{
    [System.Serializable]
    public class ObjectData
    {
        public string  ObjectName      = "";
        public Vector3 ObjectTranslate = Vector3.zero;
        public Vector3 ObjectRotate    = Vector3.zero;
        public Vector3 ObjectScale     = Vector3.one;
    }

    public string MayaSceneName = "";
    public ObjectData[] ObjectDataArray;


    [MenuItem ("Tools/Create TestScriptableObject Sample")]
    static void CreateExampleAssetInstance ()
    {
        var sampleAsset = CreateInstance<TestScriptableObject>();

        AssetDatabase.CreateAsset(sampleAsset, "Assets/TestScriptableObject_Sample.asset");
        AssetDatabase.Refresh();
    }
}