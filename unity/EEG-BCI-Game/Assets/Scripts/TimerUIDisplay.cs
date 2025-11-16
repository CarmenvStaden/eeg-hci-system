using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class TimerUIDisplay : MonoBehaviour
{
    [SerializeField] private SessionTimerManager sessionTimer;
    [SerializeField] private TextMeshProUGUI label;

    void Reset()
    {
        label = GetComponent<TextMeshProUGUI>();
        sessionTimer = FindAnyObjectByType<SessionTimerManager>();
    }

    void OnEnable()
    {
        if (sessionTimer != null)
            sessionTimer.OnTick += UpdateLabel;
    }

    void OnDisable()
    {
        if (sessionTimer != null)
            sessionTimer.OnTick -= UpdateLabel;
    }

    void UpdateLabel(float seconds)
    {
        if (!label) return;
        int s = Mathf.Max(0, Mathf.CeilToInt(seconds));
        int mm = s / 60;
        int ss = s % 60;
        label.text = $"{mm:00}:{ss:00}";

        // visual cues
        if (s <= 5) label.color = Color.red;
        else if (s <= 10) label.color = new Color(1f, 0.5f, 0f); // orange-ish
        else label.color = Color.white;
    }
}
