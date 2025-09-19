using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BrainCubes : MonoBehaviour
{
    [Header("References")]
    public TgcClient tgc;            
    public GlowCube attentionCube;   
    public GlowCube meditationCube;  

    void OnEnable()
    {
        if (tgc != null)
        {
            tgc.AttentionChanged += OnAttention;
            tgc.MeditationChanged += OnMeditation;
        }
    }

    void OnDisable()
    {
        if (tgc != null)
        {
            tgc.AttentionChanged -= OnAttention;
            tgc.MeditationChanged -= OnMeditation;
        }
    }

    void OnAttention(int v) => attentionCube?.SetLevel(v);
    void OnMeditation(int v) => meditationCube?.SetLevel(v);
}
