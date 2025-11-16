using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HoverSphere : MonoBehaviour
{
    [Header("Links")]
    public TgcClient tgc;           // drag your TGCManager here

    [Header("Hover Mapping")]
    public float minY = 0.5f;         // value = 0
    public float maxY = 1f;         // value = 100
    public float smooth = 6f;       // smoothing speed

    float targetY;

    void Start()
    {
        targetY = transform.position.y;

        if (tgc != null)
        {
            // Subscribe so we get main-thread events from your TgcClient
            tgc.AttentionChanged += OnAttention;
        }
        else
        {
            Debug.LogWarning("[HoverSphere] TgcClient not set!");
        }
    }

    void OnDestroy()
    {
        if (tgc != null) tgc.AttentionChanged -= OnAttention;
    }

    void OnAttention(int v)
    {
        float t = Mathf.Clamp01(v / 100f);
        targetY = Mathf.Lerp(minY, maxY, t);
    }

    void Update()
    {
        var p = transform.position;
        p.y = Mathf.Lerp(p.y, targetY, Time.deltaTime * smooth);
        transform.position = p;
    }
}
