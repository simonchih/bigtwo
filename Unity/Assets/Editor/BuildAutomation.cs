#if UNITY_EDITOR
using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build.Reporting;

public static class BuildAutomation
{
    private const string FallbackScene = "Assets/test_bigtwo.unity";

    public static void BuildAndroidApk()
    {
        EnsureScenesConfigured();

        string outputDir = Path.Combine("Builds", "Android");
        Directory.CreateDirectory(outputDir);
        string outputPath = Path.Combine(outputDir, "BigTwo.apk");

        bool originalBuildAppBundle = EditorUserBuildSettings.buildAppBundle;
        try
        {
            EditorUserBuildSettings.buildAppBundle = false;
            BuildPlayerOptions options = new BuildPlayerOptions
            {
                scenes = GetEnabledScenes(),
                locationPathName = outputPath,
                target = BuildTarget.Android,
                options = BuildOptions.None
            };

            BuildReport report = BuildPipeline.BuildPlayer(options);
            if (report.summary.result != BuildResult.Succeeded)
            {
                throw new InvalidOperationException($"Android build failed: {report.summary.result}. Output: {outputPath}");
            }

            Console.WriteLine($"Android build succeeded: {outputPath}");
        }
        finally
        {
            EditorUserBuildSettings.buildAppBundle = originalBuildAppBundle;
        }
    }

    private static void EnsureScenesConfigured()
    {
        string[] scenes = GetEnabledScenes();
        if (scenes.Length > 0)
        {
            return;
        }

        if (!File.Exists(FallbackScene))
        {
            throw new FileNotFoundException($"No enabled scenes and fallback scene missing: {FallbackScene}");
        }

        EditorBuildSettings.scenes = new[]
        {
            new EditorBuildSettingsScene(FallbackScene, true)
        };
    }

    private static string[] GetEnabledScenes()
    {
        return EditorBuildSettings.scenes
            .Where(scene => scene.enabled)
            .Select(scene => scene.path)
            .ToArray();
    }
}
#endif
