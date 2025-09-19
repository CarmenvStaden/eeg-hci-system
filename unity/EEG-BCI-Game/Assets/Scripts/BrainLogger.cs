using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using static TgcClient;

public class BrainLogger : MonoBehaviour
{
    public TgcClient tgc;   //  TGCManager obj
    string filePath;

    // buffer raw EEG lines here
    List<string> buffer = new List<string>();
    float flushInterval = 1f;   // write every 1 second
    float timer;

    int currentAttention = -1;
    int currentMeditation = -1;

    EegPower latestBands;

    void Start()
    {
        // Create a timestamped CSV file in persistent data path
        string filename = "BrainLog_" + System.DateTime.Now.ToString("yyyyMMdd_HHmmss") + ".csv";
        filePath = Path.Combine(Application.persistentDataPath, filename);

        // Write header row
        File.AppendAllText(filePath,
            "Timestamp,Attention,Meditation,RawEEG," +
            "Delta,Theta,LowAlpha,HighAlpha,LowBeta,HighBeta,LowGamma,MidGamma\n");

        if (tgc != null)
        {
            tgc.AttentionChanged += OnAttention;
            tgc.MeditationChanged += OnMeditation;
            tgc.RawEegReceived += OnRawEeg; 
            tgc.EegPowerReceived += OnEegPower;
            Debug.Log("[BrainLogger] Subscribed to TgcClient events.");
        }
        else
        {
            Debug.LogWarning("[BrainLogger] TgcClient reference not set!");
        }


        Debug.Log("[BrainLogger] Logging to: " + filePath);
    }


    void OnEegPower(EegPower bands)
    {
        latestBands = bands;
    }

    void OnAttention(int v)
    {
        currentAttention = v;
        Debug.Log($"[BrainLogger] Attention updated: {v}");
    }

    void OnMeditation(int v)
    {
        currentMeditation = v;
        Debug.Log($"[BrainLogger] Meditation updated: {v}");
    }

    void OnRawEeg(int raw)
    {
        string line =
            $"{System.DateTime.UtcNow:O},{currentAttention},{currentMeditation},{raw}," +
            $"{latestBands.delta},{latestBands.theta},{latestBands.lowAlpha},{latestBands.highAlpha}," +
            $"{latestBands.lowBeta},{latestBands.highBeta},{latestBands.lowGamma},{latestBands.midGamma}";
        buffer.Add(line);
    }

    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= flushInterval && buffer.Count > 0)
        {
            Debug.Log($"[BrainLogger] Flushing {buffer.Count} samples to file.");
            FlushBuffer();
            timer = 0f;
        }
    }

    void FlushBuffer()
    {
        try
        {
            File.AppendAllLines(filePath, buffer);
            Debug.Log($"[BrainLogger] Wrote {buffer.Count} lines to {filePath}");
            buffer.Clear();
        }
        catch (IOException e)
        {
            Debug.LogWarning("[BrainLogger] File write failed: " + e.Message);
        }
    }

    void OnDestroy()
    {
        if (tgc != null)
        {
            tgc.AttentionChanged -= OnAttention;
            tgc.MeditationChanged -= OnMeditation;
            tgc.RawEegReceived -= OnRawEeg;
        }

        // write any remaining samples
        if (buffer.Count > 0)
        {
            Debug.Log("[BrainLogger] Flushing remaining samples on destroy.");
            FlushBuffer();
        }
    }
}
