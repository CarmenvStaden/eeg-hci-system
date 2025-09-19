using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class TgcClient : MonoBehaviour
{
    [Header("TGC TCP Settings")]
    public string host = "127.0.0.1";
    public int port = 13854;

    TcpClient client;
    NetworkStream stream;
    Thread reader;
    volatile bool running;

    int rawEegValue = int.MinValue;

    public struct EegPower
    {
        public int delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, midGamma;
    }

    void Start()
    {
        try
        {
            client = new TcpClient();
            client.Connect(host, port);
            stream = client.GetStream();
            running = true;

            // Ask TGC for JSON output (ThinkGear Socket Protocol)
            var cfg = Encoding.ASCII.GetBytes("{\"enableRawOutput\":true,\"format\":\"Json\"}\n");
            stream.Write(cfg, 0, cfg.Length);

            // Debug: To confirm TCP connection
            Debug.Log($"[TGC] Connected to {host}:{port}. Requesting JSON…");

            reader = new Thread(ReadLoop) { IsBackground = true };
            reader.Start();
        }
        catch (Exception e)
        {
            Debug.LogError("[TGC] Connect failed: " + e.Message);
        }
    }

    void Update()
    {   
        // Log messages
        while (logQueue.TryDequeue(out var msg))
        {
            Debug.Log(msg);
        }

        // Dispatch on main thread
        if (attentionValue >= 0)
        {
            AttentionChanged?.Invoke(attentionValue);
        }
        if (meditationValue >= 0)
        {
            MeditationChanged?.Invoke(meditationValue);
        }
        if (rawEegValue != int.MinValue)
        {
            RawEegReceived?.Invoke(rawEegValue);
            rawEegValue = int.MinValue; // reset
        }

        EegPowerReceived?.Invoke(latestEegPower);

    }

    void ReadLoop()
    {
        var buf = new byte[4096];
        var sb = new StringBuilder();
        while (running)
        {
            try
            {
                int n = stream.Read(buf, 0, buf.Length);
                if (n <= 0) break;
                sb.Append(Encoding.ASCII.GetString(buf, 0, n));

                // TGC sends one JSON object per line, delimited by \r
                int idx;
                while ((idx = sb.ToString().IndexOf('\r')) >= 0)
                {
                    string line = sb.ToString(0, idx);
                    sb.Remove(0, idx + 1);
                    HandleMessage(line);
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning("[TGC] ReadLoop ended: " + e.Message);
                break;
            }
        }
        running = false;
    }

    // Pass values from bg thread (tgc) to main (unity interactions/set color)
    public int attentionValue { get; private set; } = -1;
    public int meditationValue { get; private set; } = -1;

    // queue for debug messages
    private readonly System.Collections.Concurrent.ConcurrentQueue<string> logQueue
        = new System.Collections.Concurrent.ConcurrentQueue<string>();

    void HandleMessage(string jsonLine)
    {
        // Minimal parse: pull eSense attention & meditation
        if (jsonLine.Contains("\"eSense\""))
        {
            int att = Extract(jsonLine, "\"attention\":");
            int med = Extract(jsonLine, "\"meditation\":");

            // Assign fields (ints to safely pass between threads)
            attentionValue = att;
            meditationValue = med;

            // Add messages to Q
            logQueue.Enqueue($"Attention={att}, Meditation={med}");
        }

        if (jsonLine.Contains("\"rawEeg\""))
        {
            int raw = Extract(jsonLine, "\"rawEeg\":");
            rawEegValue = raw;
        }

        if (jsonLine.Contains("\"eegPower\""))
        {
            latestEegPower = new EegPower
            {
                delta = Extract(jsonLine, "\"delta\":"),
                theta = Extract(jsonLine, "\"theta\":"),
                lowAlpha = Extract(jsonLine, "\"lowAlpha\":"),
                highAlpha = Extract(jsonLine, "\"highAlpha\":"),
                lowBeta = Extract(jsonLine, "\"lowBeta\":"),
                highBeta = Extract(jsonLine, "\"highBeta\":"),
                lowGamma = Extract(jsonLine, "\"lowGamma\":"),
                midGamma = Extract(jsonLine, "\"midGamma\":")
            };

            // TODO: parse poorSignalLevel, blinkStrength, etc.
        }
    }

    int Extract(string s, string key)
    {
        int i = s.IndexOf(key, StringComparison.Ordinal);
        if (i < 0) return -1;
        i += key.Length;
        int j = i;
        while (j < s.Length && char.IsDigit(s[j])) j++;
        int.TryParse(s.Substring(i, j - i), out var val);
        return val;
    }

    // make events usable from other scripts
    public event Action<int> AttentionChanged;
    public event Action<int> MeditationChanged;
    public event System.Action<int> RawEegReceived;
    public event System.Action<EegPower> EegPowerReceived;

    EegPower latestEegPower;

    void OnAttentionChanged(int v)
    {
        Debug.Log($"[TGC] Attention={v}");
        AttentionChanged?.Invoke(v);
    }
    void OnMeditationChanged(int v)
    {
        Debug.Log($"[TGC] Meditation={v}");
        MeditationChanged?.Invoke(v);
    }

    void OnDestroy()
    {
        running = false;
        try { stream?.Close(); } catch { }
        try { client?.Close(); } catch { }
    }
}
