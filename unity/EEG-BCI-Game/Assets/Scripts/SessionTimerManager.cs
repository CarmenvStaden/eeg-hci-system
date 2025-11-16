using System.Collections;
using UnityEngine;

public class SessionTimerManager : MonoBehaviour
{
    // For UI
    public float RemainingSeconds { get; private set; }
    public System.Action<float> OnTick; // fires every frame with remaining seconds

    [Tooltip("Uploader that starts/ends the EEG session")]
    public EegSessionUploader uploader;

    [Tooltip("How long to run before auto-ending the session (seconds)")]
    public float sessionDuration = 30f;

    [Tooltip("In the Editor, stop Play Mode automatically when session ends")]
    public bool stopPlayModeOnEnd = true;

    [Header("EEG / Signal")]
    [Tooltip("Reference to TgcClient to monitor EEG values")]
    public TgcClient tgcClient;

    [Tooltip("Signal strength threshold required to start the session timer (lower is better, 0 = perfect, 200 = bad)")]
    public int goodSignalThreshold = 25;

    [Header("Attention scoring")]
    [Tooltip("Attention must be at or above this to count as 'focused'")]
    public int attentionThreshold = 50;

    // how many seconds during the session attention was >= attentionThreshold
    public float FocusedSeconds { get; private set; } = 0f;

    // 0–100 score: (FocusedSeconds / sessionDuration) * 100
    public float FocusScorePercent { get; private set; } = 0f;

    private Coroutine timerCo;
    private bool timerStarted = false;
    private bool sessionRunning = false;

    private int latestAttention = -1;

    void Start()
    {
        if (uploader == null)
        {
            Debug.LogError("[SessionTimerManager] No EegSessionUploader assigned.");
            return;
        }

        if (!tgcClient)
        {
            tgcClient = FindObjectOfType<TgcClient>();
        }
        if (!tgcClient)
        {
            Debug.LogError("[SessionTimerManager] No TgcClient found in scene.");
            return;
        }

        // Wait for good signal before starting the session countdown
        tgcClient.SignalStrengthChanged += OnSignalStrengthChanged;
        tgcClient.AttentionChanged += OnAttentionChanged;

        Debug.Log("[SessionTimerManager] Waiting for good signal to start session…");
    }

    void OnSignalStrengthChanged(int strength)
    {
        // NeuroSky: lower = better signal; 0 is best, 200 is no signal
        if (!timerStarted && strength <= goodSignalThreshold)
        {
            timerStarted = true;
            sessionRunning = true;

            Debug.Log($"[SessionTimerManager] Good signal detected (strength {strength}). Starting session timer…");

            timerCo = StartCoroutine(SessionCountdown());
        }
    }

    void OnAttentionChanged(int v)
    {
        latestAttention = v;
    }

    IEnumerator SessionCountdown()
    {
        RemainingSeconds = sessionDuration;
        FocusedSeconds = 0f;   // reset for each session
        FocusScorePercent = 0f;

        while (RemainingSeconds > 0f)
        {
            // While the session is running, accumulate time where attention is high
            if (sessionRunning && latestAttention >= attentionThreshold)
            {
                FocusedSeconds += Time.deltaTime;
            }

            OnTick?.Invoke(RemainingSeconds);   // notify UI
            yield return null;
            RemainingSeconds -= Time.deltaTime;
        }

        sessionRunning = false;
        OnTick?.Invoke(0f);                     // final tick

        // Compute a very simple focus score: percent of time above threshold
        if (sessionDuration > 0f)
        {
            float fraction = Mathf.Clamp01(FocusedSeconds / sessionDuration);
            FocusScorePercent = fraction * 100f;
        }
        else
        {
            FocusScorePercent = 0f;
        }

        Debug.Log($"[SessionTimerManager] Time is up. Ending session…");
        Debug.Log($"[SessionTimerManager] FocusedSeconds={FocusedSeconds:F2}s, " +
                  $"Score={FocusScorePercent:F1}% (attention >= {attentionThreshold}).");

        uploader.RequestEndSessionNow();

#if UNITY_EDITOR
        if (stopPlayModeOnEnd)
            UnityEditor.EditorApplication.isPlaying = false;
#endif
    }

    void OnDisable()
    {
        // If Play is stopped early, try to end the session once.
        if (uploader != null)
        {
            uploader.RequestEndSessionNow();
        }

        if (tgcClient != null)
        {
            tgcClient.SignalStrengthChanged -= OnSignalStrengthChanged;
            tgcClient.AttentionChanged -= OnAttentionChanged;
        }
    }
}
