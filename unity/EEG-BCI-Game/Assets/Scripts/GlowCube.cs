using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

public class GlowCube : MonoBehaviour
{
    [Header("Appearance")]
    public Color baseColor = Color.red; 
    [Tooltip("How bright the glow can get at value=100")]
    public float maxIntensity = 5f;

    Renderer rend;
    Material mat;

    void Awake()
    {
        rend = GetComponent<Renderer>();
        // Instance the material to not edit the shared one
        mat = rend.material;

        // Base/albedo color
        mat.color = baseColor;

        // Enable emission on the material
        mat.EnableKeyword("_EMISSION");
        mat.globalIlluminationFlags = MaterialGlobalIlluminationFlags.RealtimeEmissive;

        // Start dark
        SetLevel(0);
    }

    // value 0 - 100
    public void SetLevel(int value)
    {
        // Glow intensity
        float t = Mathf.Clamp01(value / 100f);
        // Convert to gamma-space intensity to looks brighter
        Color emission = baseColor * Mathf.LinearToGammaSpace(t * maxIntensity);
        mat.SetColor("_EmissionColor", emission);

        // Float height
        float y = Mathf.Lerp(1f, 4f, t);
        Vector3 pos = transform.position;
        pos.y = y;
        transform.position = pos;
    }
}
