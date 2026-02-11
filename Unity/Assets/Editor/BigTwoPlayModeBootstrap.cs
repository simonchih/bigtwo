#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

[InitializeOnLoad]
internal static class BigTwoPlayModeBootstrap
{
    static BigTwoPlayModeBootstrap()
    {
        EditorApplication.playModeStateChanged += OnPlayModeStateChanged;
    }

    private static void OnPlayModeStateChanged(PlayModeStateChange state)
    {
        if (state != PlayModeStateChange.ExitingEditMode)
        {
            return;
        }

        EnsureSceneHasBootstrapObjects();
    }

    private static void EnsureSceneHasBootstrapObjects()
    {
        Scene activeScene = SceneManager.GetActiveScene();
        if (!activeScene.IsValid())
        {
            return;
        }

        bool changed = false;

        if (Object.FindAnyObjectByType<BigTwoGame>() == null)
        {
            GameObject game = new GameObject("BigTwoGame");
            game.AddComponent<BigTwoGame>();
            changed = true;
        }

        Camera[] cameras = Object.FindObjectsByType<Camera>(FindObjectsSortMode.None);
        bool hasEnabledCamera = false;
        for (int i = 0; i < cameras.Length; i++)
        {
            if (cameras[i] != null && cameras[i].enabled && cameras[i].gameObject.activeInHierarchy)
            {
                hasEnabledCamera = true;
                break;
            }
        }

        if (!hasEnabledCamera)
        {
            if (cameras.Length > 0 && cameras[0] != null)
            {
                cameras[0].enabled = true;
                cameras[0].gameObject.SetActive(true);
            }
            else
            {
                GameObject cameraObject = new GameObject("Main Camera");
                Camera camera = cameraObject.AddComponent<Camera>();
                camera.clearFlags = CameraClearFlags.SolidColor;
                camera.backgroundColor = new Color(0.04f, 0.14f, 0.05f, 1f);
                camera.nearClipPlane = 0.1f;
                camera.farClipPlane = 1000f;
                camera.orthographic = true;
                camera.orthographicSize = 5f;
            }

            changed = true;
        }

        if (changed)
        {
            EditorSceneManager.MarkSceneDirty(activeScene);
        }
    }
}
#endif
