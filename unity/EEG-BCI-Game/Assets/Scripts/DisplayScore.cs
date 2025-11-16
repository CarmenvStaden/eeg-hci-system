using UnityEngine;
using TMPro;

public class DisplayScore : MonoBehaviour
{
    [Header("References")]
    public SessionTimerManager timerManager;   // assign in inspector
    public GameObject hoverSphere;             // object to hide
    public GameObject scorePanel;              // panel to show
    public TMP_Text scoreText;                 // TMP text for score

    private bool scoreShown = false;
    private bool timerHasStarted = false;

    void Start()
    {
        if (!timerManager)
            timerManager = FindObjectOfType<SessionTimerManager>();

        if (!scorePanel)
            Debug.LogWarning("[DisplayScore] ScorePanel not assigned.");
        else
            scorePanel.SetActive(false); // hide score UI at first
    }

    void Update()
    {
        // Detect when the timer actually starts (RemainingSeconds set > 0)
        if (!timerHasStarted && timerManager.RemainingSeconds > 0f)
        {
            timerHasStarted = true;
        }

        // Only show score once, and only after timer has started
        if (!scoreShown && timerHasStarted && timerManager.RemainingSeconds <= 0f)
        {
            ShowScore();
        }
    }

    void ShowScore()
    {
        scoreShown = true;

        // Hide hover sphere
        if (hoverSphere != null)
            hoverSphere.SetActive(false);

        // Show score UI
        if (scorePanel != null)
            scorePanel.SetActive(true);

        float score = timerManager.FocusScorePercent;
        if (scoreText != null)
            scoreText.text = $"Your Score: {score:F1}%";

        Debug.Log($"[DisplayScore] Showing score: {score:F1}%");
    }
}
