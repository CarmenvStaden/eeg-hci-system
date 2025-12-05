using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using static TgcClient; // for EegPower

public class EegSessionUploader : MonoBehaviour
{
    [System.Serializable]
    public class UnityEegConfig
    {
        public string bearerToken;
        public int gameId;
        public int prescriptionId;
    }

    [Header("Links")]
    public TgcClient tgc; // assigned TgcClient in Inspector

    [Header("Django API")]
    [Tooltip("e.g. http://127.0.0.1:8000")]
    public string baseUrl = "http://127.0.0.1:8000";  // Editor / Standalone

    [Tooltip("Set a testing token here; your React app will provide real auth later")]
    public string bearerToken = "";
    [Header("Endpoints (relative)")]
    public string startSessionPath = "/api/gamesession/sessions/start/";
    public string readingPath = "/api/gamesession/eeg-readings/";
    public string endSessionPath = "/api/gamesession/sessions/{id}/end/"; // {id} will be replaced

    [Header("Session Metadata")]
    public int gameId = 1;
    public int prescriptionId = 1;
    public int sessionIdOverride = 0; // for testing

    [Header("Posting")]
    public float postIntervalSeconds = 1.0f;
    public bool logRequests = true;

    // rolling state
    private int latestAttention = -1;
    private int latestMeditation = -1;
    private EegPower latestBands;
    private bool haveBands = false;

    private int sessionId = 0;
    private Coroutine loopCo;

    // session response
    private string endSessionResponseJson;

    void Awake()
    {
#if UNITY_WEBGL && !UNITY_EDITOR
        // In WebGL we let Vite proxy /api to backend.
        baseUrl = "";
#else
        if (string.IsNullOrEmpty(baseUrl))
            baseUrl = "http://127.0.0.1:8000";
#endif
    }

    private bool isConfigured = false;

    public void ApplyConfigFromJson(string json)
    {
        Debug.Log("[EegSessionUploader] ApplyConfigFromJson: " + json);
        var cfg = JsonUtility.FromJson<UnityEegConfig>(json);
        if (cfg == null)
        {
            Debug.LogError("[EegSessionUploader] Failed to parse config JSON.");
            return;
        }

        bearerToken = cfg.bearerToken;
        gameId = cfg.gameId;
        prescriptionId = cfg.prescriptionId;

        isConfigured = true;
    }

    public void BeginSession()
    {
        if (!isConfigured)
        {
            Debug.LogWarning("[EegSessionUploader] BeginSession called before config applied.");
            return;
        }

        // kick off session start
        Debug.Log($"[EegSessionUploader] BeginSession called. bearerToken prefix={bearerToken?.Substring(0, 12)}, gameId={gameId}, prescriptionId={prescriptionId}");
        StartCoroutine(StartSessionAndBeginPosting());
    }

    void Start()
    {
        if (tgc == null)
        {
            Debug.LogError("[EegSessionUploader] No TgcClient assigned.");
            return;
        }

        // subscribe to data
        tgc.AttentionChanged += OnAttention;
        tgc.MeditationChanged += OnMeditation;
        tgc.EegPowerReceived += OnBands;

        //StartCoroutine(StartSessionAndBeginPosting());
    }

    void OnAttention(int v) => latestAttention = v;
    void OnMeditation(int v) => latestMeditation = v;
    void OnBands(EegPower p) { latestBands = p; haveBands = true; }

    IEnumerator StartSessionAndBeginPosting()
    {
        string url = baseUrl.TrimEnd('/') + startSessionPath;

        var req = new StartSessionRequest
        {
            game_id = gameId,
            prescription_id = prescriptionId
        };

        string json = JsonUtility.ToJson(req);
        if (logRequests) Debug.Log("[EegSessionUploader] StartSession => " + json);

        bool done = false;
        bool ok = false;
        long code = 0;
        string text = null;

        yield return DjangoApiClient.PostJson(
            baseUrl.TrimEnd('/') + startSessionPath,
            json,
            bearerToken,
            (_ok, _code, _text) => { ok = _ok; code = _code; text = _text; done = true; }
        );

        while (!done) yield return null;

        if (!ok)
        {
            Debug.LogError($"[EegSessionUploader] Start failed HTTP {code}: {text}");
            yield break;
        }

        // Parse the new session id; fall back to inspector override if needed
        try
        {
            var resp = JsonUtility.FromJson<StartSessionResponse>(text ?? "{}");
            sessionId = (resp != null && resp.id != 0)
                ? resp.id
                : (sessionIdOverride != 0 ? sessionIdOverride : 0);
        }
        catch
        {
            sessionId = sessionIdOverride != 0 ? sessionIdOverride : 0;
        }

        if (sessionId == 0)
        {
            Debug.LogError("[EegSessionUploader] Could not determine session id from start response. " +
                           "Set SessionIdOverride in Inspector for now.");
            yield break;
        }

        Debug.Log($"[EegSessionUploader] Session started. sessionId={sessionId} (HTTP {code})");

        // Begin periodic posts
        loopCo = StartCoroutine(PostLoop());

    }

    IEnumerator PostLoop()
    {
        var wait = new WaitForSeconds(postIntervalSeconds);
        while (true)
        {
            yield return wait;
            // build a reading only if we have something
            if (sessionId == 0) continue;

            // Convert attention/meditation 0..100 ints => 0..1 floats (clamp)
            float att = Mathf.Clamp01(latestAttention < 0 ? 0f : latestAttention / 100f);
            float med = Mathf.Clamp01(latestMeditation < 0 ? 0f : latestMeditation / 100f);

            // If we have band powers, normalize to relative power (band / sum)
            float d = 0, t = 0, la = 0, ha = 0, lb = 0, hb = 0, lg = 0, mg = 0;
            if (haveBands)
            {
                // ThinkGear band values are large ints; normalize to proportions
                double sd = Mathf.Max(0, latestBands.delta);
                double st = Mathf.Max(0, latestBands.theta);
                double sla = Mathf.Max(0, latestBands.lowAlpha);
                double sha = Mathf.Max(0, latestBands.highAlpha);
                double slb = Mathf.Max(0, latestBands.lowBeta);
                double shb = Mathf.Max(0, latestBands.highBeta);
                double slg = Mathf.Max(0, latestBands.lowGamma);
                double smg = Mathf.Max(0, latestBands.midGamma);

                double sum = sd + st + sla + sha + slb + shb + slg + smg;
                if (sum <= 0) sum = 1.0;

                d = (float)(sd / sum);
                t = (float)(st / sum);
                la = (float)(sla / sum);
                ha = (float)(sha / sum);
                lb = (float)(slb / sum);
                hb = (float)(shb / sum);
                lg = (float)(slg / sum);
                mg = (float)(smg / sum);
            }

            var reading = new EegReadingRequest
            {
                session = sessionId,
                timestamp = System.DateTime.UtcNow.ToString("o"),
                attention = att,
                meditation = med,
                delta = d,
                theta = t,
                low_alpha = la,
                high_alpha = ha,
                low_beta = lb,
                high_beta = hb,
                low_gamma = lg,
                mid_gamma = mg
            };

            string url = baseUrl.TrimEnd('/') + readingPath;
            string json = JsonUtility.ToJson(reading);

            if (logRequests) Debug.Log("[EegSessionUploader] POST reading => " + json);

            // Fire and forget each tick
            yield return DjangoApiClient.PostJson(url, json, bearerToken, (ok, code, text) =>
            {
                if (!ok)
                {
                    Debug.LogWarning($"[EegSessionUploader] Reading failed HTTP {code}: {text}");
                }
            });
        }
    }

    private bool ending = false;
    private bool ended = false;

    public void RequestEndSessionNow()
    {
        if (ending || ended) return;
        ending = true;

        // stop periodic posting
        if (loopCo != null)
        {
            StopCoroutine(loopCo);
            loopCo = null;
        }

        // fire end-session once
        StartCoroutine(EndSessionWrapper());
    }

    private IEnumerator EndSessionWrapper()
    {
        yield return EndSession();   // call existing EndSession() coroutine
        ended = true;
        ending = false;
    }

    IEnumerator EndSession()
    {
        if (sessionId == 0) yield break;

        string path = endSessionPath.Replace("{id}", sessionId.ToString());
        string url = baseUrl.TrimEnd('/') + path;

        if (logRequests) Debug.Log("[EegSessionUploader] Ending session " + sessionId);

        bool done = false;
        yield return DjangoApiClient.PostJson(url, "{}", bearerToken, (_ok, _code, _text) =>
        {
            if (_ok)
            {
                Debug.Log($"[EegSessionUploader] Session ended (HTTP {_code}).");

                // Log the response body (the JSON returned by your API)
                Debug.Log($"[EegSessionUploader] End session response body:\n{_text}");

                //  store for later
                endSessionResponseJson = _text;
            }
            else
            {
                Debug.LogWarning($"[EegSessionUploader] End failed HTTP {_code}: {_text}");
            }

            done = true;
        });

        while (!done) yield return null;
    }

    void OnDestroy()
    {
        if (tgc != null)
        {
            tgc.AttentionChanged -= OnAttention;
            tgc.MeditationChanged -= OnMeditation;
            tgc.EegPowerReceived -= OnBands;
        }

        if (loopCo != null) StopCoroutine(loopCo);

        // try to end the session (can’t block app quit; this tries once)
        StartCoroutine(EndSession());
    }
}
