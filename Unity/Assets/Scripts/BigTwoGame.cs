using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.Networking;
#if UNITY_EDITOR
using UnityEditor;
#endif

public sealed class BigTwoGame : MonoBehaviour
{
    private static readonly char[] SuitCodes = { 'c', 'd', 'h', 's' };

    private readonly List<int>[] _hands = new List<int>[5];
    private readonly bool[] _passFlags = new bool[5];
    private readonly List<int> _desktopCards = new List<int>(13);
    private readonly HashSet<int> _selectedCards = new HashSet<int>();
    private readonly Dictionary<int, Texture2D> _cardTextures = new Dictionary<int, Texture2D>(52);

    private Texture2D _backCardTexture;
    private Texture2D _passTexture;
    private Texture2D _backgroundTexture;

    private GUIStyle _textStyle;
    private GUIStyle _titleStyle;
    private GUIStyle _buttonStyle;

    private int _turnId = 1;
    private int _owner = 1;
    private bool _firstPut = true;
    private bool _start3c = true;
    private int _countPass;
    private int _winner;

    private float _nextAiActionAt;
    private float _statusUntil;
    private string _statusMessage = string.Empty;

    private bool _assetsLoaded;
    private string _assetError = string.Empty;
    private bool _firstGuiFrameLogged;

    private System.Random _random;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    private static void BootstrapBeforeSceneLoad()
    {
        EnsureBootstrap();
    }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void BootstrapAfterSceneLoad()
    {
        EnsureBootstrap();
    }

#if UNITY_EDITOR
    [InitializeOnEnterPlayMode]
    private static void BootstrapOnEnterPlayMode(EnterPlayModeOptions options)
    {
        EnsureBootstrap();
    }
#endif

    private static void EnsureBootstrap()
    {
        if (FindObjectsByType<BigTwoGame>(FindObjectsSortMode.None).Length > 0)
        {
            return;
        }

        var gameObject = new GameObject("BigTwoGame");
        gameObject.AddComponent<BigTwoGame>();
        DontDestroyOnLoad(gameObject);
    }

    private void Awake()
    {
        EnsureCamera();
        Application.targetFrameRate = 60;
        _random = new System.Random();

        for (int i = 1; i <= 4; i++)
        {
            _hands[i] = new List<int>(13);
        }

        StartCoroutine(LoadAssetsRoutine());
        StartNewRound();
        Debug.Log($"[BigTwo] Awake complete. dataPath={Application.dataPath}, streamingAssetsPath={Application.streamingAssetsPath}");
    }

    private static void EnsureCamera()
    {
        Camera[] cameras = FindObjectsByType<Camera>(FindObjectsSortMode.None);
        for (int i = 0; i < cameras.Length; i++)
        {
            if (cameras[i] != null && cameras[i].enabled && cameras[i].gameObject.activeInHierarchy)
            {
                return;
            }
        }

        if (cameras.Length > 0)
        {
            cameras[0].enabled = true;
            cameras[0].gameObject.SetActive(true);
            return;
        }

        GameObject cameraObject = new GameObject("Main Camera");
        Camera camera = cameraObject.AddComponent<Camera>();
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(0.04f, 0.14f, 0.05f, 1f);
        camera.nearClipPlane = 0.1f;
        camera.farClipPlane = 1000f;
        camera.orthographic = true;
        camera.orthographicSize = 5f;

        DontDestroyOnLoad(cameraObject);
    }

    private void OnDestroy()
    {
        foreach (var texture in _cardTextures.Values)
        {
            if (texture != null)
            {
                Destroy(texture);
            }
        }

        if (_backCardTexture != null)
        {
            Destroy(_backCardTexture);
        }

        if (_passTexture != null)
        {
            Destroy(_passTexture);
        }

        if (_backgroundTexture != null)
        {
            Destroy(_backgroundTexture);
        }
    }

    private void Update()
    {
        if (_statusUntil > 0f && Time.time >= _statusUntil)
        {
            _statusUntil = 0f;
            _statusMessage = string.Empty;
        }

        if (_winner != 0 || !_assetsLoaded)
        {
            return;
        }

        // A player who passed cannot play again until the trick resets.
        if (_turnId == 1 && _passFlags[1])
        {
            _turnId = NextActivePlayer(1);
            _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.25f;
            return;
        }

        if (_turnId != 1 && Time.time >= _nextAiActionAt)
        {
            ExecuteAiTurn(_turnId);
        }
    }

    private void OnGUI()
    {
        if (!_firstGuiFrameLogged)
        {
            _firstGuiFrameLogged = true;
            Debug.Log($"[BigTwo] OnGUI first frame. screen={Screen.width}x{Screen.height}, turn={_turnId}");
        }

        EnsureStyles();
        DrawBackground();

        if (!_assetsLoaded)
        {
            GUI.Label(new Rect(24f, 24f, Screen.width - 48f, 40f), "Assets are loading...", _textStyle);
            return;
        }

        if (!string.IsNullOrEmpty(_assetError))
        {
            GUI.Label(new Rect(24f, 24f, Screen.width - 48f, 30f), _assetError, _textStyle);
        }

        float scale = Mathf.Clamp(Mathf.Min(Screen.width / 1280f, Screen.height / 720f), 0.65f, 1.4f);
        float cardW = ((_cardTextures.TryGetValue(4, out Texture2D tex) && tex != null) ? tex.width : 71f) * scale;
        float cardH = ((_cardTextures.TryGetValue(4, out tex) && tex != null) ? tex.height : 96f) * scale;

        DrawHeader();
        DrawAiHands(cardW, cardH);
        DrawDesktopCards(cardW, cardH);
        DrawPlayerHand(cardW, cardH);
        DrawControls(scale);
        DrawWinnerPanel();

        if (!string.IsNullOrEmpty(_statusMessage))
        {
            GUI.Label(new Rect(24f, Screen.height - 48f, Screen.width - 48f, 26f), _statusMessage, _textStyle);
        }
    }

    private void EnsureStyles()
    {
        if (_textStyle != null && _titleStyle != null && _buttonStyle != null)
        {
            return;
        }

        GUISkin skin = GUI.skin;
        GUIStyle labelBase = skin != null ? skin.label : new GUIStyle();
        GUIStyle buttonBase = skin != null ? skin.button : new GUIStyle();

        _textStyle = new GUIStyle(labelBase)
        {
            fontSize = 16,
            normal = { textColor = Color.white }
        };

        _titleStyle = new GUIStyle(labelBase)
        {
            fontSize = 24,
            fontStyle = FontStyle.Bold,
            alignment = TextAnchor.MiddleCenter,
            normal = { textColor = Color.white }
        };

        _buttonStyle = new GUIStyle(buttonBase)
        {
            fontSize = 16
        };
    }

    private void DrawBackground()
    {
        if (_backgroundTexture == null)
        {
            GUI.Box(new Rect(0f, 0f, Screen.width, Screen.height), GUIContent.none);
            return;
        }

        for (int y = 0; y < Screen.height; y += _backgroundTexture.height)
        {
            for (int x = 0; x < Screen.width; x += _backgroundTexture.width)
            {
                GUI.DrawTexture(new Rect(x, y, _backgroundTexture.width, _backgroundTexture.height), _backgroundTexture, ScaleMode.StretchToFill);
            }
        }
    }

    private void DrawHeader()
    {
        GUI.Label(new Rect(24f, 16f, 320f, 30f), "Big Two (Unity)", _titleStyle);
        GUI.Label(new Rect(24f, 56f, 440f, 24f), $"Current Turn: Player {_turnId}", _textStyle);
        GUI.Label(new Rect(24f, 80f, 440f, 24f), $"Current Owner: Player {_owner}", _textStyle);
        GUI.Label(new Rect(24f, 104f, 440f, 24f), _firstPut ? "Status: New trick" : "Status: Follow the trick", _textStyle);
        GUI.Label(new Rect(24f, 128f, 520f, 24f), "Left click cards to select. Use Play or Pass button.", _textStyle);
    }

    private void DrawAiHands(float cardW, float cardH)
    {
        float topSpacing = cardW * 0.46f;
        float sideSpacing = cardH * 0.24f;

        // Player 3 (top)
        float p3TotalW = _hands[3].Count > 0 ? cardW + (_hands[3].Count - 1) * topSpacing : 0f;
        float p3StartX = (Screen.width - p3TotalW) * 0.5f;
        float p3Y = 170f;
        for (int i = 0; i < _hands[3].Count; i++)
        {
            DrawHiddenCard(new Rect(p3StartX + i * topSpacing, p3Y, cardW, cardH));
        }
        GUI.Label(new Rect(p3StartX, p3Y - 24f, 240f, 24f), $"Player 3: {_hands[3].Count} cards", _textStyle);

        // Player 2 (right)
        float p2X = Screen.width - cardW - 28f;
        float p2Y = 220f;
        for (int i = 0; i < _hands[2].Count; i++)
        {
            DrawHiddenCard(new Rect(p2X, p2Y + i * sideSpacing, cardW, cardH));
        }
        GUI.Label(new Rect(p2X - 90f, p2Y - 24f, 180f, 24f), $"P2: {_hands[2].Count}", _textStyle);

        // Player 4 (left)
        float p4X = 28f;
        float p4Y = 220f;
        for (int i = 0; i < _hands[4].Count; i++)
        {
            DrawHiddenCard(new Rect(p4X, p4Y + i * sideSpacing, cardW, cardH));
        }
        GUI.Label(new Rect(p4X, p4Y - 24f, 180f, 24f), $"P4: {_hands[4].Count}", _textStyle);

        DrawPassFlag(3, new Rect(Screen.width * 0.5f - 55f, 145f, 110f, 44f));
        DrawPassFlag(2, new Rect(Screen.width - 180f, Screen.height * 0.5f - 22f, 110f, 44f));
        DrawPassFlag(4, new Rect(70f, Screen.height * 0.5f - 22f, 110f, 44f));
    }

    private void DrawDesktopCards(float cardW, float cardH)
    {
        if (_desktopCards.Count == 0)
        {
            return;
        }

        float spacing = _desktopCards.Count == 13 ? cardW * 0.5f : cardW * 0.9f;
        float totalWidth = cardW + (_desktopCards.Count - 1) * spacing;
        float startX = (Screen.width - totalWidth) * 0.5f;
        float y = Screen.height * 0.48f - cardH * 0.5f;

        for (int i = 0; i < _desktopCards.Count; i++)
        {
            DrawCard(_desktopCards[i], new Rect(startX + i * spacing, y, cardW, cardH));
        }
    }

    private void DrawPlayerHand(float cardW, float cardH)
    {
        List<int> hand = _hands[1];
        float spacing = cardW * 0.52f;
        float totalWidth = hand.Count > 0 ? cardW + (hand.Count - 1) * spacing : 0f;
        float startX = (Screen.width - totalWidth) * 0.5f;
        float y = Screen.height - cardH - 64f;
        List<Rect> cardRects = new List<Rect>(hand.Count);

        GUI.Label(new Rect(startX, y - 28f, 360f, 24f), $"Player 1: {hand.Count} cards", _textStyle);

        for (int i = 0; i < hand.Count; i++)
        {
            int card = hand[i];
            bool isSelected = _selectedCards.Contains(card);
            float cardY = y - (isSelected ? 28f : 0f);
            Rect rect = new Rect(startX + i * spacing, cardY, cardW, cardH);
            cardRects.Add(rect);
            DrawCard(card, rect);
        }

        if (_turnId == 1 && _winner == 0 && !_passFlags[1])
        {
            Event evt = Event.current;
            if (evt.type == EventType.MouseDown && evt.button == 0)
            {
                // Resolve overlapping hitboxes from right to left, matching the visual stacking.
                for (int i = hand.Count - 1; i >= 0; i--)
                {
                    if (cardRects[i].Contains(evt.mousePosition))
                    {
                        ToggleCardSelection(hand[i]);
                        evt.Use();
                        break;
                    }
                }
            }
        }

        DrawPassFlag(1, new Rect(Screen.width * 0.5f - 55f, Screen.height - 170f, 110f, 44f));
    }

    private void DrawControls(float scale)
    {
        float panelW = 260f;
        float panelH = 180f;
        Rect panel = new Rect(Screen.width - panelW - 24f, Screen.height - panelH - 24f, panelW, panelH);
        GUI.Box(panel, GUIContent.none);

        GUI.Label(new Rect(panel.x + 12f, panel.y + 10f, panel.width - 24f, 24f), "Controls", _titleStyle);

        if (_winner == 0)
        {
            GUI.enabled = _turnId == 1 && !_passFlags[1];
            if (GUI.Button(new Rect(panel.x + 20f, panel.y + 52f, panel.width - 40f, 42f), "Play", _buttonStyle))
            {
                HandleHumanPlay();
            }

            if (GUI.Button(new Rect(panel.x + 20f, panel.y + 102f, panel.width - 40f, 42f), "Pass", _buttonStyle))
            {
                HandleHumanPass();
            }
            GUI.enabled = true;

            if (_turnId != 1)
            {
                GUI.Label(new Rect(panel.x + 12f, panel.y + 148f, panel.width - 24f, 24f), "AI is taking turn...", _textStyle);
            }
        }
    }

    private void DrawWinnerPanel()
    {
        if (_winner == 0)
        {
            return;
        }

        Rect panel = new Rect(Screen.width * 0.5f - 180f, Screen.height * 0.5f - 100f, 360f, 200f);
        GUI.Box(panel, GUIContent.none);
        GUI.Label(new Rect(panel.x + 10f, panel.y + 20f, panel.width - 20f, 40f), $"Player {_winner} wins", _titleStyle);

        if (GUI.Button(new Rect(panel.x + 60f, panel.y + 90f, panel.width - 120f, 44f), "Start New Round", _buttonStyle))
        {
            StartNewRound();
        }
    }

    private void DrawHiddenCard(Rect rect)
    {
        if (_backCardTexture != null)
        {
            GUI.DrawTexture(rect, _backCardTexture, ScaleMode.StretchToFill);
        }
        else
        {
            GUI.Box(rect, "Back");
        }
    }

    private void DrawCard(int card, Rect rect)
    {
        if (_cardTextures.TryGetValue(card, out Texture2D texture) && texture != null)
        {
            GUI.DrawTexture(rect, texture, ScaleMode.StretchToFill);
        }
        else
        {
            GUI.Box(rect, CardLabel(card));
        }

        if (_selectedCards.Contains(card))
        {
            DrawOutline(rect, Color.yellow, 2f);
        }
    }

    private static void DrawOutline(Rect rect, Color color, float thickness)
    {
        Color org = GUI.color;
        GUI.color = color;
        GUI.DrawTexture(new Rect(rect.x, rect.y, rect.width, thickness), Texture2D.whiteTexture);
        GUI.DrawTexture(new Rect(rect.x, rect.yMax - thickness, rect.width, thickness), Texture2D.whiteTexture);
        GUI.DrawTexture(new Rect(rect.x, rect.y, thickness, rect.height), Texture2D.whiteTexture);
        GUI.DrawTexture(new Rect(rect.xMax - thickness, rect.y, thickness, rect.height), Texture2D.whiteTexture);
        GUI.color = org;
    }

    private void DrawPassFlag(int playerId, Rect rect)
    {
        if (!_passFlags[playerId])
        {
            return;
        }

        if (_passTexture != null)
        {
            GUI.DrawTexture(rect, _passTexture, ScaleMode.ScaleToFit);
        }
        else
        {
            GUI.Box(rect, "PASS");
        }
    }

    private IEnumerator LoadAssetsRoutine()
    {
        _assetsLoaded = false;
        _assetError = string.Empty;

        string streamingRoot = BuildStreamingAssetUri(Application.streamingAssetsPath, "Image");
        bool useUriLoading = Application.platform == RuntimePlatform.Android ||
                             Application.platform == RuntimePlatform.WebGLPlayer ||
                             Application.streamingAssetsPath.Contains("://", StringComparison.Ordinal);

        if (useUriLoading)
        {
            yield return LoadAssetsFromStreamingAssetsUri(streamingRoot);
        }
        else
        {
            LoadAssetsFromFileSystem();
        }

        _assetsLoaded = true;
    }

    private void LoadAssetsFromFileSystem()
    {
        List<string> imageRoots = BuildImageRoots();
        string imageRoot = imageRoots.Count > 0 ? imageRoots[0] : "(none)";
        Debug.Log($"[BigTwo] Image search roots: {string.Join(" | ", imageRoots)}");

        for (int card = 0; card < 52; card++)
        {
            _cardTextures[card] = LoadTextureByFileName(CardFileName(card), imageRoots);
        }

        _backCardTexture = LoadTextureByFileName("back101.png", imageRoots);
        _passTexture = LoadTextureByFileName("pass.png", imageRoots);
        _backgroundTexture = LoadTextureByFileName("Nostalgy.png", imageRoots);
        ValidateLoadedAssets(imageRoot);
    }

    private IEnumerator LoadAssetsFromStreamingAssetsUri(string imageRootUri)
    {
        Debug.Log($"[BigTwo] URI image root: {imageRootUri}");

        for (int card = 0; card < 52; card++)
        {
            int capturedCard = card;
            string cardUri = BuildStreamingAssetUri(imageRootUri, CardFileName(capturedCard));
            yield return LoadTextureFromUri(cardUri, texture => _cardTextures[capturedCard] = texture);
        }

        string backUri = BuildStreamingAssetUri(imageRootUri, "back101.png");
        string passUri = BuildStreamingAssetUri(imageRootUri, "pass.png");
        string backgroundUri = BuildStreamingAssetUri(imageRootUri, "Nostalgy.png");

        yield return LoadTextureFromUri(backUri, texture => _backCardTexture = texture);
        yield return LoadTextureFromUri(passUri, texture => _passTexture = texture);
        yield return LoadTextureFromUri(backgroundUri, texture => _backgroundTexture = texture);

        ValidateLoadedAssets(imageRootUri);
    }

    private void ValidateLoadedAssets(string root)
    {
        List<string> missing = new List<string>();
        if (_cardTextures.Values.Any(texture => texture == null))
        {
            missing.Add("some card textures");
        }

        if (_backCardTexture == null)
        {
            missing.Add("back101.png");
        }

        if (_passTexture == null)
        {
            missing.Add("pass.png");
        }

        if (_backgroundTexture == null)
        {
            missing.Add("Nostalgy.png");
        }

        if (missing.Count > 0)
        {
            _assetError = "Missing assets: " + string.Join(", ", missing) + $" | root={root}";
            Debug.LogWarning($"[BigTwo] {_assetError}");
        }
        else
        {
            _assetError = string.Empty;
        }
    }

    private static string BuildStreamingAssetUri(string root, string fileName)
    {
        if (string.IsNullOrWhiteSpace(root))
        {
            return fileName;
        }

        string normalizedRoot = root.Replace("\\", "/");
        string normalizedFile = fileName.Replace("\\", "/");
        return normalizedRoot.EndsWith("/", StringComparison.Ordinal)
            ? normalizedRoot + normalizedFile
            : normalizedRoot + "/" + normalizedFile;
    }

    private static IEnumerator LoadTextureFromUri(string uri, Action<Texture2D> setter)
    {
        using UnityWebRequest request = UnityWebRequestTexture.GetTexture(uri, false);
        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogWarning($"[BigTwo] Failed loading texture: {uri} | {request.error}");
            setter(null);
            yield break;
        }

        Texture2D texture = DownloadHandlerTexture.GetContent(request);
        if (texture != null)
        {
            texture.filterMode = FilterMode.Bilinear;
            texture.wrapMode = TextureWrapMode.Clamp;
        }

        setter(texture);
    }

    private static List<string> BuildImageRoots()
    {
        List<string> roots = new List<string>();
        HashSet<string> seen = new HashSet<string>(StringComparer.Ordinal);

        void AddRoot(string root)
        {
            if (string.IsNullOrWhiteSpace(root))
            {
                return;
            }

            string normalized = NormalizePath(root);
            if (string.IsNullOrWhiteSpace(normalized))
            {
                return;
            }

            if (!seen.Add(normalized))
            {
                return;
            }

            if (Directory.Exists(normalized))
            {
                roots.Add(normalized);
            }
        }

        AddRoot(Path.Combine(Application.streamingAssetsPath, "Image"));
        AddRoot(Path.Combine(Application.dataPath, "StreamingAssets", "Image"));
        AddRoot(Path.Combine(Application.dataPath, "Resources", "Data", "StreamingAssets", "Image"));

        return roots;
    }

    private static string NormalizePath(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            return string.Empty;
        }

        if (path.StartsWith("file://", StringComparison.OrdinalIgnoreCase))
        {
            try
            {
                return new Uri(path).LocalPath;
            }
            catch
            {
                return path;
            }
        }

        return path;
    }

    private static Texture2D LoadTextureByFileName(string fileName, IReadOnlyList<string> roots)
    {
        for (int i = 0; i < roots.Count; i++)
        {
            string path = Path.Combine(roots[i], fileName);
            Texture2D texture = LoadTexture(path);
            if (texture != null)
            {
                return texture;
            }
        }

        return null;
    }

    private static Texture2D LoadTexture(string path)
    {
        if (!File.Exists(path))
        {
            return null;
        }

        try
        {
            byte[] bytes = File.ReadAllBytes(path);
            Texture2D texture = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            if (!ImageConversion.LoadImage(texture, bytes, false))
            {
                UnityEngine.Object.Destroy(texture);
                return null;
            }

            texture.filterMode = FilterMode.Bilinear;
            texture.wrapMode = TextureWrapMode.Clamp;
            return texture;
        }
        catch
        {
            return null;
        }
    }

    private static string CardFileName(int card)
    {
        int rank = Rank(card);
        string rankText = rank == 12 ? "01" : (rank + 2).ToString("00");
        char suit = SuitCodes[Suit(card)];
        return $"{rankText}{suit}.png";
    }

    private static string CardLabel(int card)
    {
        int rank = Rank(card);
        string rankText;
        if (rank <= 8)
        {
            rankText = (rank + 2).ToString();
        }
        else if (rank == 9)
        {
            rankText = "J";
        }
        else if (rank == 10)
        {
            rankText = "Q";
        }
        else if (rank == 11)
        {
            rankText = "K";
        }
        else
        {
            rankText = "A";
        }

        char suit = char.ToUpperInvariant(SuitCodes[Suit(card)]);
        return rankText + suit;
    }

    private void StartNewRound()
    {
        _selectedCards.Clear();
        _desktopCards.Clear();
        _countPass = 0;
        _winner = 0;
        _firstPut = true;
        _start3c = true;

        for (int i = 1; i <= 4; i++)
        {
            _hands[i].Clear();
            _passFlags[i] = false;
        }

        List<int> deck = new List<int>(52);
        for (int card = 0; card < 52; card++)
        {
            deck.Add(card);
        }

        Shuffle(deck);

        for (int i = 0; i < 52; i++)
        {
            int player = 1 + (i % 4);
            _hands[player].Add(deck[i]);
        }

        for (int player = 1; player <= 4; player++)
        {
            _hands[player].Sort();
        }

        _turnId = FindCardOwner(4);
        _owner = _turnId;

        _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.8f;
        ShowStatus($"Player {_turnId} starts (has 3C)");
    }

    private void HandleHumanPlay()
    {
        if (_turnId != 1 || _winner != 0)
        {
            return;
        }

        if (_passFlags[1])
        {
            ShowStatus("You already passed this trick.");
            return;
        }

        List<int> putCards = _hands[1].Where(card => _selectedCards.Contains(card)).ToList();
        putCards.Sort();

        if (putCards.Count == 0)
        {
            if (_owner == 1 && !_firstPut)
            {
                _turnId = NextActivePlayer(1);
                _nextAiActionAt = Time.time + 0.5f;
                return;
            }

            if (!_firstPut)
            {
                _passFlags[1] = true;
                _countPass += 1;
                _selectedCards.Clear();
                _turnId = NextActivePlayer(1);
                ResolvePassReset();
                if (_turnId != 1)
                {
                    _nextAiActionAt = Time.time + 0.7f;
                }
                return;
            }

            ShowStatus("Please select cards.");
            return;
        }

        NormalizeWheelOrder(putCards);

        bool valid = _firstPut ? IsValidFirstPutCard(putCards) : CompareCard(_desktopCards, putCards) == 1;
        if (!valid)
        {
            _selectedCards.Clear();
            ShowStatus("Invalid move.");
            return;
        }

        _selectedCards.Clear();
        PlayMove(1, putCards);
        if (_turnId != 1 && _winner == 0)
        {
            _nextAiActionAt = Time.time + 0.7f;
        }
    }

    private void HandleHumanPass()
    {
        if (_turnId != 1 || _winner != 0)
        {
            return;
        }

        if (_passFlags[1])
        {
            ShowStatus("You already passed this trick.");
            return;
        }

        if (_selectedCards.Count > 0)
        {
            HandleHumanPlay();
            return;
        }

        if (_owner == 1 && !_firstPut)
        {
            _turnId = NextActivePlayer(1);
            _nextAiActionAt = Time.time + 0.6f;
            return;
        }

        if (_firstPut)
        {
            ShowStatus("First move cannot pass.");
            return;
        }

        _passFlags[1] = true;
        _countPass += 1;
        _turnId = NextActivePlayer(1);
        ResolvePassReset();

        if (_turnId != 1)
        {
            _nextAiActionAt = Time.time + 0.7f;
        }
    }

    private void ExecuteAiTurn(int aiPlayer)
    {
        if (aiPlayer == 1 || _winner != 0)
        {
            return;
        }

        if (_passFlags[aiPlayer])
        {
            _turnId = NextActivePlayer(aiPlayer);
            _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.6f;
            return;
        }

        if (_firstPut)
        {
            List<int> opening = Strategy(_hands[aiPlayer], true, null);
            if (opening != null && opening.Count > 0)
            {
                PlayMove(aiPlayer, opening);
            }
            else
            {
                // Defensive fallback: AI should always have at least one valid opening move.
                List<int> fallback = new List<int> { _hands[aiPlayer][0] };
                NormalizeWheelOrder(fallback);
                PlayMove(aiPlayer, fallback);
            }

            _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.8f;
            return;
        }

        if (_owner == aiPlayer)
        {
            _turnId = NextActivePlayer(aiPlayer);
            _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.6f;
            return;
        }

        List<int> move = Strategy(_hands[aiPlayer], false, _desktopCards);
        if (move != null && move.Count > 0)
        {
            PlayMove(aiPlayer, move);
            _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.8f;
            return;
        }

        _passFlags[aiPlayer] = true;
        _countPass += 1;
        _turnId = NextActivePlayer(aiPlayer);
        ResolvePassReset();
        _nextAiActionAt = _turnId == 1 ? 0f : Time.time + 0.6f;
    }

    private void PlayMove(int playerId, List<int> cards)
    {
        cards.Sort();
        NormalizeWheelOrder(cards);

        _desktopCards.Clear();
        _desktopCards.AddRange(cards);

        foreach (int card in cards)
        {
            _hands[playerId].Remove(card);
        }
        _hands[playerId].Sort();

        if (_start3c && cards.Contains(4))
        {
            _start3c = false;
        }

        _firstPut = false;
        _owner = playerId;
        _passFlags[playerId] = false;

        if (_hands[playerId].Count == 0)
        {
            _winner = playerId;
            ShowStatus($"Player {_winner} wins.");
            return;
        }

        _turnId = NextActivePlayer(playerId);
    }

    private void ResolvePassReset()
    {
        if (_countPass != 3)
        {
            return;
        }

        _countPass = 0;
        for (int i = 1; i <= 4; i++)
        {
            _passFlags[i] = false;
        }

        _desktopCards.Clear();
        _firstPut = true;
        _turnId = _owner;
        ShowStatus($"Player {_owner} leads next trick.");
    }

    private void ToggleCardSelection(int card)
    {
        if (_selectedCards.Contains(card))
        {
            _selectedCards.Remove(card);
        }
        else
        {
            _selectedCards.Add(card);
        }
    }

    private void Shuffle(List<int> cards)
    {
        for (int i = cards.Count - 1; i > 0; i--)
        {
            int j = _random.Next(i + 1);
            (cards[i], cards[j]) = (cards[j], cards[i]);
        }
    }

    private int FindCardOwner(int card)
    {
        for (int player = 1; player <= 4; player++)
        {
            if (_hands[player].Contains(card))
            {
                return player;
            }
        }

        return 1;
    }

    private static int NextPlayer(int playerId)
    {
        return (playerId % 4) + 1;
    }

    private int NextActivePlayer(int playerId)
    {
        int next = NextPlayer(playerId);
        while (next != playerId && _passFlags[next])
        {
            next = NextPlayer(next);
        }

        return next;
    }

    private void ShowStatus(string message, float seconds = 2.5f)
    {
        _statusMessage = message;
        _statusUntil = Time.time + seconds;
    }

    private static int Rank(int card)
    {
        return card / 4;
    }

    private static int Suit(int card)
    {
        return card % 4;
    }

    private static int SingleCardScore(int card)
    {
        return card switch
        {
            0 => 52,
            1 => 53,
            2 => 54,
            3 => 55,
            _ => card
        };
    }

    private static int OneCard(IReadOnlyList<int> cardList, int cardNum)
    {
        int bigCardScore = 0;
        for (int i = 0; i < cardNum; i++)
        {
            int score = SingleCardScore(cardList[i]);
            if (score > bigCardScore)
            {
                bigCardScore = score;
            }
        }

        return bigCardScore;
    }

    private static int TwoCard(IReadOnlyList<int> cardList)
    {
        if (Rank(cardList[0]) != Rank(cardList[1]))
        {
            return 0;
        }

        return OneCard(cardList, 2);
    }

    private static int StraightTaiwanBig(IReadOnlyList<int> cardList, int cardNum)
    {
        int[] numCard = new int[13];
        int sc = 0;
        for (int i = 0; i < cardNum; i++)
        {
            numCard[Rank(cardList[i])] += 1;
            if (Rank(cardList[i]) == 3)
            {
                sc = cardList[i];
            }
        }

        if (numCard[0] == 1 && numCard[1] == 1 && numCard[2] == 1 && numCard[3] == 1 && numCard[12] == 1)
        {
            return sc;
        }

        return OneCard(cardList, cardNum);
    }

    private static int FiveCard(IReadOnlyList<int> cardList)
    {
        int[] cardNumber = new int[13];
        int sameColorNum = 1;
        int color = 0;
        bool first = false;
        int seq = 0;
        int seqStart = 0;
        int threeNum = 0;
        int twoNum = 0;

        for (int i = 0; i < 5; i++)
        {
            cardNumber[Rank(cardList[i])] += 1;
            if (!first)
            {
                color = Suit(cardList[i]);
                first = true;
            }
            else if (Suit(cardList[i]) == color)
            {
                sameColorNum += 1;
            }
        }

        first = false;
        for (int i = 0; i < 13; i++)
        {
            if (cardNumber[i] == 1)
            {
                if (!first)
                {
                    seqStart = i;
                    seq = 1;
                    first = true;
                }
                else if (i == seqStart + 1)
                {
                    seqStart += 1;
                    seq += 1;
                }
            }
        }

        if (cardNumber[12] == 1 && cardNumber[0] == 1 && cardNumber[1] == 1 && cardNumber[2] == 1 && cardNumber[3] == 1)
        {
            seq = 5;
        }

        for (int i = 0; i < 13; i++)
        {
            if (cardNumber[i] == 3)
            {
                threeNum = 1;
            }
            else if (cardNumber[i] == 2)
            {
                twoNum = 1;
            }
        }

        if (seq == 5 && sameColorNum == 5)
        {
            return 9000;
        }

        if (cardNumber[Rank(cardList[0])] == 4 || cardNumber[Rank(cardList[1])] == 4)
        {
            return 8000;
        }

        if (threeNum == 1 && twoNum == 1)
        {
            return 6000;
        }

        if (seq == 5)
        {
            return 5000;
        }

        return 0;
    }

    private static int ThirteenCard(IReadOnlyList<int> cardList)
    {
        bool oneSuit = true;
        int suit = Suit(cardList[0]);
        int[] num = new int[13];

        for (int i = 0; i < 13; i++)
        {
            if (Suit(cardList[i]) != suit)
            {
                oneSuit = false;
            }

            num[Rank(cardList[i])] += 1;
        }

        bool fullRanks = true;
        for (int i = 0; i < 13; i++)
        {
            if (num[i] != 1)
            {
                fullRanks = false;
                break;
            }
        }

        if (oneSuit && fullRanks)
        {
            return 11000;
        }

        if (fullRanks)
        {
            return 10000;
        }

        return 0;
    }

    private static int FkBig(IReadOnlyList<int> cards)
    {
        Dictionary<int, List<int>> groups = new Dictionary<int, List<int>>();
        for (int i = 0; i < cards.Count; i++)
        {
            int rank = Rank(cards[i]);
            if (!groups.TryGetValue(rank, out List<int> group))
            {
                group = new List<int>();
                groups[rank] = group;
            }
            group.Add(cards[i]);
        }

        foreach (List<int> group in groups.Values)
        {
            if (group.Count == 4)
            {
                return OneCard(group, 4);
            }
        }

        return 0;
    }

    private static int FullHouseBig(IReadOnlyList<int> cards)
    {
        Dictionary<int, List<int>> groups = new Dictionary<int, List<int>>();
        for (int i = 0; i < cards.Count; i++)
        {
            int rank = Rank(cards[i]);
            if (!groups.TryGetValue(rank, out List<int> group))
            {
                group = new List<int>();
                groups[rank] = group;
            }
            group.Add(cards[i]);
        }

        foreach (List<int> group in groups.Values)
        {
            if (group.Count == 3)
            {
                return OneCard(group, 3);
            }
        }

        return 0;
    }

    private static int FourKindSmallCard(int fourKindCard, IReadOnlyList<int> cards, int listLen)
    {
        bool first = true;
        int smallCard = 0;

        for (int i = 0; i < listLen; i++)
        {
            if (Rank(cards[i]) == Rank(fourKindCard))
            {
                continue;
            }

            if (first)
            {
                smallCard = cards[i];
                first = false;
            }
            else if (SingleCardScore(smallCard) > SingleCardScore(cards[i]))
            {
                smallCard = cards[i];
            }
        }

        return smallCard;
    }

    private int CompareCard(IReadOnlyList<int> orgCardList, IReadOnlyList<int> putCardList)
    {
        int orgLen = orgCardList.Count;
        int putLen = putCardList.Count;

        if (orgLen == putLen)
        {
            if (orgLen == 1)
            {
                return OneCard(orgCardList, 1) < OneCard(putCardList, 1) ? 1 : -1;
            }

            if (orgLen == 2)
            {
                return TwoCard(orgCardList) < TwoCard(putCardList) ? 1 : -1;
            }

            if (orgLen == 5)
            {
                int putFive = FiveCard(putCardList);
                int orgFive = FiveCard(orgCardList);

                if (putFive == 9000)
                {
                    if (orgFive < 9000)
                    {
                        return 1;
                    }

                    int orgScore = orgFive + StraightTaiwanBig(orgCardList, 5);
                    int putScore = putFive + StraightTaiwanBig(putCardList, 5);
                    return orgScore < putScore ? 1 : -1;
                }

                if (putFive == 8000)
                {
                    if (orgFive == 9000)
                    {
                        return -1;
                    }

                    if (orgFive == 8000)
                    {
                        int orgScore = orgFive + FkBig(orgCardList);
                        int putScore = putFive + FkBig(putCardList);
                        return orgScore < putScore ? 1 : -1;
                    }

                    return 1;
                }

                if (orgFive == 6000)
                {
                    if (putFive == 6000)
                    {
                        int orgScore = orgFive + FullHouseBig(orgCardList);
                        int putScore = putFive + FullHouseBig(putCardList);
                        return orgScore < putScore ? 1 : -1;
                    }

                    return -1;
                }

                if (orgFive == 5000)
                {
                    if (putFive == 5000)
                    {
                        int orgScore = orgFive + StraightTaiwanBig(orgCardList, 5);
                        int putScore = putFive + StraightTaiwanBig(putCardList, 5);
                        return orgScore < putScore ? 1 : -1;
                    }

                    return -1;
                }

                return -1;
            }

            if (orgLen == 13)
            {
                int putDragon = ThirteenCard(putCardList);
                int orgDragon = ThirteenCard(orgCardList);

                if (putDragon == 11000)
                {
                    if (orgDragon < 11000)
                    {
                        return 1;
                    }

                    if (orgDragon == 11000)
                    {
                        return OneCard(orgCardList, 13) < OneCard(putCardList, 13) ? 1 : -1;
                    }

                    return -1;
                }

                if (putDragon == 10000)
                {
                    if (orgDragon < 10000)
                    {
                        return 1;
                    }

                    if (orgDragon == 10000)
                    {
                        return OneCard(orgCardList, 13) < OneCard(putCardList, 13) ? 1 : -1;
                    }

                    return -1;
                }

                return -1;
            }

            return -1;
        }

        if (putLen == 13 && ThirteenCard(putCardList) > 9000)
        {
            return 1;
        }

        if (orgLen < 13 && putLen == 5 && FiveCard(putCardList) > 7000)
        {
            return 1;
        }

        return -1;
    }

    private bool IsValidFirstPutCard(IReadOnlyList<int> putCardList)
    {
        if (_start3c)
        {
            bool has3c = false;
            for (int i = 0; i < putCardList.Count; i++)
            {
                if (putCardList[i] == 4)
                {
                    has3c = true;
                    break;
                }
            }

            if (!has3c)
            {
                return false;
            }
        }

        return putCardList.Count switch
        {
            1 => OneCard(putCardList, 1) > 0,
            2 => TwoCard(putCardList) > 0,
            5 => FiveCard(putCardList) > 0,
            13 => ThirteenCard(putCardList) > 0,
            _ => false
        };
    }

    private static void NormalizeWheelOrder(List<int> cardList)
    {
        if (cardList.Count != 5)
        {
            return;
        }

        if (Rank(cardList[0]) == 0 && Rank(cardList[1]) == 1 && Rank(cardList[2]) == 2 && Rank(cardList[3]) == 3 && Rank(cardList[4]) == 12)
        {
            int tail = cardList[4];
            for (int i = 4; i > 0; i--)
            {
                cardList[i] = cardList[i - 1];
            }
            cardList[0] = tail;
        }
    }

    private delegate bool MoveValidator(List<int> move);

    private List<int> Dragon(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        if (cardLen != 13)
        {
            return null;
        }

        List<int> putCardList = new List<int>(cardList.Take(13));
        return validator(putCardList) ? putCardList : null;
    }

    private List<int> StraightFlush(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        for (int i = 0; i <= cardLen - 5; i++)
        {
            List<int> putCardList = new List<int> { cardList[i] };
            for (int j = i + 1; j < cardLen; j++)
            {
                if (Rank(putCardList[putCardList.Count - 1]) + 1 == Rank(cardList[j]) && Suit(putCardList[putCardList.Count - 1]) == Suit(cardList[j]))
                {
                    putCardList.Add(cardList[j]);
                }
                else if (putCardList.Count == 4 && (Rank(cardList[j]) + 1) % 13 == Rank(putCardList[0]) && Suit(putCardList[0]) == Suit(cardList[j]))
                {
                    putCardList = new List<int>
                    {
                        cardList[j],
                        putCardList[0],
                        putCardList[1],
                        putCardList[2],
                        putCardList[3]
                    };
                }

                if (putCardList.Count == 5)
                {
                    NormalizeWheelOrder(putCardList);
                    if (validator(putCardList))
                    {
                        return putCardList;
                    }
                    break;
                }
            }
        }

        return null;
    }

    private List<int> FourKind(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        if (cardLen <= 5)
        {
            return null;
        }

        for (int i = 0; i <= cardLen - 4; i++)
        {
            if (Rank(cardList[i]) == Rank(cardList[i + 1]) && Rank(cardList[i]) == Rank(cardList[i + 2]) && Rank(cardList[i]) == Rank(cardList[i + 3]))
            {
                int fourKindN = cardList[i + 3];
                int otherSmallCard = FourKindSmallCard(fourKindN, cardList, cardLen);
                List<int> putCardList = new List<int>
                {
                    cardList[i],
                    cardList[i + 1],
                    cardList[i + 2],
                    cardList[i + 3],
                    otherSmallCard
                };

                if (validator(putCardList))
                {
                    return putCardList;
                }
            }
        }

        return null;
    }

    private List<int> One(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        int smallCard = cardList[0];
        int smallCardIndex = 0;

        for (int i = 0; i < cardLen; i++)
        {
            if (SingleCardScore(smallCard) > SingleCardScore(cardList[i]))
            {
                smallCard = cardList[i];
                smallCardIndex = i;
            }
        }

        for (int i = 0; i < cardLen; i++)
        {
            List<int> putCardList = new List<int> { smallCard };
            if (validator(putCardList))
            {
                return putCardList;
            }

            smallCardIndex += 1;
            smallCardIndex %= cardLen;
            smallCard = cardList[smallCardIndex];
        }

        return null;
    }

    private List<int> OneBig(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        int bigCard = cardList[0];

        for (int i = 0; i < cardLen; i++)
        {
            if (SingleCardScore(bigCard) < SingleCardScore(cardList[i]))
            {
                bigCard = cardList[i];
            }
        }

        List<int> putCardList = new List<int> { bigCard };
        return validator(putCardList) ? putCardList : null;
    }

    private List<int> FullHouse(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        int smallI = SmallOne(cardList, cardLen);

        for (int offset = 0; offset < cardLen - 2; offset++)
        {
            int i = (smallI + offset) % cardLen;
            int i1 = (i + 1) % cardLen;
            int i2 = (i + 2) % cardLen;

            if (Rank(cardList[i]) == Rank(cardList[i1]) && Rank(cardList[i]) == Rank(cardList[i2]))
            {
                for (int offsetJ = 0; offsetJ < cardLen - 1; offsetJ++)
                {
                    int j = (smallI + offsetJ) % cardLen;
                    int j1 = (j + 1) % cardLen;

                    if (j == i || j == i1 || j == i2 || j1 == i || j1 == i1 || j1 == i2)
                    {
                        continue;
                    }

                    if (Rank(cardList[j]) == Rank(cardList[j1]))
                    {
                        List<int> putCardList = new List<int>
                        {
                            cardList[i],
                            cardList[i1],
                            cardList[i2],
                            cardList[j],
                            cardList[j1]
                        };

                        if (validator(putCardList))
                        {
                            return putCardList;
                        }
                    }
                }
            }
        }

        return null;
    }

    private List<int> Straight(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        for (int i = 0; i <= cardLen - 5; i++)
        {
            int c0 = cardList[i];
            for (int i2 = i + 1; i2 <= cardLen - 4; i2++)
            {
                if (Rank(c0) + 1 < Rank(cardList[i2]))
                {
                    break;
                }

                if (Rank(c0) + 1 == Rank(cardList[i2]))
                {
                    int c1 = cardList[i2];
                    for (int i3 = i2 + 1; i3 <= cardLen - 3; i3++)
                    {
                        if (Rank(c1) + 1 < Rank(cardList[i3]))
                        {
                            break;
                        }

                        if (Rank(c1) + 1 == Rank(cardList[i3]))
                        {
                            int c2 = cardList[i3];
                            for (int i4 = i3 + 1; i4 <= cardLen - 2; i4++)
                            {
                                if (Rank(c2) + 1 < Rank(cardList[i4]))
                                {
                                    break;
                                }

                                if (Rank(c2) + 1 == Rank(cardList[i4]))
                                {
                                    int c3 = cardList[i4];
                                    for (int i5 = i4 + 1; i5 < cardLen; i5++)
                                    {
                                        if ((Rank(cardList[i5]) + 1) % 13 == Rank(c0) || Rank(c3) + 1 == Rank(cardList[i5]))
                                        {
                                            List<int> putCardList;
                                            if ((Rank(cardList[i5]) + 1) % 13 == Rank(c0))
                                            {
                                                putCardList = new List<int>
                                                {
                                                    cardList[i5],
                                                    c0,
                                                    c1,
                                                    c2,
                                                    c3
                                                };
                                            }
                                            else
                                            {
                                                putCardList = new List<int>
                                                {
                                                    c0,
                                                    c1,
                                                    c2,
                                                    c3,
                                                    cardList[i5]
                                                };
                                            }

                                            NormalizeWheelOrder(putCardList);
                                            if (validator(putCardList))
                                            {
                                                return putCardList;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        return null;
    }

    private List<int> Pair(IReadOnlyList<int> cardList, int cardLen, MoveValidator validator)
    {
        int smallI = SmallOne(cardList, cardLen);

        for (int i = 0; i < cardLen - 1; i++)
        {
            int iIndex = (smallI + i) % cardLen;
            for (int j = i + 1; j < cardLen; j++)
            {
                int jIndex = (smallI + j) % cardLen;
                if (Rank(cardList[iIndex]) == Rank(cardList[jIndex]))
                {
                    List<int> putCardList = new List<int>
                    {
                        cardList[iIndex],
                        cardList[jIndex]
                    };

                    if (validator(putCardList))
                    {
                        return putCardList;
                    }
                }
            }
        }

        return null;
    }

    private static int SmallOne(IReadOnlyList<int> cardList, int cardLen)
    {
        int smallCard = cardList[0];
        int smallCardIndex = 0;

        for (int i = 0; i < cardLen; i++)
        {
            if (SingleCardScore(smallCard) > SingleCardScore(cardList[i]))
            {
                smallCard = cardList[i];
                smallCardIndex = i;
            }
        }

        return smallCardIndex;
    }

    private int NextTurnNumOfCard(int turnId)
    {
        int nextTurn = NextPlayer(turnId);

        while (nextTurn != turnId)
        {
            if (!_passFlags[nextTurn])
            {
                break;
            }

            nextTurn = NextPlayer(nextTurn);
        }

        return _hands[nextTurn].Count;
    }

    private List<int> Strategy(IReadOnlyList<int> cardList, bool firstPlay, IReadOnlyList<int> orgCardList)
    {
        int cardLen = cardList.Count;
        MoveValidator firstValidator = move => IsValidFirstPutCard(move);
        MoveValidator compareValidator = move => CompareCard(orgCardList, move) == 1;

        if (firstPlay)
        {
            if (_start3c)
            {
                List<int> putCardList = Dragon(cardList, cardLen, firstValidator);
                if (putCardList != null && putCardList.Count > 1 && putCardList[1] == 4)
                {
                    return putCardList;
                }

                putCardList = FourKind(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    int[] num = new int[13];
                    for (int i = 0; i < putCardList.Count; i++)
                    {
                        num[Rank(putCardList[i])] += 1;
                    }

                    if (num[1] == 4)
                    {
                        return putCardList;
                    }
                }
            }

            if (cardLen == 13)
            {
                List<int> putCardList = Dragon(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }
            }

            if (cardLen > 6)
            {
                List<int> putCardList = FullHouse(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                putCardList = Straight(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                putCardList = Pair(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                if (NextTurnNumOfCard(_turnId) == 1)
                {
                    putCardList = OneBig(cardList, cardLen, firstValidator);
                    if (putCardList != null)
                    {
                        return putCardList;
                    }
                }

                return One(cardList, cardLen, firstValidator);
            }

            if (cardLen == 6 || cardLen == 5)
            {
                List<int> putCardList = StraightFlush(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                putCardList = FourKind(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                putCardList = FullHouse(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                putCardList = Straight(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                putCardList = Pair(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                if (NextTurnNumOfCard(_turnId) == 1)
                {
                    putCardList = OneBig(cardList, cardLen, firstValidator);
                    if (putCardList != null)
                    {
                        return putCardList;
                    }
                }

                return One(cardList, cardLen, firstValidator);
            }

            if (cardLen >= 2)
            {
                List<int> putCardList = Pair(cardList, cardLen, firstValidator);
                if (putCardList != null)
                {
                    return putCardList;
                }

                if (NextTurnNumOfCard(_turnId) == 1)
                {
                    putCardList = OneBig(cardList, cardLen, firstValidator);
                    if (putCardList != null)
                    {
                        return putCardList;
                    }
                }

                return One(cardList, cardLen, firstValidator);
            }

            return One(cardList, cardLen, firstValidator);
        }

        if (cardLen == 13)
        {
            List<int> putCardList = Dragon(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }
        }

        int orgCardLen = orgCardList.Count;

        if (orgCardLen == 5)
        {
            List<int> putCardList = FullHouse(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }

            putCardList = Straight(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }

            putCardList = FourKind(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }

            return StraightFlush(cardList, cardLen, compareValidator);
        }

        if (orgCardLen == 2)
        {
            List<int> putCardList = Pair(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }

            putCardList = FourKind(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }

            return StraightFlush(cardList, cardLen, compareValidator);
        }

        if (NextTurnNumOfCard(_turnId) == 1)
        {
            List<int> putCardList = OneBig(cardList, cardLen, compareValidator);
            if (putCardList != null)
            {
                return putCardList;
            }
        }

        List<int> onePut = One(cardList, cardLen, compareValidator);
        if (onePut != null)
        {
            return onePut;
        }

        List<int> fourPut = FourKind(cardList, cardLen, compareValidator);
        if (fourPut != null)
        {
            return fourPut;
        }

        return StraightFlush(cardList, cardLen, compareValidator);
    }
}
