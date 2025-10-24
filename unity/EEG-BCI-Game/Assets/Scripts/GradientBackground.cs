using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GradientBackground : MonoBehaviour
{
    public Color topColor = new Color(0.15f, 0.25f, 0.6f);   // deep blue
    public Color bottomColor = new Color(0.9f, 0.9f, 1f);     // light sky
    public int height = 512;  // gradient texture height (width auto 1)

    RawImage img;
    Texture2D tex;

    void Awake()
    {
        img = GetComponent<RawImage>();
        tex = new Texture2D(1, Mathf.Max(2, height), TextureFormat.RGBA32, false);
        tex.wrapMode = TextureWrapMode.Clamp;

        for (int y = 0; y < tex.height; y++)
        {
            float t = (float)y / (tex.height - 1);            // 0 at bottom, 1 at top
            Color c = Color.Lerp(bottomColor, topColor, t);
            tex.SetPixel(0, y, c);
        }
        tex.Apply();
        img.texture = tex;
    }

    void OnDestroy()
    {
        if (Application.isPlaying && tex != null) Destroy(tex);
    }
}
